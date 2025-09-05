"""项目管理相关的Pydantic模式

本文件定义了项目管理模块的所有数据模型，包括项目、项目分配、里程碑、任务和文档等。
"""

from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from .base import BaseSchema, TimestampMixin, BaseResponse, DataResponse, ListResponse, PaginatedResponse


class ProjectStatus(str, Enum):
    """项目状态枚举"""
    PLANNING = "planning"  # 规划中
    ACTIVE = "active"  # 进行中
    ON_HOLD = "on_hold"  # 暂停
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class ProjectPriority(str, Enum):
    """项目优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    CRITICAL = "critical"  # 紧急


class TaskStatus(str, Enum):
    """任务状态枚举"""
    TODO = "todo"  # 待办
    IN_PROGRESS = "in_progress"  # 进行中
    REVIEW = "review"  # 审核中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class TaskPriority(str, Enum):
    """任务优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


class MilestoneStatus(str, Enum):
    """里程碑状态枚举"""
    PENDING = "pending"  # 待完成
    COMPLETED = "completed"  # 已完成
    OVERDUE = "overdue"  # 已逾期


class DocumentType(str, Enum):
    """文档类型枚举"""
    REQUIREMENT = "requirement"  # 需求文档
    DESIGN = "design"  # 设计文档
    TECHNICAL = "technical"  # 技术文档
    USER_MANUAL = "user_manual"  # 用户手册
    TEST_PLAN = "test_plan"  # 测试计划
    OTHER = "other"  # 其他


