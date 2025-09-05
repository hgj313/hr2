"""组织架构管理API端点

本模块实现了组织架构管理相关的API端点，包括部门、职位、人员、工作地点等的管理功能。
"""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user, check_permissions
from app.models.auth import User
from app.schemas.organization import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    PositionCreate,
    PositionUpdate,
    PositionResponse,
    PersonnelCreate,
    PersonnelUpdate,
    PersonnelResponse,
    PersonnelDetailResponse,
    WorkLocationCreate,
    WorkLocationUpdate,
    WorkLocationResponse,
    PersonnelHistoryResponse
)
from app.schemas.base import (
    PaginatedResponse,
    MessageResponse,
    BulkOperationRequest,
    BulkOperationResponse
)
from app.services.organization import OrganizationService

# 创建路由器
router = APIRouter()

# 初始化服务
org_service = OrganizationService()


# ==================== 部门管理 ====================

@router.get("/departments", response_model=PaginatedResponse[DepartmentResponse], summary="获取部门列表")
async def get_departments(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    parent_id: Optional[UUID] = Query(None, description="父部门ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取部门列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（部门名称、描述）
        parent_id: 父部门ID过滤
        is_active: 激活状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[DepartmentResponse]: 分页的部门列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:read"], db)
        
        # 构建过滤条件
        filters = {}
        if parent_id:
            filters["parent_id"] = parent_id
        if is_active is not None:
            filters["is_active"] = is_active
        
        # 获取部门列表
        departments, total = await org_service.get_departments(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[DepartmentResponse.model_validate(dept) for dept in departments],
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
            detail="获取部门列表时发生错误"
        )


@router.get("/departments/tree", response_model=List[DepartmentResponse], summary="获取部门树结构")
async def get_department_tree(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取部门树结构
    
    Args:
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[DepartmentResponse]: 部门树结构
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:read"], db)
        
        # 获取部门树
        department_tree = await org_service.get_department_tree(db)
        
        return [DepartmentResponse.model_validate(dept) for dept in department_tree]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取部门树结构时发生错误"
        )


@router.get("/departments/{department_id}", response_model=DepartmentResponse, summary="获取部门详情")
async def get_department(
    department_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取部门详情
    
    Args:
        department_id: 部门ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        DepartmentResponse: 部门详情
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:read"], db)
        
        # 获取部门信息
        department = await org_service.get_department_by_id(db, department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        return DepartmentResponse.model_validate(department)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取部门详情时发生错误"
        )


@router.post("/departments", response_model=DepartmentResponse, summary="创建部门")
async def create_department(
    department_data: DepartmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建部门
    
    Args:
        department_data: 部门创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        DepartmentResponse: 创建的部门信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:create"], db)
        
        # 创建部门
        department = await org_service.create_department(db, department_data)
        
        return DepartmentResponse.model_validate(department)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建部门时发生错误"
        )


@router.put("/departments/{department_id}", response_model=DepartmentResponse, summary="更新部门")
async def update_department(
    department_id: UUID,
    department_data: DepartmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新部门
    
    Args:
        department_id: 部门ID
        department_data: 部门更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        DepartmentResponse: 更新后的部门信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:update"], db)
        
        # 更新部门
        department = await org_service.update_department(db, department_id, department_data)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        return DepartmentResponse.model_validate(department)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新部门时发生错误"
        )


@router.delete("/departments/{department_id}", response_model=MessageResponse, summary="删除部门")
async def delete_department(
    department_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除部门
    
    Args:
        department_id: 部门ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["department:delete"], db)
        
        # 删除部门
        success = await org_service.delete_department(db, department_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在或无法删除（存在子部门或人员）"
            )
        
        return MessageResponse(message="部门删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除部门时发生错误"
        )


# ==================== 职位管理 ====================

@router.get("/positions", response_model=PaginatedResponse[PositionResponse], summary="获取职位列表")
async def get_positions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    level: Optional[str] = Query(None, description="职位级别"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取职位列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（职位名称、描述）
        department_id: 部门ID过滤
        level: 职位级别过滤
        is_active: 激活状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[PositionResponse]: 分页的职位列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["position:read"], db)
        
        # 构建过滤条件
        filters = {}
        if department_id:
            filters["department_id"] = department_id
        if level:
            filters["level"] = level
        if is_active is not None:
            filters["is_active"] = is_active
        
        # 获取职位列表
        positions, total = await org_service.get_positions(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[PositionResponse.model_validate(pos) for pos in positions],
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
            detail="获取职位列表时发生错误"
        )


@router.get("/positions/{position_id}", response_model=PositionResponse, summary="获取职位详情")
async def get_position(
    position_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取职位详情
    
    Args:
        position_id: 职位ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PositionResponse: 职位详情
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["position:read"], db)
        
        # 获取职位信息
        position = await org_service.get_position_by_id(db, position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="职位不存在"
            )
        
        return PositionResponse.model_validate(position)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取职位详情时发生错误"
        )


@router.post("/positions", response_model=PositionResponse, summary="创建职位")
async def create_position(
    position_data: PositionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建职位
    
    Args:
        position_data: 职位创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PositionResponse: 创建的职位信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["position:create"], db)
        
        # 创建职位
        position = await org_service.create_position(db, position_data)
        
        return PositionResponse.model_validate(position)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建职位时发生错误"
        )


@router.put("/positions/{position_id}", response_model=PositionResponse, summary="更新职位")
async def update_position(
    position_id: UUID,
    position_data: PositionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新职位
    
    Args:
        position_id: 职位ID
        position_data: 职位更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PositionResponse: 更新后的职位信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["position:update"], db)
        
        # 更新职位
        position = await org_service.update_position(db, position_id, position_data)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="职位不存在"
            )
        
        return PositionResponse.model_validate(position)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新职位时发生错误"
        )


