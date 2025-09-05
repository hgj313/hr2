"""项目管理API端点

本模块实现了项目管理相关的API端点，包括项目、项目分配、里程碑、任务、文档等的管理功能。
"""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user, check_permissions
from app.models.auth import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectAssignmentCreate,
    ProjectAssignmentUpdate,
    ProjectAssignmentResponse,
    ProjectMilestoneCreate,
    ProjectMilestoneUpdate,
    ProjectMilestoneResponse,
    ProjectTaskCreate,
    ProjectTaskUpdate,
    ProjectTaskResponse,
    ProjectDocumentCreate,
    ProjectDocumentUpdate,
    ProjectDocumentResponse
)
from app.schemas.base import (
    PaginatedResponse,
    MessageResponse,
    BulkOperationRequest,
    BulkOperationResponse
)
from app.services.project import ProjectService

# 创建路由器
router = APIRouter()

# 初始化服务
project_service = ProjectService()


# ==================== 项目管理 ====================

@router.get("/projects", response_model=PaginatedResponse[ProjectResponse], summary="获取项目列表")
async def get_projects(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="项目状态"),
    priority: Optional[str] = Query(None, description="项目优先级"),
    manager_id: Optional[UUID] = Query(None, description="项目经理ID"),
    department_id: Optional[UUID] = Query(None, description="部门ID"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词（项目名称、描述）
        status: 项目状态过滤
        priority: 项目优先级过滤
        manager_id: 项目经理ID过滤
        department_id: 部门ID过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[ProjectResponse]: 分页的项目列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 构建过滤条件
        filters = {}
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if manager_id:
            filters["manager_id"] = manager_id
        if department_id:
            filters["department_id"] = department_id
        
        # 获取项目列表
        projects, total = await project_service.get_projects(
            db, skip=skip, limit=limit, search=search, filters=filters
        )
        
        return PaginatedResponse(
            items=[ProjectResponse.model_validate(project) for project in projects],
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
            detail="获取项目列表时发生错误"
        )


@router.get("/projects/{project_id}", response_model=ProjectDetailResponse, summary="获取项目详情")
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目详情
    
    Args:
        project_id: 项目ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectDetailResponse: 项目详情
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 获取项目信息
        project = await project_service.get_project_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目不存在"
            )
        
        return ProjectDetailResponse.model_validate(project)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取项目详情时发生错误"
        )


@router.post("/projects", response_model=ProjectResponse, summary="创建项目")
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建项目
    
    Args:
        project_data: 项目创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectResponse: 创建的项目信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:create"], db)
        
        # 创建项目
        project = await project_service.create_project(db, project_data, current_user.id)
        
        return ProjectResponse.model_validate(project)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建项目时发生错误"
        )


@router.put("/projects/{project_id}", response_model=ProjectResponse, summary="更新项目")
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新项目
    
    Args:
        project_id: 项目ID
        project_data: 项目更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectResponse: 更新后的项目信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 更新项目
        project = await project_service.update_project(db, project_id, project_data)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目不存在"
            )
        
        return ProjectResponse.model_validate(project)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新项目时发生错误"
        )


@router.delete("/projects/{project_id}", response_model=MessageResponse, summary="删除项目")
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除项目
    
    Args:
        project_id: 项目ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:delete"], db)
        
        # 删除项目
        success = await project_service.delete_project(db, project_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目不存在"
            )
        
        return MessageResponse(message="项目删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除项目时发生错误"
        )


# ==================== 项目分配管理 ====================

@router.get("/projects/{project_id}/assignments", response_model=List[ProjectAssignmentResponse], summary="获取项目分配列表")
async def get_project_assignments(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目分配列表
    
    Args:
        project_id: 项目ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ProjectAssignmentResponse]: 项目分配列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 获取项目分配列表
        assignments = await project_service.get_project_assignments(db, project_id)
        
        return [ProjectAssignmentResponse.model_validate(assignment) for assignment in assignments]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取项目分配列表时发生错误"
        )


