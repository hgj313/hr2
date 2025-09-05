from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import (
    get_db, get_current_active_user, get_current_superuser,
    CommonQueryParams, get_pagination_params
)
from app.core.permissions import require_permissions, PermissionType
from app.models.auth import User
from app.schemas.auth import (
    UserResponse, UserCreate, UserUpdate, UserSearch,
    UserListResponse, UserStats
)
from app.crud.auth import user_crud
from app.utils.audit import log_user_activity
from app.utils.pagination import paginate

router = APIRouter()


@router.get("/", response_model=UserListResponse)
@require_permissions([PermissionType.USER_READ])
async def get_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="搜索用户名或邮箱"),
    department_id: Optional[int] = Query(None, description="部门ID筛选"),
    role: Optional[str] = Query(None, description="角色筛选"),
    is_active: Optional[bool] = Query(None, description="激活状态筛选"),
    is_email_verified: Optional[bool] = Query(None, description="邮箱验证状态筛选")
) -> Any:
    """
    获取用户列表
    """
    # 构建筛选条件
    filters = {}
    if search:
        filters["search"] = search
    if department_id:
        filters["department_id"] = department_id
    if role:
        filters["role"] = role
    if is_active is not None:
        filters["is_active"] = is_active
    if is_email_verified is not None:
        filters["is_email_verified"] = is_email_verified
    
    # 获取用户列表
    users, total = user_crud.get_multi_with_filters(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters=filters
    )
    
    # 记录查看用户列表活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="users_list_viewed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"filters": filters}
    )
    
    return {
        "users": [UserResponse.from_orm(user) for user in users],
        "total": total,
        "page": pagination["page"],
        "size": pagination["size"],
        "pages": (total + pagination["size"] - 1) // pagination["size"]
    }


@router.get("/stats", response_model=UserStats)
@require_permissions([PermissionType.USER_READ])
async def get_user_stats(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取用户统计信息
    """
    stats = user_crud.get_user_stats(db)
    
    # 记录查看用户统计活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_stats_viewed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return stats


@router.get("/{user_id}", response_model=UserResponse)
@require_permissions([PermissionType.USER_READ])
async def get_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取指定用户信息
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 记录查看用户详情活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_detail_viewed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"target_user_id": user_id}
    )
    
    return UserResponse.from_orm(user)


@router.post("/", response_model=UserResponse)
@require_permissions([PermissionType.USER_CREATE])
async def create_user(
    request: Request,
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    创建新用户
    """
    # 检查邮箱是否已存在
    existing_user = user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱地址已被使用"
        )
    
    # 检查用户名是否已存在
    existing_user = user_crud.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用"
        )
    
    # 创建用户
    user = user_crud.create(db, obj_in=user_in)
    
    # 记录创建用户活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_created",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"created_user_id": user.id, "created_user_email": user.email}
    )
    
    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
@require_permissions([PermissionType.USER_UPDATE])
async def update_user(
    request: Request,
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    更新用户信息
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 如果更新邮箱，检查是否已被其他用户使用
    if user_in.email and user_in.email != user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱地址已被其他用户使用"
            )
    
    # 如果更新用户名，检查是否已被其他用户使用
    if user_in.username and user_in.username != user.username:
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被其他用户使用"
            )
    
    # 更新用户
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    
    # 记录更新用户活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_updated",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"updated_user_id": user_id}
    )
    
    return UserResponse.from_orm(user)


@router.delete("/{user_id}")
@require_permissions([PermissionType.USER_DELETE])
async def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    删除用户
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不能删除自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账户"
        )
    
    # 软删除用户
    user_crud.remove(db, id=user_id)
    
    # 记录删除用户活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_deleted",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"deleted_user_id": user_id, "deleted_user_email": user.email}
    )
    
    return {"message": "用户删除成功"}


@router.post("/{user_id}/activate")
@require_permissions([PermissionType.USER_UPDATE])
async def activate_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    激活用户
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已经是激活状态"
        )
    
    # 激活用户
    user_crud.activate(db, user_id=user_id)
    
    # 记录激活用户活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_activated",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"activated_user_id": user_id}
    )
    
    return {"message": "用户激活成功"}


@router.post("/{user_id}/deactivate")
@require_permissions([PermissionType.USER_UPDATE])
async def deactivate_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    停用用户
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不能停用自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的账户"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已经是停用状态"
        )
    
    # 停用用户
    user_crud.deactivate(db, user_id=user_id)
    
    # 记录停用用户活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_deactivated",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"deactivated_user_id": user_id}
    )
    
    return {"message": "用户停用成功"}


@router.post("/{user_id}/reset-password")
@require_permissions([PermissionType.USER_UPDATE])
async def admin_reset_password(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    管理员重置用户密码
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 生成临时密码
    temp_password = user_crud.generate_temp_password()
    user_crud.update_password(db, user_id=user_id, password=temp_password)
    
    # 记录管理员重置密码活动
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="admin_password_reset",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"target_user_id": user_id}
    )
    
    return {
        "message": "密码重置成功",
        "temp_password": temp_password,
        "note": "请通知用户尽快修改密码"
    }


@router.get("/{user_id}/activity")
@require_permissions([PermissionType.USER_READ])
async def get_user_activity(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params),
    action: Optional[str] = Query(None, description="活动类型筛选")
) -> Any:
    """
    获取用户活动记录
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取用户活动记录
    activities, total = user_crud.get_user_activities(
        db,
        user_id=user_id,
        skip=pagination["skip"],
        limit=pagination["limit"],
        action=action
    )
    
    # 记录查看用户活动记录
    await log_user_activity(
        db=db,
        user_id=current_user.id,
        action="user_activity_viewed",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details={"target_user_id": user_id}
    )
    
    return {
        "activities": activities,
        "total": total,
        "page": pagination["page"],
        "size": pagination["size"],
        "pages": (total + pagination["size"] - 1) // pagination["size"]
    }