@router.delete("/positions/{position_id}", response_model=MessageResponse, summary="删除职位")
async def delete_position(
    position_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除职位
    
    Args:
        position_id: 职位ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["position:delete"], db)
        
        # 删除职位
        success = await org_service.delete_position(db, position_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="职位不存在或无法删除（存在关联人员）"
            )
        
        return MessageResponse(message="职位删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除职位时发生错误"
        )


# ==================== 人员管理 ====================

@router.get("/personnel", response_model=PaginatedResponse[PersonnelResponse], summary="获取人员列表")
async def get_personnel(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    position_id: Optional[UUID] = Query(None, description="职位ID"),
    status: Optional[str] = Query(None, description="人员状态"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取人员列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（姓名、工号、邮箱）
        department_id: 部门ID过滤
        position_id: 职位ID过滤
        status: 人员状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[PersonnelResponse]: 分页的人员列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:read"], db)
        
        # 构建过滤条件
        filters = {}
        if department_id:
            filters["department_id"] = department_id
        if position_id:
            filters["position_id"] = position_id
        if status:
            filters["status"] = status
        
        # 获取人员列表
        personnel, total = await org_service.get_personnel(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[PersonnelResponse.model_validate(person) for person in personnel],
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
            detail="获取人员列表时发生错误"
        )


@router.get("/personnel/{personnel_id}", response_model=PersonnelDetailResponse, summary="获取人员详情")
async def get_personnel_detail(
    personnel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取人员详情
    
    Args:
        personnel_id: 人员ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PersonnelDetailResponse: 人员详情
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:read"], db)
        
        # 获取人员信息
        personnel = await org_service.get_personnel_by_id(db, personnel_id)
        if not personnel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="人员不存在"
            )
        
        return PersonnelDetailResponse.model_validate(personnel)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取人员详情时发生错误"
        )


@router.post("/personnel", response_model=PersonnelResponse, summary="创建人员")
async def create_personnel(
    personnel_data: PersonnelCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建人员
    
    Args:
        personnel_data: 人员创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PersonnelResponse: 创建的人员信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:create"], db)
        
        # 创建人员
        personnel = await org_service.create_personnel(db, personnel_data)
        
        return PersonnelResponse.model_validate(personnel)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建人员时发生错误"
        )


@router.put("/personnel/{personnel_id}", response_model=PersonnelResponse, summary="更新人员")
async def update_personnel(
    personnel_id: UUID,
    personnel_data: PersonnelUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新人员
    
    Args:
        personnel_id: 人员ID
        personnel_data: 人员更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PersonnelResponse: 更新后的人员信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:update"], db)
        
        # 更新人员
        personnel = await org_service.update_personnel(db, personnel_id, personnel_data)
        if not personnel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="人员不存在"
            )
        
        return PersonnelResponse.model_validate(personnel)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新人员时发生错误"
        )