@router.post("/projects/{project_id}/assignments", response_model=ProjectAssignmentResponse, summary="创建项目分配")
async def create_project_assignment(
    project_id: UUID,
    assignment_data: ProjectAssignmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建项目分配
    
    Args:
        project_id: 项目ID
        assignment_data: 项目分配创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectAssignmentResponse: 创建的项目分配信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 创建项目分配
        assignment = await project_service.create_project_assignment(
            db, project_id, assignment_data, current_user.id
        )
        
        return ProjectAssignmentResponse.model_validate(assignment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建项目分配时发生错误"
        )


@router.put("/assignments/{assignment_id}", response_model=ProjectAssignmentResponse, summary="更新项目分配")
async def update_project_assignment(
    assignment_id: UUID,
    assignment_data: ProjectAssignmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新项目分配
    
    Args:
        assignment_id: 项目分配ID
        assignment_data: 项目分配更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectAssignmentResponse: 更新后的项目分配信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 更新项目分配
        assignment = await project_service.update_project_assignment(
            db, assignment_id, assignment_data
        )
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目分配不存在"
            )
        
        return ProjectAssignmentResponse.model_validate(assignment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新项目分配时发生错误"
        )


@router.delete("/assignments/{assignment_id}", response_model=MessageResponse, summary="删除项目分配")
async def delete_project_assignment(
    assignment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除项目分配
    
    Args:
        assignment_id: 项目分配ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 删除项目分配
        success = await project_service.delete_project_assignment(db, assignment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目分配不存在"
            )
        
        return MessageResponse(message="项目分配删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除项目分配时发生错误"
        )


# ==================== 项目里程碑管理 ====================

@router.get("/projects/{project_id}/milestones", response_model=List[ProjectMilestoneResponse], summary="获取项目里程碑列表")
async def get_project_milestones(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目里程碑列表
    
    Args:
        project_id: 项目ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ProjectMilestoneResponse]: 项目里程碑列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 获取项目里程碑列表
        milestones = await project_service.get_project_milestones(db, project_id)
        
        return [ProjectMilestoneResponse.model_validate(milestone) for milestone in milestones]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取项目里程碑列表时发生错误"
        )


@router.post("/projects/{project_id}/milestones", response_model=ProjectMilestoneResponse, summary="创建项目里程碑")
async def create_project_milestone(
    project_id: UUID,
    milestone_data: ProjectMilestoneCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建项目里程碑
    
    Args:
        project_id: 项目ID
        milestone_data: 项目里程碑创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectMilestoneResponse: 创建的项目里程碑信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 创建项目里程碑
        milestone = await project_service.create_project_milestone(
            db, project_id, milestone_data, current_user.id
        )
        
        return ProjectMilestoneResponse.model_validate(milestone)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建项目里程碑时发生错误"
        )


@router.put("/milestones/{milestone_id}", response_model=ProjectMilestoneResponse, summary="更新项目里程碑")
async def update_project_milestone(
    milestone_id: UUID,
    milestone_data: ProjectMilestoneUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新项目里程碑
    
    Args:
        milestone_id: 项目里程碑ID
        milestone_data: 项目里程碑更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectMilestoneResponse: 更新后的项目里程碑信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 更新项目里程碑
        milestone = await project_service.update_project_milestone(
            db, milestone_id, milestone_data
        )
        if not milestone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目里程碑不存在"
            )
        
        return ProjectMilestoneResponse.model_validate(milestone)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新项目里程碑时发生错误"
        )


