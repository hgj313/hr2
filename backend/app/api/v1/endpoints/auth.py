"""认证相关API端点

本模块实现了用户认证相关的API端点，包括登录、注册、令牌刷新、密码重置等功能。
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import SecurityManager, get_current_user, get_current_active_user
from app.models.auth import User, LoginAttempt
from app.schemas.auth import (
    UserCreate,
    UserRegister,
    UserResponse,
    TokenResponse,
    TokenRefreshRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest,
    EmailVerificationRequest,
    EmailVerificationConfirm
)
from app.schemas.base import MessageResponse, SuccessResponse
from app.services.auth import AuthService
from app.services.email import EmailService

# 获取配置
settings = get_settings()

# 创建路由器
router = APIRouter()

# 初始化服务
security_manager = SecurityManager()
auth_service = AuthService()
email_service = EmailService()


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """用户登录
    
    Args:
        form_data: 登录表单数据（用户名和密码）
        db: 数据库会话
    
    Returns:
        TokenResponse: 包含访问令牌和刷新令牌的响应
    
    Raises:
        HTTPException: 当用户名或密码错误时抛出401异常
    """
    try:
        # 验证用户凭据
        user = await auth_service.authenticate_user(
            db, form_data.username, form_data.password
        )
        
        if not user:
            # 记录登录失败尝试
            await auth_service.record_login_attempt(
                db, form_data.username, success=False
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否被禁用
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已被禁用"
            )
        
        # 生成访问令牌和刷新令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = security_manager.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        refresh_token = security_manager.create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires
        )
        
        # 记录登录成功
        await auth_service.record_login_attempt(
            db, form_data.username, success=True, user_id=user.id
        )
        
        # 创建用户会话
        await auth_service.create_user_session(
            db, user.id, access_token, refresh_token
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误"
        )


@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(
    user_data: UserRegister,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """用户注册
    
    Args:
        user_data: 用户注册数据
        background_tasks: 后台任务
        db: 数据库会话
    
    Returns:
        UserResponse: 创建的用户信息
    
    Raises:
        HTTPException: 当用户名或邮箱已存在时抛出400异常
    """
    try:
        # 检查用户名是否已存在
        existing_user = await auth_service.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        existing_email = await auth_service.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建用户
        user = await auth_service.create_user(db, user_data)
        
        # 发送邮箱验证邮件
        if settings.EMAIL_VERIFICATION_ENABLED:
            verification_token = security_manager.create_email_verification_token(
                data={"email": user.email}
            )
            
            background_tasks.add_task(
                email_service.send_verification_email,
                user.email,
                user.full_name or user.username,
                verification_token
            )
        
        return UserResponse.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程中发生错误"
        )


@router.post("/refresh", response_model=TokenResponse, summary="刷新令牌")
async def refresh_token(
    token_data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """刷新访问令牌
    
    Args:
        token_data: 刷新令牌请求数据
        db: 数据库会话
    
    Returns:
        TokenResponse: 新的访问令牌和刷新令牌
    
    Raises:
        HTTPException: 当刷新令牌无效时抛出401异常
    """
    try:
        # 验证刷新令牌
        payload = security_manager.verify_refresh_token(token_data.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的令牌载荷"
            )
        
        # 获取用户信息
        user = await auth_service.get_user_by_id(db, int(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        # 生成新的令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        new_access_token = security_manager.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        new_refresh_token = security_manager.create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires
        )
        
        # 更新用户会话
        await auth_service.update_user_session(
            db, user.id, new_access_token, new_refresh_token
        )
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="令牌刷新过程中发生错误"
        )


@router.post("/logout", response_model=MessageResponse, summary="用户登出")
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """用户登出
    
    Args:
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 登出成功消息
    """
    try:
        # 删除用户会话
        await auth_service.delete_user_session(db, current_user.id)
        
        return MessageResponse(message="登出成功")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出过程中发生错误"
        )


@router.post("/password-reset", response_model=MessageResponse, summary="请求密码重置")
async def request_password_reset(
    request_data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """请求密码重置
    
    Args:
        request_data: 密码重置请求数据
        background_tasks: 后台任务
        db: 数据库会话
    
    Returns:
        MessageResponse: 请求处理结果消息
    """
    try:
        # 查找用户
        user = await auth_service.get_user_by_email(db, request_data.email)
        if not user:
            # 为了安全考虑，即使用户不存在也返回成功消息
            return MessageResponse(message="如果邮箱存在，重置链接已发送")
        
        # 生成密码重置令牌
        reset_token = security_manager.create_password_reset_token(
            data={"email": user.email}
        )
        
        # 保存重置令牌到数据库
        await auth_service.create_password_reset_token(db, user.id, reset_token)
        
        # 发送密码重置邮件
        background_tasks.add_task(
            email_service.send_password_reset_email,
            user.email,
            user.full_name or user.username,
            reset_token
        )
        
        return MessageResponse(message="如果邮箱存在，重置链接已发送")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置请求处理过程中发生错误"
        )


@router.post("/password-reset/confirm", response_model=MessageResponse, summary="确认密码重置")
async def confirm_password_reset(
    confirm_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """确认密码重置
    
    Args:
        confirm_data: 密码重置确认数据
        db: 数据库会话
    
    Returns:
        MessageResponse: 重置结果消息
    
    Raises:
        HTTPException: 当令牌无效或已过期时抛出400异常
    """
    try:
        # 验证重置令牌
        payload = security_manager.verify_password_reset_token(confirm_data.token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效或已过期的重置令牌"
            )
        
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的令牌载荷"
            )
        
        # 查找用户
        user = await auth_service.get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户不存在"
            )
        
        # 验证数据库中的重置令牌
        if not await auth_service.verify_password_reset_token(db, user.id, confirm_data.token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效或已使用的重置令牌"
            )
        
        # 更新密码
        await auth_service.update_user_password(db, user.id, confirm_data.new_password)
        
        # 删除重置令牌
        await auth_service.delete_password_reset_token(db, user.id, confirm_data.token)
        
        # 删除所有用户会话（强制重新登录）
        await auth_service.delete_all_user_sessions(db, user.id)
        
        return MessageResponse(message="密码重置成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置过程中发生错误"
        )


@router.post("/change-password", response_model=MessageResponse, summary="修改密码")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """修改密码
    
    Args:
        password_data: 密码修改数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 修改结果消息
    
    Raises:
        HTTPException: 当当前密码错误时抛出400异常
    """
    try:
        # 验证当前密码
        if not security_manager.verify_password(
            password_data.current_password, current_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        # 更新密码
        await auth_service.update_user_password(
            db, current_user.id, password_data.new_password
        )
        
        return MessageResponse(message="密码修改成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码修改过程中发生错误"
        )


@router.post("/verify-email", response_model=MessageResponse, summary="请求邮箱验证")
async def request_email_verification(
    request_data: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """请求邮箱验证
    
    Args:
        request_data: 邮箱验证请求数据
        background_tasks: 后台任务
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 请求处理结果消息
    """
    try:
        # 检查邮箱是否已被其他用户使用
        existing_user = await auth_service.get_user_by_email(db, request_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被其他用户使用"
            )
        
        # 生成邮箱验证令牌
        verification_token = security_manager.create_email_verification_token(
            data={"email": request_data.email, "user_id": current_user.id}
        )
        
        # 保存验证令牌到数据库
        await auth_service.create_email_verification_token(
            db, current_user.id, request_data.email, verification_token
        )
        
        # 发送验证邮件
        background_tasks.add_task(
            email_service.send_verification_email,
            request_data.email,
            current_user.full_name or current_user.username,
            verification_token
        )
        
        return MessageResponse(message="验证邮件已发送")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="邮箱验证请求处理过程中发生错误"
        )


@router.post("/verify-email/confirm", response_model=MessageResponse, summary="确认邮箱验证")
async def confirm_email_verification(
    confirm_data: EmailVerificationConfirm,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """确认邮箱验证
    
    Args:
        confirm_data: 邮箱验证确认数据
        db: 数据库会话
    
    Returns:
        MessageResponse: 验证结果消息
    
    Raises:
        HTTPException: 当令牌无效或已过期时抛出400异常
    """
    try:
        # 验证邮箱验证令牌
        payload = security_manager.verify_email_verification_token(confirm_data.token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效或已过期的验证令牌"
            )
        
        email = payload.get("email")
        user_id = payload.get("user_id")
        
        if not email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的令牌载荷"
            )
        
        # 验证数据库中的验证令牌
        if not await auth_service.verify_email_verification_token(
            db, user_id, email, confirm_data.token
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效或已使用的验证令牌"
            )
        
        # 更新用户邮箱验证状态
        await auth_service.verify_user_email(db, user_id, email)
        
        # 删除验证令牌
        await auth_service.delete_email_verification_token(db, user_id, confirm_data.token)
        
        return MessageResponse(message="邮箱验证成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="邮箱验证过程中发生错误"
        )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取当前用户信息
    
    Args:
        current_user: 当前用户
    
    Returns:
        UserResponse: 当前用户信息
    """
    return UserResponse.model_validate(current_user)