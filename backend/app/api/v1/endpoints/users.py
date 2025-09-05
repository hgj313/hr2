"""用户管理API端点

本模块实现了用户管理相关的API端点，包括用户的创建、查询、更新、删除等功能。
"""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user, check_permissions
from app.models.auth import User
from app.schemas.auth import (
    UserCreate,
    UserUpdate,
    UserResponse,
    RoleResponse,
    ApiKeyCreate,
    ApiKeyResponse
)
from app.schemas.base import (
    PaginatedResponse,
    MessageResponse,
    BulkOperationRequest,
    BulkOperationResponse
)
from app.services.user import UserService
from app.services.role import RoleService

# 创建路由器
router = APIRouter()

# 初始化服务
user_service = UserService()
role_service = RoleService()


@router.get("/", response_model=PaginatedResponse[UserResponse], summary="获取用户列表")
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    role_id: Optional[UUID] = Query(None, description="角色ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取用户列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（用户名、邮箱、姓名）
        department_id: 部门ID过滤
        role_id: 角色ID过滤
        is_active: 激活状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[UserResponse]: 分页的用户列表
    
    Raises:
        HTTPException: 当权限不足时抛出403异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:read"], db)
        
        # 构建过滤条件
        filters = {}
        if department_id:
            filters["department_id"] = department_id
        if role_id:
            filters["role_id"] = role_id
        if is_active is not None:
            filters["is_active"] = is_active
        
        # 获取用户列表
        users, total = await user_service.get_users(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表时发生错误"
        )


@router.get("/{user_id}", response_model=UserResponse, summary="获取用户详情")
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取用户详情
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        UserResponse: 用户详情
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限（可以查看自己的信息或有用户读取权限）
        if current_user.id != user_id:
            await check_permissions(current_user, ["user:read"], db)
        
        # 获取用户信息
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return UserResponse.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户详情时发生错误"
        )


@router.post("/", response_model=UserResponse, summary="创建用户")
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建用户
    
    Args:
        user_data: 用户创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        UserResponse: 创建的用户信息
    
    Raises:
        HTTPException: 当权限不足或用户已存在时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:create"], db)
        
        # 检查用户名是否已存在
        existing_user = await user_service.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        existing_email = await user_service.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建用户
        user = await user_service.create_user(db, user_data)
        
        return UserResponse.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建用户时发生错误"
        )


@router.put("/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新用户
    
    Args:
        user_id: 用户ID
        user_data: 用户更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        UserResponse: 更新后的用户信息
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限（可以更新自己的信息或有用户更新权限）
        if current_user.id != user_id:
            await check_permissions(current_user, ["user:update"], db)
        
        # 检查用户是否存在
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 如果更新邮箱，检查是否已被其他用户使用
        if user_data.email and user_data.email != user.email:
            existing_email = await user_service.get_user_by_email(db, user_data.email)
            if existing_email and existing_email.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被其他用户使用"
                )
        
        # 更新用户
        updated_user = await user_service.update_user(db, user_id, user_data)
        
        return UserResponse.model_validate(updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户时发生错误"
        )


@router.delete("/{user_id}", response_model=MessageResponse, summary="删除用户")
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除用户
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:delete"], db)
        
        # 不能删除自己
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除自己的账户"
            )
        
        # 检查用户是否存在
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 删除用户
        await user_service.delete_user(db, user_id)
        
        return MessageResponse(message="用户删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户时发生错误"
        )