@router.delete("/personnel/{personnel_id}", response_model=MessageResponse, summary="删除人员")
async def delete_personnel(
    personnel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除人员
    
    Args:
        personnel_id: 人员ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:delete"], db)
        
        # 删除人员
        success = await org_service.delete_personnel(db, personnel_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="人员不存在"
            )
        
        return MessageResponse(message="人员删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除人员时发生错误"
        )


@router.get("/personnel/{personnel_id}/history", response_model=List[PersonnelHistoryResponse], summary="获取人员变更历史")
async def get_personnel_history(
    personnel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取人员变更历史
    
    Args:
        personnel_id: 人员ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[PersonnelHistoryResponse]: 人员变更历史列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["personnel:read"], db)
        
        # 获取人员变更历史
        history = await org_service.get_personnel_history(db, personnel_id)
        
        return [PersonnelHistoryResponse.model_validate(h) for h in history]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取人员变更历史时发生错误"
        )


# ==================== 工作地点管理 ====================

@router.get("/work-locations", response_model=PaginatedResponse[WorkLocationResponse], summary="获取工作地点列表")
async def get_work_locations(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取工作地点列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（地点名称、地址）
        is_active: 激活状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[WorkLocationResponse]: 分页的工作地点列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["work_location:read"], db)
        
        # 构建过滤条件
        filters = {}
        if is_active is not None:
            filters["is_active"] = is_active
        
        # 获取工作地点列表
        locations, total = await org_service.get_work_locations(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[WorkLocationResponse.model_validate(loc) for loc in locations],
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
            detail="获取工作地点列表时发生错误"
        )


@router.post("/work-locations", response_model=WorkLocationResponse, summary="创建工作地点")
async def create_work_location(
    location_data: WorkLocationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建工作地点
    
    Args:
        location_data: 工作地点创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        WorkLocationResponse: 创建的工作地点信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["work_location:create"], db)
        
        # 创建工作地点
        location = await org_service.create_work_location(db, location_data)
        
        return WorkLocationResponse.model_validate(location)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建工作地点时发生错误"
        )


@router.put("/work-locations/{location_id}", response_model=WorkLocationResponse, summary="更新工作地点")
async def update_work_location(
    location_id: UUID,
    location_data: WorkLocationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新工作地点
    
    Args:
        location_id: 工作地点ID
        location_data: 工作地点更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        WorkLocationResponse: 更新后的工作地点信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["work_location:update"], db)
        
        # 更新工作地点
        location = await org_service.update_work_location(db, location_id, location_data)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="工作地点不存在"
            )
        
        return WorkLocationResponse.model_validate(location)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新工作地点时发生错误"
        )


@router.delete("/work-locations/{location_id}", response_model=MessageResponse, summary="删除工作地点")
async def delete_work_location(
    location_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除工作地点
    
    Args:
        location_id: 工作地点ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["work_location:delete"], db)
        
        # 删除工作地点
        success = await org_service.delete_work_location(db, location_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="工作地点不存在或无法删除（存在关联人员）"
            )
        
        return MessageResponse(message="工作地点删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除工作地点时发生错误"
        )