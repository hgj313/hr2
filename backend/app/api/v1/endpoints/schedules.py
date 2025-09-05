"""调度管理API端点

本模块实现了调度管理相关的API端点，包括调度计划、调度分配、冲突检测、模板管理等功能。
"""

from typing import Any, List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user, check_permissions
from app.models.auth import User
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ScheduleDetailResponse,
    ScheduleAssignmentCreate,
    ScheduleAssignmentUpdate,
    ScheduleAssignmentResponse,
    ScheduleConflictResponse,
    ScheduleTemplateCreate,
    ScheduleTemplateUpdate,
    ScheduleTemplateResponse,
    ResourceAvailabilityCreate,
    ResourceAvailabilityUpdate,
    ResourceAvailabilityResponse,
    WorkloadAnalysisResponse
)
from app.schemas.base import (
    PaginatedResponse,
    MessageResponse,
    BulkOperationRequest,
    BulkOperationResponse
)
from app.services.schedule import ScheduleService

# 创建路由器
router = APIRouter()

# 初始化服务
schedule_service = ScheduleService()


# ==================== 调度计划管理 ====================

@router.get("/schedules", response_model=PaginatedResponse[ScheduleResponse], summary="获取调度计划列表")
async def get_schedules(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="调度状态"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取调度计划列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（调度名称、描述）
        status: 调度状态过滤
        start_date: 开始日期过滤
        end_date: 结束日期过滤
        department_id: 部门ID过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[ScheduleResponse]: 分页的调度计划列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 构建过滤条件
        filters = {}
        if status:
            filters["status"] = status
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        if department_id:
            filters["department_id"] = department_id
        
        # 获取调度计划列表
        schedules, total = await schedule_service.get_schedules(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[ScheduleResponse.model_validate(schedule) for schedule in schedules],
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
            detail="获取调度计划列表时发生错误"
        )


@router.get("/schedules/{schedule_id}", response_model=ScheduleDetailResponse, summary="获取调度计划详情")
async def get_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取调度计划详情
    
    Args:
        schedule_id: 调度计划ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleDetailResponse: 调度计划详情
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 获取调度计划信息
        schedule = await schedule_service.get_schedule_by_id(db, schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度计划不存在"
            )
        
        return ScheduleDetailResponse.model_validate(schedule)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调度计划详情时发生错误"
        )


@router.post("/schedules", response_model=ScheduleResponse, summary="创建调度计划")
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建调度计划
    
    Args:
        schedule_data: 调度计划创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleResponse: 创建的调度计划信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:create"], db)
        
        # 创建调度计划
        schedule = await schedule_service.create_schedule(db, schedule_data, current_user.id)
        
        return ScheduleResponse.model_validate(schedule)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建调度计划时发生错误"
        )


@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse, summary="更新调度计划")
async def update_schedule(
    schedule_id: UUID,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新调度计划
    
    Args:
        schedule_id: 调度计划ID
        schedule_data: 调度计划更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleResponse: 更新后的调度计划信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 更新调度计划
        schedule = await schedule_service.update_schedule(db, schedule_id, schedule_data)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度计划不存在"
            )
        
        return ScheduleResponse.model_validate(schedule)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新调度计划时发生错误"
        )


@router.delete("/schedules/{schedule_id}", response_model=MessageResponse, summary="删除调度计划")
async def delete_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除调度计划
    
    Args:
        schedule_id: 调度计划ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:delete"], db)
        
        # 删除调度计划
        success = await schedule_service.delete_schedule(db, schedule_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度计划不存在"
            )
        
        return MessageResponse(message="调度计划删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除调度计划时发生错误"
        )


# ==================== 调度分配管理 ====================

@router.get("/schedules/{schedule_id}/assignments", response_model=List[ScheduleAssignmentResponse], summary="获取调度分配列表")
async def get_schedule_assignments(
    schedule_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取调度分配列表
    
    Args:
        schedule_id: 调度计划ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ScheduleAssignmentResponse]: 调度分配列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 获取调度分配列表
        assignments = await schedule_service.get_schedule_assignments(db, schedule_id)
        
        return [ScheduleAssignmentResponse.model_validate(assignment) for assignment in assignments]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调度分配列表时发生错误"
        )