@router.post("/bulk-delete", response_model=BulkOperationResponse, summary="批量删除用户")
async def bulk_delete_users(
    request_data: BulkOperationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """批量删除用户
    
    Args:
        request_data: 批量操作请求数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        BulkOperationResponse: 批量操作结果
    
    Raises:
        HTTPException: 当权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:delete"], db)
        
        # 过滤掉当前用户ID（不能删除自己）
        user_ids = [uid for uid in request_data.ids if uid != current_user.id]
        
        if not user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有有效的用户ID可以删除"
            )
        
        # 批量删除用户
        success_count, failed_count, errors = await user_service.bulk_delete_users(
            db, user_ids
        )
        
        return BulkOperationResponse(
            success_count=success_count,
            failed_count=failed_count,
            errors=errors
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="批量删除用户时发生错误"
        )


@router.post("/{user_id}/activate", response_model=MessageResponse, summary="激活用户")
async def activate_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """激活用户
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 激活结果消息
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:update"], db)
        
        # 激活用户
        success = await user_service.activate_user(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return MessageResponse(message="用户激活成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="激活用户时发生错误"
        )


@router.post("/{user_id}/deactivate", response_model=MessageResponse, summary="停用用户")
async def deactivate_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """停用用户
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 停用结果消息
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:update"], db)
        
        # 不能停用自己
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能停用自己的账户"
            )
        
        # 停用用户
        success = await user_service.deactivate_user(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return MessageResponse(message="用户停用成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="停用用户时发生错误"
        )


@router.get("/{user_id}/roles", response_model=List[RoleResponse], summary="获取用户角色")
async def get_user_roles(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取用户角色
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[RoleResponse]: 用户角色列表
    
    Raises:
        HTTPException: 当用户不存在或权限不足时抛出异常
    """
    try:
        # 检查权限（可以查看自己的角色或有用户读取权限）
        if current_user.id != user_id:
            await check_permissions(current_user, ["user:read"], db)
        
        # 获取用户角色
        roles = await role_service.get_user_roles(db, user_id)
        
        return [RoleResponse.model_validate(role) for role in roles]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户角色时发生错误"
        )


@router.post("/{user_id}/roles/{role_id}", response_model=MessageResponse, summary="分配角色")
async def assign_role(
    user_id: UUID,
    role_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """分配角色给用户
    
    Args:
        user_id: 用户ID
        role_id: 角色ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 分配结果消息
    
    Raises:
        HTTPException: 当用户或角色不存在或权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:update", "role:assign"], db)
        
        # 分配角色
        success = await role_service.assign_role_to_user(db, user_id, role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色分配失败，用户或角色不存在，或角色已分配"
            )
        
        return MessageResponse(message="角色分配成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="分配角色时发生错误"
        )


@router.delete("/{user_id}/roles/{role_id}", response_model=MessageResponse, summary="移除角色")
async def remove_role(
    user_id: UUID,
    role_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """从用户移除角色
    
    Args:
        user_id: 用户ID
        role_id: 角色ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 移除结果消息
    
    Raises:
        HTTPException: 当权限不足时抛出异常
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["user:update", "role:assign"], db)
        
        # 移除角色
        success = await role_service.remove_role_from_user(db, user_id, role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色移除失败，用户或角色不存在，或角色未分配"
            )
        
        return MessageResponse(message="角色移除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="移除角色时发生错误"
        )


@router.get("/{user_id}/api-keys", response_model=List[ApiKeyResponse], summary="获取用户API密钥")
async def get_user_api_keys(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取用户API密钥
    
    Args:
        user_id: 用户ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ApiKeyResponse]: API密钥列表
    
    Raises:
        HTTPException: 当权限不足时抛出异常
    """
    try:
        # 检查权限（只能查看自己的API密钥或有管理权限）
        if current_user.id != user_id:
            await check_permissions(current_user, ["api_key:read"], db)
        
        # 获取API密钥
        api_keys = await user_service.get_user_api_keys(db, user_id)
        
        return [ApiKeyResponse.model_validate(key) for key in api_keys]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取API密钥时发生错误"
        )


@router.post("/{user_id}/api-keys", response_model=ApiKeyResponse, summary="创建API密钥")
async def create_api_key(
    user_id: UUID,
    api_key_data: ApiKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建API密钥
    
    Args:
        user_id: 用户ID
        api_key_data: API密钥创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ApiKeyResponse: 创建的API密钥信息
    
    Raises:
        HTTPException: 当权限不足时抛出异常
    """
    try:
        # 检查权限（只能为自己创建API密钥或有管理权限）
        if current_user.id != user_id:
            await check_permissions(current_user, ["api_key:create"], db)
        
        # 创建API密钥
        api_key = await user_service.create_api_key(db, user_id, api_key_data)
        
        return ApiKeyResponse.model_validate(api_key)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建API密钥时发生错误"
        )