@router.delete("/milestones/{milestone_id}", response_model=MessageResponse, summary="删除项目里程碑")
async def delete_project_milestone(
    milestone_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除项目里程碑
    
    Args:
        milestone_id: 项目里程碑ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 删除项目里程碑
        success = await project_service.delete_project_milestone(db, milestone_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目里程碑不存在"
            )
        
        return MessageResponse(message="项目里程碑删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除项目里程碑时发生错误"
        )


# ==================== 项目任务管理 ====================

@router.get("/projects/{project_id}/tasks", response_model=PaginatedResponse[ProjectTaskResponse], summary="获取项目任务列表")
async def get_project_tasks(
    project_id: UUID,
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    status: Optional[str] = Query(None, description="任务状态"),
    assignee_id: Optional[UUID] = Query(None, description="分配人员ID"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目任务列表
    
    Args:
        project_id: 项目ID
        skip: 跳过的记录数
        limit: 返回的记录数
        status: 任务状态过滤
        assignee_id: 分配人员ID过滤
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        PaginatedResponse[ProjectTaskResponse]: 分页的项目任务列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 构建过滤条件
        filters = {"project_id": project_id}
        if status:
            filters["status"] = status
        if assignee_id:
            filters["assignee_id"] = assignee_id
        
        # 获取项目任务列表
        tasks, total = await project_service.get_project_tasks(
            db, skip=skip, limit=limit, filters=filters
        )
        
        return PaginatedResponse(
            items=[ProjectTaskResponse.model_validate(task) for task in tasks],
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
            detail="获取项目任务列表时发生错误"
        )


@router.post("/projects/{project_id}/tasks", response_model=ProjectTaskResponse, summary="创建项目任务")
async def create_project_task(
    project_id: UUID,
    task_data: ProjectTaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建项目任务
    
    Args:
        project_id: 项目ID
        task_data: 项目任务创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectTaskResponse: 创建的项目任务信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 创建项目任务
        task = await project_service.create_project_task(
            db, project_id, task_data, current_user.id
        )
        
        return ProjectTaskResponse.model_validate(task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建项目任务时发生错误"
        )


@router.put("/tasks/{task_id}", response_model=ProjectTaskResponse, summary="更新项目任务")
async def update_project_task(
    task_id: UUID,
    task_data: ProjectTaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新项目任务
    
    Args:
        task_id: 项目任务ID
        task_data: 项目任务更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectTaskResponse: 更新后的项目任务信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 更新项目任务
        task = await project_service.update_project_task(db, task_id, task_data)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目任务不存在"
            )
        
        return ProjectTaskResponse.model_validate(task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新项目任务时发生错误"
        )


@router.delete("/tasks/{task_id}", response_model=MessageResponse, summary="删除项目任务")
async def delete_project_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除项目任务
    
    Args:
        task_id: 项目任务ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 删除项目任务
        success = await project_service.delete_project_task(db, task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目任务不存在"
            )
        
        return MessageResponse(message="项目任务删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除项目任务时发生错误"
        )


# ==================== 项目文档管理 ====================

@router.get("/projects/{project_id}/documents", response_model=List[ProjectDocumentResponse], summary="获取项目文档列表")
async def get_project_documents(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取项目文档列表
    
    Args:
        project_id: 项目ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        List[ProjectDocumentResponse]: 项目文档列表
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:read"], db)
        
        # 获取项目文档列表
        documents = await project_service.get_project_documents(db, project_id)
        
        return [ProjectDocumentResponse.model_validate(doc) for doc in documents]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取项目文档列表时发生错误"
        )


@router.post("/projects/{project_id}/documents", response_model=ProjectDocumentResponse, summary="创建项目文档")
async def create_project_document(
    project_id: UUID,
    document_data: ProjectDocumentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建项目文档
    
    Args:
        project_id: 项目ID
        document_data: 项目文档创建数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectDocumentResponse: 创建的项目文档信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 创建项目文档
        document = await project_service.create_project_document(
            db, project_id, document_data, current_user.id
        )
        
        return ProjectDocumentResponse.model_validate(document)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建项目文档时发生错误"
        )


@router.put("/documents/{document_id}", response_model=ProjectDocumentResponse, summary="更新项目文档")
async def update_project_document(
    document_id: UUID,
    document_data: ProjectDocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """更新项目文档
    
    Args:
        document_id: 项目文档ID
        document_data: 项目文档更新数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        ProjectDocumentResponse: 更新后的项目文档信息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 更新项目文档
        document = await project_service.update_project_document(
            db, document_id, document_data
        )
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目文档不存在"
            )
        
        return ProjectDocumentResponse.model_validate(document)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新项目文档时发生错误"
        )


@router.delete("/documents/{document_id}", response_model=MessageResponse, summary="删除项目文档")
async def delete_project_document(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """删除项目文档
    
    Args:
        document_id: 项目文档ID
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        MessageResponse: 删除结果消息
    """
    try:
        # 检查权限
        await check_permissions(current_user, ["project:update"], db)
        
        # 删除项目文档
        success = await project_service.delete_project_document(db, document_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目文档不存在"
            )
        
        return MessageResponse(message="项目文档删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除项目文档时发生错误"
        )