@router.post("/schedules/{schedule_id}/assignments", response_model=ScheduleAssignmentResponse, summary="创建调度分配")
async def create_schedule_assignment(
    schedule_id: UUID,
    assignment_data: ScheduleAssignmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建调度分配
    
    Args:
        schedule_id: 调度计划ID
        assignment_data: 调度分配创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleAssignmentResponse: 创建的调度分配信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 创建调度分配
        assignment = await schedule_service.create_schedule_assignment(
            db, schedule_id, assignment_data, current_user.id
        )
        
        return ScheduleAssignmentResponse.model_validate(assignment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建调度分配时发生错误"
        )


@router.put("/assignments/{assignment_id}", response_model=ScheduleAssignmentResponse, summary="更新调度分配")
async def update_schedule_assignment(
    assignment_id: UUID,
    assignment_data: ScheduleAssignmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新调度分配
    
    Args:
        assignment_id: 调度分配ID
        assignment_data: 调度分配更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleAssignmentResponse: 更新后的调度分配信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 更新调度分配
        assignment = await schedule_service.update_schedule_assignment(
            db, assignment_id, assignment_data
        )
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度分配不存在"
            )
        
        return ScheduleAssignmentResponse.model_validate(assignment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新调度分配时发生错误"
        )


@router.delete("/assignments/{assignment_id}", response_model=MessageResponse, summary="删除调度分配")
async def delete_schedule_assignment(
    assignment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除调度分配
    
    Args:
        assignment_id: 调度分配ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 删除调度分配
        success = await schedule_service.delete_schedule_assignment(db, assignment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度分配不存在"
            )
        
        return MessageResponse(message="调度分配删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除调度分配时发生错误"
        )


# ==================== 调度冲突检测 ====================

@router.get("/schedules/{schedule_id}/conflicts", response_model=List[ScheduleConflictResponse], summary="获取调度冲突列表")
async def get_schedule_conflicts(
    schedule_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取调度冲突列表
    
    Args:
        schedule_id: 调度计划ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ScheduleConflictResponse]: 调度冲突列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 获取调度冲突列表
        conflicts = await schedule_service.get_schedule_conflicts(db, schedule_id)
        
        return [ScheduleConflictResponse.model_validate(conflict) for conflict in conflicts]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调度冲突列表时发生错误"
        )


@router.post("/schedules/{schedule_id}/detect-conflicts", response_model=List[ScheduleConflictResponse], summary="检测调度冲突")
async def detect_schedule_conflicts(
    schedule_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """检测调度冲突
    
    Args:
        schedule_id: 调度计划ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ScheduleConflictResponse]: 检测到的调度冲突列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 检测调度冲突
        conflicts = await schedule_service.detect_schedule_conflicts(db, schedule_id)
        
        return [ScheduleConflictResponse.model_validate(conflict) for conflict in conflicts]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="检测调度冲突时发生错误"
        )


@router.post("/conflicts/{conflict_id}/resolve", response_model=MessageResponse, summary="解决调度冲突")
async def resolve_schedule_conflict(
    conflict_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """解决调度冲突
    
    Args:
        conflict_id: 调度冲突ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 解决结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 解决调度冲突
        success = await schedule_service.resolve_schedule_conflict(db, conflict_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度冲突不存在"
            )
        
        return MessageResponse(message="调度冲突解决成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="解决调度冲突时发生错误"
        )


# ==================== 调度模板管理 ====================

@router.get("/templates", response_model=PaginatedResponse[ScheduleTemplateResponse], summary="获取调度模板列表")
async def get_schedule_templates(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取调度模板列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（模板名称、描述）
        is_active: 激活状态过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[ScheduleTemplateResponse]: 分页的调度模板列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 构建过滤条件
        filters = {}
        if is_active is not None:
            filters["is_active"] = is_active
        
        # 获取调度模板列表
        templates, total = await schedule_service.get_schedule_templates(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[ScheduleTemplateResponse.model_validate(template) for template in templates],
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
            detail="获取调度模板列表时发生错误"
        )


@router.post("/templates", response_model=ScheduleTemplateResponse, summary="创建调度模板")
async def create_schedule_template(
    template_data: ScheduleTemplateCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建调度模板
    
    Args:
        template_data: 调度模板创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleTemplateResponse: 创建的调度模板信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:create"], db)
        
        # 创建调度模板
        template = await schedule_service.create_schedule_template(
            db, template_data, current_user.id
        )
        
        return ScheduleTemplateResponse.model_validate(template)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建调度模板时发生错误"
        )


@router.put("/templates/{template_id}", response_model=ScheduleTemplateResponse, summary="更新调度模板")
async def update_schedule_template(
    template_id: UUID,
    template_data: ScheduleTemplateUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新调度模板
    
    Args:
        template_id: 调度模板ID
        template_data: 调度模板更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ScheduleTemplateResponse: 更新后的调度模板信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 更新调度模板
        template = await schedule_service.update_schedule_template(
            db, template_id, template_data
        )
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度模板不存在"
            )
        
        return ScheduleTemplateResponse.model_validate(template)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新调度模板时发生错误"
        )


@router.delete("/templates/{template_id}", response_model=MessageResponse, summary="删除调度模板")
async def delete_schedule_template(
    template_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除调度模板
    
    Args:
        template_id: 调度模板ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:delete"], db)
        
        # 删除调度模板
        success = await schedule_service.delete_schedule_template(db, template_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调度模板不存在"
            )
        
        return MessageResponse(message="调度模板删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除调度模板时发生错误"
        )


# ==================== 资源可用性管理 ====================

@router.get("/resource-availability", response_model=PaginatedResponse[ResourceAvailabilityResponse], summary="获取资源可用性列表")
async def get_resource_availability(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    resource_id: Optional[UUID] = Query(None, description="资源ID"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取资源可用性列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        resource_id: 资源ID过滤
        start_date: 开始日期过滤
        end_date: 结束日期过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[ResourceAvailabilityResponse]: 分页的资源可用性列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 构建过滤条件
        filters = {}
        if resource_id:
            filters["resource_id"] = resource_id
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        
        # 获取资源可用性列表
        availability, total = await schedule_service.get_resource_availability(
            db, skip=skip, limit=limit, filters=filters
        )
        
        return PaginatedResponse(
            items=[ResourceAvailabilityResponse.model_validate(avail) for avail in availability],
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
            detail="获取资源可用性列表时发生错误"
        )


@router.post("/resource-availability", response_model=ResourceAvailabilityResponse, summary="创建资源可用性")
async def create_resource_availability(
    availability_data: ResourceAvailabilityCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建资源可用性
    
    Args:
        availability_data: 资源可用性创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ResourceAvailabilityResponse: 创建的资源可用性信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 创建资源可用性
        availability = await schedule_service.create_resource_availability(
            db, availability_data, current_user.id
        )
        
        return ResourceAvailabilityResponse.model_validate(availability)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建资源可用性时发生错误"
        )


@router.put("/resource-availability/{availability_id}", response_model=ResourceAvailabilityResponse, summary="更新资源可用性")
async def update_resource_availability(
    availability_id: UUID,
    availability_data: ResourceAvailabilityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新资源可用性
    
    Args:
        availability_id: 资源可用性ID
        availability_data: 资源可用性更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ResourceAvailabilityResponse: 更新后的资源可用性信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 更新资源可用性
        availability = await schedule_service.update_resource_availability(
            db, availability_id, availability_data
        )
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资源可用性不存在"
            )
        
        return ResourceAvailabilityResponse.model_validate(availability)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新资源可用性时发生错误"
        )


@router.delete("/resource-availability/{availability_id}", response_model=MessageResponse, summary="删除资源可用性")
async def delete_resource_availability(
    availability_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除资源可用性
    
    Args:
        availability_id: 资源可用性ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:update"], db)
        
        # 删除资源可用性
        success = await schedule_service.delete_resource_availability(db, availability_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资源可用性不存在"
            )
        
        return MessageResponse(message="资源可用性删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除资源可用性时发生错误"
        )


# ==================== 工作负荷分析 ====================

@router.get("/workload-analysis", response_model=List[WorkloadAnalysisResponse], summary="获取工作负荷分析")
async def get_workload_analysis(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    personnel_id: Optional[UUID] = Query(None, description="人员ID"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取工作负荷分析
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        department_id: 部门ID过滤
        personnel_id: 人员ID过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[WorkloadAnalysisResponse]: 工作负荷分析列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:read"], db)
        
        # 构建过滤条件
        filters = {
            "start_date": start_date,
            "end_date": end_date
        }
        if department_id:
            filters["department_id"] = department_id
        if personnel_id:
            filters["personnel_id"] = personnel_id
        
        # 获取工作负荷分析
        analysis = await schedule_service.get_workload_analysis(db, filters)
        
        return [WorkloadAnalysisResponse.model_validate(item) for item in analysis]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取工作负荷分析时发生错误"
        )


@router.post("/workload-analysis/generate", response_model=MessageResponse, summary="生成工作负荷分析")
async def generate_workload_analysis(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """生成工作负荷分析
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 生成结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["schedule:create"], db)
        
        # 生成工作负荷分析
        success = await schedule_service.generate_workload_analysis(
            db, start_date, end_date, current_user.id
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="生成工作负荷分析失败"
            )
        
        return MessageResponse(message="工作负荷分析生成成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="生成工作负荷分析时发生错误"
        )