# 项目相关模式
class ProjectBase(BaseSchema):
    """项目基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="项目名称")
    description: Optional[str] = Field(None, max_length=2000, description="项目描述")
    status: ProjectStatus = Field(ProjectStatus.PLANNING, description="项目状态")
    priority: ProjectPriority = Field(ProjectPriority.MEDIUM, description="项目优先级")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    budget: Optional[Decimal] = Field(None, ge=0, description="项目预算")
    actual_cost: Optional[Decimal] = Field(None, ge=0, description="实际成本")
    progress: int = Field(0, ge=0, le=100, description="项目进度百分比")
    manager_id: Optional[int] = Field(None, description="项目经理ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    client_name: Optional[str] = Field(None, max_length=200, description="客户名称")
    client_contact: Optional[str] = Field(None, max_length=200, description="客户联系方式")
    is_active: bool = Field(True, description="是否激活")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v


class ProjectCreate(ProjectBase):
    """创建项目模式"""
    pass


class ProjectUpdate(BaseSchema):
    """更新项目模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="项目名称")
    description: Optional[str] = Field(None, max_length=2000, description="项目描述")
    status: Optional[ProjectStatus] = Field(None, description="项目状态")
    priority: Optional[ProjectPriority] = Field(None, description="项目优先级")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    budget: Optional[Decimal] = Field(None, ge=0, description="项目预算")
    actual_cost: Optional[Decimal] = Field(None, ge=0, description="实际成本")
    progress: Optional[int] = Field(None, ge=0, le=100, description="项目进度百分比")
    manager_id: Optional[int] = Field(None, description="项目经理ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    client_name: Optional[str] = Field(None, max_length=200, description="客户名称")
    client_contact: Optional[str] = Field(None, max_length=200, description="客户联系方式")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ProjectResponse(ProjectBase, TimestampMixin):
    """项目响应模式"""
    id: int = Field(..., description="项目ID")
    manager_name: Optional[str] = Field(None, description="项目经理姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    team_size: int = Field(0, description="团队规模")
    task_count: int = Field(0, description="任务数量")
    completed_task_count: int = Field(0, description="已完成任务数量")
    milestone_count: int = Field(0, description="里程碑数量")
    completed_milestone_count: int = Field(0, description="已完成里程碑数量")

    class Config:
        from_attributes = True


# 项目分配相关模式
class ProjectAssignmentBase(BaseSchema):
    """项目分配基础模式"""
    project_id: int = Field(..., description="项目ID")
    user_id: int = Field(..., description="用户ID")
    role: str = Field(..., max_length=100, description="角色")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    allocation_percentage: int = Field(100, ge=0, le=100, description="分配百分比")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    is_active: bool = Field(True, description="是否激活")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v


class ProjectAssignmentCreate(ProjectAssignmentBase):
    """创建项目分配模式"""
    pass


class ProjectAssignmentUpdate(BaseSchema):
    """更新项目分配模式"""
    role: Optional[str] = Field(None, max_length=100, description="角色")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    allocation_percentage: Optional[int] = Field(None, ge=0, le=100, description="分配百分比")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ProjectAssignmentResponse(ProjectAssignmentBase, TimestampMixin):
    """项目分配响应模式"""
    id: int = Field(..., description="分配ID")
    project_name: Optional[str] = Field(None, description="项目名称")
    user_name: Optional[str] = Field(None, description="用户姓名")
    user_email: Optional[str] = Field(None, description="用户邮箱")
    total_hours: Optional[Decimal] = Field(None, description="总工时")
    total_cost: Optional[Decimal] = Field(None, description="总成本")

    class Config:
        from_attributes = True


# 里程碑相关模式
class MilestoneBase(BaseSchema):
    """里程碑基础模式"""
    project_id: int = Field(..., description="项目ID")
    name: str = Field(..., min_length=1, max_length=200, description="里程碑名称")
    description: Optional[str] = Field(None, max_length=1000, description="里程碑描述")
    due_date: date = Field(..., description="截止日期")
    status: MilestoneStatus = Field(MilestoneStatus.PENDING, description="里程碑状态")
    completion_date: Optional[date] = Field(None, description="完成日期")
    deliverables: Optional[str] = Field(None, max_length=2000, description="交付物")
    is_critical: bool = Field(False, description="是否关键里程碑")


class MilestoneCreate(MilestoneBase):
    """创建里程碑模式"""
    pass


class MilestoneUpdate(BaseSchema):
    """更新里程碑模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="里程碑名称")
    description: Optional[str] = Field(None, max_length=1000, description="里程碑描述")
    due_date: Optional[date] = Field(None, description="截止日期")
    status: Optional[MilestoneStatus] = Field(None, description="里程碑状态")
    completion_date: Optional[date] = Field(None, description="完成日期")
    deliverables: Optional[str] = Field(None, max_length=2000, description="交付物")
    is_critical: Optional[bool] = Field(None, description="是否关键里程碑")


class MilestoneResponse(MilestoneBase, TimestampMixin):
    """里程碑响应模式"""
    id: int = Field(..., description="里程碑ID")
    project_name: Optional[str] = Field(None, description="项目名称")
    days_remaining: Optional[int] = Field(None, description="剩余天数")
    is_overdue: bool = Field(False, description="是否逾期")

    class Config:
        from_attributes = True


# 任务相关模式
class TaskBase(BaseSchema):
    """任务基础模式"""
    project_id: int = Field(..., description="项目ID")
    milestone_id: Optional[int] = Field(None, description="里程碑ID")
    parent_task_id: Optional[int] = Field(None, description="父任务ID")
    name: str = Field(..., min_length=1, max_length=200, description="任务名称")
    description: Optional[str] = Field(None, max_length=2000, description="任务描述")
    status: TaskStatus = Field(TaskStatus.TODO, description="任务状态")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="任务优先级")
    assignee_id: Optional[int] = Field(None, description="负责人ID")
    start_date: Optional[date] = Field(None, description="开始日期")
    due_date: Optional[date] = Field(None, description="截止日期")
    completion_date: Optional[date] = Field(None, description="完成日期")
    estimated_hours: Optional[Decimal] = Field(None, ge=0, description="预估工时")
    actual_hours: Optional[Decimal] = Field(None, ge=0, description="实际工时")
    progress: int = Field(0, ge=0, le=100, description="任务进度百分比")
    tags: Optional[str] = Field(None, max_length=500, description="标签")

    @validator('due_date')
    def validate_due_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('截止日期不能早于开始日期')
        return v


class TaskCreate(TaskBase):
    """创建任务模式"""
    pass


class TaskUpdate(BaseSchema):
    """更新任务模式"""
    milestone_id: Optional[int] = Field(None, description="里程碑ID")
    parent_task_id: Optional[int] = Field(None, description="父任务ID")
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="任务名称")
    description: Optional[str] = Field(None, max_length=2000, description="任务描述")
    status: Optional[TaskStatus] = Field(None, description="任务状态")
    priority: Optional[TaskPriority] = Field(None, description="任务优先级")
    assignee_id: Optional[int] = Field(None, description="负责人ID")
    start_date: Optional[date] = Field(None, description="开始日期")
    due_date: Optional[date] = Field(None, description="截止日期")
    completion_date: Optional[date] = Field(None, description="完成日期")
    estimated_hours: Optional[Decimal] = Field(None, ge=0, description="预估工时")
    actual_hours: Optional[Decimal] = Field(None, ge=0, description="实际工时")
    progress: Optional[int] = Field(None, ge=0, le=100, description="任务进度百分比")
    tags: Optional[str] = Field(None, max_length=500, description="标签")


class TaskResponse(TaskBase, TimestampMixin):
    """任务响应模式"""
    id: int = Field(..., description="任务ID")
    project_name: Optional[str] = Field(None, description="项目名称")
    milestone_name: Optional[str] = Field(None, description="里程碑名称")
    parent_task_name: Optional[str] = Field(None, description="父任务名称")
    assignee_name: Optional[str] = Field(None, description="负责人姓名")
    subtask_count: int = Field(0, description="子任务数量")
    completed_subtask_count: int = Field(0, description="已完成子任务数量")
    days_remaining: Optional[int] = Field(None, description="剩余天数")
    is_overdue: bool = Field(False, description="是否逾期")

    class Config:
        from_attributes = True


# 文档相关模式
class DocumentBase(BaseSchema):
    """文档基础模式"""
    project_id: int = Field(..., description="项目ID")
    task_id: Optional[int] = Field(None, description="任务ID")
    name: str = Field(..., min_length=1, max_length=200, description="文档名称")
    description: Optional[str] = Field(None, max_length=1000, description="文档描述")
    document_type: DocumentType = Field(DocumentType.OTHER, description="文档类型")
    file_path: str = Field(..., max_length=500, description="文件路径")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小（字节）")
    mime_type: Optional[str] = Field(None, max_length=100, description="MIME类型")
    version: str = Field("1.0", max_length=20, description="版本号")
    author_id: int = Field(..., description="作者ID")
    is_public: bool = Field(False, description="是否公开")


class DocumentCreate(DocumentBase):
    """创建文档模式"""
    pass


class DocumentUpdate(BaseSchema):
    """更新文档模式"""
    task_id: Optional[int] = Field(None, description="任务ID")
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="文档名称")
    description: Optional[str] = Field(None, max_length=1000, description="文档描述")
    document_type: Optional[DocumentType] = Field(None, description="文档类型")
    version: Optional[str] = Field(None, max_length=20, description="版本号")
    is_public: Optional[bool] = Field(None, description="是否公开")


class DocumentResponse(DocumentBase, TimestampMixin):
    """文档响应模式"""
    id: int = Field(..., description="文档ID")
    project_name: Optional[str] = Field(None, description="项目名称")
    task_name: Optional[str] = Field(None, description="任务名称")
    author_name: Optional[str] = Field(None, description="作者姓名")
    download_count: int = Field(0, description="下载次数")
    file_size_formatted: Optional[str] = Field(None, description="格式化的文件大小")

    class Config:
        from_attributes = True


# 响应模式
class ProjectListResponse(ListResponse[ProjectResponse]):
    """项目列表响应"""
    pass


class ProjectPaginatedResponse(PaginatedResponse[ProjectResponse]):
    """项目分页响应"""
    pass


class ProjectAssignmentListResponse(ListResponse[ProjectAssignmentResponse]):
    """项目分配列表响应"""
    pass


class MilestoneListResponse(ListResponse[MilestoneResponse]):
    """里程碑列表响应"""
    pass


class TaskListResponse(ListResponse[TaskResponse]):
    """任务列表响应"""
    pass


class TaskPaginatedResponse(PaginatedResponse[TaskResponse]):
    """任务分页响应"""
    pass


class DocumentListResponse(ListResponse[DocumentResponse]):
    """文档列表响应"""
    pass