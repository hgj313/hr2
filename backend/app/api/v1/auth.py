from datetime import timedelta
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, get_current_active_user
from app.core.security import (
    create_access_token, create_refresh_token, verify_password,
    get_password_hash, create_reset_password_token, create_email_verification_token,
    verify_token, generate_csrf_token, verify_csrf_token
)
from app.core.config import settings
from app.models.auth import User
from app.schemas.auth import (
    UserLogin, UserRegister, UserResponse, Token, TokenRefresh,
    PasswordReset, PasswordResetRequest, EmailVerification,
    ChangePassword, UserProfile, CSRFToken
)
from app.crud.auth import user_crud
from app.core.permissions import PermissionManager
from app.utils.email import send_reset_password_email, send_verification_email
from app.utils.audit import log_user_activity

router = APIRouter()
permission_manager = PermissionManager()


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    用户登录
    """
    # 检查登录尝试次数
    user = user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        # 记录失败的登录尝试
        await log_user_activity(
            db=db,
            user_id=None,
            action="login_failed",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details={"email": form_data.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先验证邮箱地址"
        )
    
    # 创建访问令牌和刷新令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )
    
    # 生成CSRF令牌
    csrf_token = generate_csrf_token()
    
    # 更新用户最后登录时间
    user_crud.update_last_login(db, user_id=user.id)
    
    # 记录成功的登录活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="login_success",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    # 设置安全cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_token_expires.total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite="strict"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "csrf_token": csrf_token,
        "user": UserResponse.from_orm(user)
    }


@router.post("/register", response_model=UserResponse)
async def register(
    request: Request,
    user_in: UserRegister,
    db: Session = Depends(get_db)
) -> Any:
    """
    用户注册
    """
    # 检查邮箱是否已存在
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱地址已被注册"
        )
    
    # 创建新用户
    user = user_crud.create(db, obj_in=user_in)
    
    # 发送邮箱验证邮件
    if settings.SMTP_HOST:
        verification_token = create_email_verification_token(email=user.email)
        await send_verification_email(
            email_to=user.email,
            username=user.username,
            token=verification_token
        )
    
    # 记录注册活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="user_registered",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return UserResponse.from_orm(user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> Any:
    """
    刷新访问令牌
    """
    try:
        payload = verify_token(token_data.refresh_token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user = user_crud.get(db, id=int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用"
        )
    
    # 创建新的访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # 记录令牌刷新活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="token_refreshed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    用户登出
    """
    # 清除刷新令牌cookie
    response.delete_cookie(key="refresh_token")
    
    # 记录登出活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="logout",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "成功登出"}


@router.post("/password-reset-request")
async def request_password_reset(
    request: Request,
    password_reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    请求密码重置
    """
    user = user_crud.get_by_email(db, email=password_reset_request.email)
    if not user:
        # 为了安全，即使用户不存在也返回成功消息
        return {"message": "如果该邮箱地址存在，您将收到密码重置邮件"}
    
    # 生成密码重置令牌
    reset_token = create_reset_password_token(email=user.email)
    
    # 发送密码重置邮件
    if settings.SMTP_HOST:
        await send_reset_password_email(
            email_to=user.email,
            username=user.username,
            token=reset_token
        )
    
    # 记录密码重置请求活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="password_reset_requested",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "如果该邮箱地址存在，您将收到密码重置邮件"}


@router.post("/password-reset")
async def reset_password(
    request: Request,
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
) -> Any:
    """
    重置密码
    """
    try:
        payload = verify_token(password_reset.token)
        email = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的重置令牌"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效或已过期的重置令牌"
        )
    
    user = user_crud.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新密码
    hashed_password = get_password_hash(password_reset.new_password)
    user_crud.update_password(db, user_id=user.id, hashed_password=hashed_password)
    
    # 记录密码重置活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="password_reset_completed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "密码重置成功"}


@router.post("/change-password")
async def change_password(
    request: Request,
    password_change: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    修改密码
    """
    # 验证当前密码
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 更新密码
    hashed_password = get_password_hash(password_change.new_password)
    user_crud.update_password(db, user_id=current_user.id, hashed_password=hashed_password)
    
    # 记录密码修改活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="password_changed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "密码修改成功"}


@router.post("/verify-email")
async def verify_email(
    request: Request,
    email_verification: EmailVerification,
    db: Session = Depends(get_db)
) -> Any:
    """
    验证邮箱地址
    """
    try:
        payload = verify_token(email_verification.token)
        email = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的验证令牌"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效或已过期的验证令牌"
        )
    
    user = user_crud.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.is_email_verified:
        return {"message": "邮箱已经验证过了"}
    
    # 更新邮箱验证状态
    user_crud.verify_email(db, user_id=user.id)
    
    # 记录邮箱验证活动
    await log_user_activity(
        db=db,
        user_id=user.id,
        action="email_verified",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "邮箱验证成功"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取当前用户信息
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    request: Request,
    user_update: UserProfile,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新当前用户信息
    """
    user = user_crud.update(db, db_obj=current_user, obj_in=user_update)
    
    # 记录用户信息更新活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="profile_updated",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return UserResponse.from_orm(user)


@router.get("/csrf-token", response_model=CSRFToken)
async def get_csrf_token() -> Any:
    """
    获取CSRF令牌
    """
    csrf_token = generate_csrf_token()
    return {"csrf_token": csrf_token}


@router.get("/permissions")
async def get_user_permissions(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取当前用户权限
    """
    permissions = permission_manager.get_user_permissions(current_user)
    return {"permissions": list(permissions)}