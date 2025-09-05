"""审批流程相关的Pydantic模式

本文件定义了审批流程模块的所有数据模型，包括审批请求、审批工作流、审批评论、审批历史和审批委托等。
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from .base import BaseSchema, TimestampMixin, BaseResponse, DataResponse, ListResponse, PaginatedResponse


class ApprovalStatus(str, Enum):
    """审批状态枚举"""
    PENDING = "pending"  # 待审批
    IN_REVIEW = "in_review"  # 审核中
    APPROVED = "approved"  # 已批准
    REJECTED = "rejected"  # 已拒绝
    CANCELLED = "cancelled"  # 已取消
    EXPIRED = "expired"  # 已过期


class ApprovalPriority(str, Enum):
    """审批优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


class ApprovalType(str, Enum):
    """审批类型枚举"""
    LEAVE_REQUEST = "leave_request"  # 请假申请
    OVERTIME_REQUEST = "overtime_request"  # 加班申请
    EXPENSE_CLAIM = "expense_claim"  # 费用报销
    BUDGET_APPROVAL = "budget_approval"  # 预算审批
    PROJECT_APPROVAL = "project_approval"  # 项目审批
    RESOURCE_REQUEST = "resource_request"  # 资源申请
    SCHEDULE_CHANGE = "schedule_change"  # 调度变更
    POLICY_EXCEPTION = "policy_exception"  # 政策例外
    OTHER = "other"  # 其他


class WorkflowStatus(str, Enum):
    """工作流状态枚举"""
    DRAFT = "draft"  # 草稿
    ACTIVE = "active"  # 激活
    INACTIVE = "inactive"  # 停用
    ARCHIVED = "archived"  # 已归档


class StepType(str, Enum):
    """步骤类型枚举"""
    APPROVAL = "approval"  # 审批
    REVIEW = "review"  # 审核
    NOTIFICATION = "notification"  # 通知
    CONDITION = "condition"  # 条件判断
    PARALLEL = "parallel"  # 并行处理
    SEQUENTIAL = "sequential"  # 顺序处理


class DelegationType(str, Enum):
    """委托类型枚举"""
    TEMPORARY = "temporary"  # 临时委托
    PERMANENT = "permanent"  # 永久委托
    CONDITIONAL = "conditional"  # 条件委托


# 审批请求相关模式
class ApprovalRequestBase(BaseSchema):
    """审批请求基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="审批标题")
    description: Optional[str] = Field(None, max_length=2000, description="审批描述")
    approval_type: ApprovalType = Field(..., description="审批类型")
    priority: ApprovalPriority = Field(ApprovalPriority.MEDIUM, description="优先级")
    status: ApprovalStatus = Field(ApprovalStatus.PENDING, description="审批状态")
    workflow_id: Optional[int] = Field(None, description="工作流ID")
    current_step: int = Field(1, ge=1, description="当前步骤")
    total_steps: int = Field(1, ge=1, description="总步骤数")
    request_data: Dict[str, Any] = Field(..., description="请求数据")
    amount: Optional[Decimal] = Field(None, ge=0, description="金额")
    currency: Optional[str] = Field(None, max_length=3, description="货币")
    due_date: Optional[date] = Field(None, description="截止日期")
    business_justification: Optional[str] = Field(None, max_length=1000, description="业务理由")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    requester_id: int = Field(..., description="申请人ID")
    current_approver_id: Optional[int] = Field(None, description="当前审批人ID")
    is_urgent: bool = Field(False, description="是否紧急")
    auto_approve: bool = Field(False, description="是否自动审批")

    @validator('total_steps')
    def validate_total_steps(cls, v, values):
        if v and 'current_step' in values and values['current_step'] and v < values['current_step']:
            raise ValueError('总步骤数不能小于当前步骤')
        return v


class ApprovalRequestCreate(ApprovalRequestBase):
    """创建审批请求模式"""
    pass


class ApprovalRequestUpdate(BaseSchema):
    """更新审批请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="审批标题")
    description: Optional[str] = Field(None, max_length=2000, description="审批描述")
    priority: Optional[ApprovalPriority] = Field(None, description="优先级")
    status: Optional[ApprovalStatus] = Field(None, description="审批状态")
    current_step: Optional[int] = Field(None, ge=1, description="当前步骤")
    total_steps: Optional[int] = Field(None, ge=1, description="总步骤数")
    request_data: Optional[Dict[str, Any]] = Field(None, description="请求数据")
    amount: Optional[Decimal] = Field(None, ge=0, description="金额")
    currency: Optional[str] = Field(None, max_length=3, description="货币")
    due_date: Optional[date] = Field(None, description="截止日期")
    business_justification: Optional[str] = Field(None, max_length=1000, description="业务理由")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    current_approver_id: Optional[int] = Field(None, description="当前审批人ID")
    is_urgent: Optional[bool] = Field(None, description="是否紧急")
    auto_approve: Optional[bool] = Field(None, description="是否自动审批")


class ApprovalRequestResponse(ApprovalRequestBase, TimestampMixin):
    """审批请求响应模式"""
    id: int = Field(..., description="请求ID")
    workflow_name: Optional[str] = Field(None, description="工作流名称")
    requester_name: Optional[str] = Field(None, description="申请人姓名")
    requester_email: Optional[str] = Field(None, description="申请人邮箱")
    current_approver_name: Optional[str] = Field(None, description="当前审批人姓名")
    days_pending: Optional[int] = Field(None, description="待审批天数")
    is_overdue: bool = Field(False, description="是否逾期")
    approval_history_count: int = Field(0, description="审批历史数量")
    comment_count: int = Field(0, description="评论数量")
    estimated_completion_date: Optional[date] = Field(None, description="预计完成日期")
    sla_deadline: Optional[datetime] = Field(None, description="SLA截止时间")

    class Config:
        from_attributes = True


# 审批工作流相关模式
class ApprovalWorkflowBase(BaseSchema):
    """审批工作流基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="工作流名称")
    description: Optional[str] = Field(None, max_length=1000, description="工作流描述")
    approval_type: ApprovalType = Field(..., description="审批类型")
    status: WorkflowStatus = Field(WorkflowStatus.DRAFT, description="工作流状态")
    workflow_definition: Dict[str, Any] = Field(..., description="工作流定义")
    version: str = Field("1.0", max_length=20, description="版本号")
    is_default: bool = Field(False, description="是否默认工作流")
    auto_start: bool = Field(True, description="是否自动启动")
    sla_hours: Optional[int] = Field(None, ge=0, description="SLA小时数")
    escalation_rules: Optional[Dict[str, Any]] = Field(None, description="升级规则")
    notification_settings: Optional[Dict[str, Any]] = Field(None, description="通知设置")
    conditions: Optional[Dict[str, Any]] = Field(None, description="触发条件")
    created_by: int = Field(..., description="创建人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_active: bool = Field(True, description="是否激活")


class ApprovalWorkflowCreate(ApprovalWorkflowBase):
    """创建审批工作流模式"""
    pass


class ApprovalWorkflowUpdate(BaseSchema):
    """更新审批工作流模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="工作流名称")
    description: Optional[str] = Field(None, max_length=1000, description="工作流描述")
    status: Optional[WorkflowStatus] = Field(None, description="工作流状态")
    workflow_definition: Optional[Dict[str, Any]] = Field(None, description="工作流定义")
    version: Optional[str] = Field(None, max_length=20, description="版本号")
    is_default: Optional[bool] = Field(None, description="是否默认工作流")
    auto_start: Optional[bool] = Field(None, description="是否自动启动")
    sla_hours: Optional[int] = Field(None, ge=0, description="SLA小时数")
    escalation_rules: Optional[Dict[str, Any]] = Field(None, description="升级规则")
    notification_settings: Optional[Dict[str, Any]] = Field(None, description="通知设置")
    conditions: Optional[Dict[str, Any]] = Field(None, description="触发条件")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ApprovalWorkflowResponse(ApprovalWorkflowBase, TimestampMixin):
    """审批工作流响应模式"""
    id: int = Field(..., description="工作流ID")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    usage_count: int = Field(0, description="使用次数")
    success_rate: Optional[Decimal] = Field(None, description="成功率")
    average_completion_time: Optional[Decimal] = Field(None, description="平均完成时间（小时）")
    step_count: int = Field(0, description="步骤数量")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")

    class Config:
        from_attributes = True


# 审批评论相关模式
class ApprovalCommentBase(BaseSchema):
    """审批评论基础模式"""
    approval_request_id: int = Field(..., description="审批请求ID")
    content: str = Field(..., min_length=1, max_length=2000, description="评论内容")
    comment_type: str = Field("general", max_length=50, description="评论类型")
    is_internal: bool = Field(False, description="是否内部评论")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    author_id: int = Field(..., description="作者ID")
    parent_comment_id: Optional[int] = Field(None, description="父评论ID")
    is_system_generated: bool = Field(False, description="是否系统生成")


class ApprovalCommentCreate(ApprovalCommentBase):
    """创建审批评论模式"""
    pass


class ApprovalCommentUpdate(BaseSchema):
    """更新审批评论模式"""
    content: Optional[str] = Field(None, min_length=1, max_length=2000, description="评论内容")
    comment_type: Optional[str] = Field(None, max_length=50, description="评论类型")
    is_internal: Optional[bool] = Field(None, description="是否内部评论")
    attachments: Optional[List[str]] = Field(None, description="附件列表")


class ApprovalCommentResponse(ApprovalCommentBase, TimestampMixin):
    """审批评论响应模式"""
    id: int = Field(..., description="评论ID")
    author_name: Optional[str] = Field(None, description="作者姓名")
    author_avatar: Optional[str] = Field(None, description="作者头像")
    parent_comment_content: Optional[str] = Field(None, description="父评论内容")
    reply_count: int = Field(0, description="回复数量")
    is_edited: bool = Field(False, description="是否已编辑")
    edited_at: Optional[datetime] = Field(None, description="编辑时间")

    class Config:
        from_attributes = True


# 审批历史相关模式
class ApprovalHistoryBase(BaseSchema):
    """审批历史基础模式"""
    approval_request_id: int = Field(..., description="审批请求ID")
    step_number: int = Field(..., ge=1, description="步骤编号")
    step_name: str = Field(..., max_length=100, description="步骤名称")
    action: str = Field(..., max_length=50, description="操作")
    status: ApprovalStatus = Field(..., description="状态")
    actor_id: int = Field(..., description="操作人ID")
    decision: Optional[str] = Field(None, max_length=20, description="决定")
    comments: Optional[str] = Field(None, max_length=1000, description="评论")
    duration_minutes: Optional[int] = Field(None, ge=0, description="处理时长（分钟）")
    delegated_from: Optional[int] = Field(None, description="委托来源ID")
    system_notes: Optional[str] = Field(None, max_length=500, description="系统备注")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class ApprovalHistoryCreate(ApprovalHistoryBase):
    """创建审批历史模式"""
    pass


class ApprovalHistoryResponse(ApprovalHistoryBase, TimestampMixin):
    """审批历史响应模式"""
    id: int = Field(..., description="历史ID")
    actor_name: Optional[str] = Field(None, description="操作人姓名")
    delegator_name: Optional[str] = Field(None, description="委托人姓名")
    duration_formatted: Optional[str] = Field(None, description="格式化的处理时长")
    is_current_step: bool = Field(False, description="是否当前步骤")
    next_step_name: Optional[str] = Field(None, description="下一步骤名称")
    next_approver_name: Optional[str] = Field(None, description="下一审批人姓名")

    class Config:
        from_attributes = True


# 审批委托相关模式
class ApprovalDelegationBase(BaseSchema):
    """审批委托基础模式"""
    delegator_id: int = Field(..., description="委托人ID")
    delegate_id: int = Field(..., description="被委托人ID")
    delegation_type: DelegationType = Field(DelegationType.TEMPORARY, description="委托类型")
    approval_types: Optional[List[ApprovalType]] = Field(None, description="审批类型列表")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    conditions: Optional[Dict[str, Any]] = Field(None, description="委托条件")
    reason: Optional[str] = Field(None, max_length=500, description="委托原因")
    is_active: bool = Field(True, description="是否激活")
    auto_notify: bool = Field(True, description="是否自动通知")
    created_by: int = Field(..., description="创建人ID")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v

    @validator('delegate_id')
    def validate_delegate_id(cls, v, values):
        if v and 'delegator_id' in values and values['delegator_id'] and v == values['delegator_id']:
            raise ValueError('被委托人不能是委托人自己')
        return v


class ApprovalDelegationCreate(ApprovalDelegationBase):
    """创建审批委托模式"""
    pass


class ApprovalDelegationUpdate(BaseSchema):
    """更新审批委托模式"""
    delegation_type: Optional[DelegationType] = Field(None, description="委托类型")
    approval_types: Optional[List[ApprovalType]] = Field(None, description="审批类型列表")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    conditions: Optional[Dict[str, Any]] = Field(None, description="委托条件")
    reason: Optional[str] = Field(None, max_length=500, description="委托原因")
    is_active: Optional[bool] = Field(None, description="是否激活")
    auto_notify: Optional[bool] = Field(None, description="是否自动通知")


class ApprovalDelegationResponse(ApprovalDelegationBase, TimestampMixin):
    """审批委托响应模式"""
    id: int = Field(..., description="委托ID")
    delegator_name: Optional[str] = Field(None, description="委托人姓名")
    delegate_name: Optional[str] = Field(None, description="被委托人姓名")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    usage_count: int = Field(0, description="使用次数")
    days_remaining: Optional[int] = Field(None, description="剩余天数")
    is_expired: bool = Field(False, description="是否已过期")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")

    class Config:
        from_attributes = True


# 响应模式
class ApprovalRequestListResponse(ListResponse[ApprovalRequestResponse]):
    """审批请求列表响应"""
    pass


class ApprovalRequestPaginatedResponse(PaginatedResponse[ApprovalRequestResponse]):
    """审批请求分页响应"""
    pass


class ApprovalWorkflowListResponse(ListResponse[ApprovalWorkflowResponse]):
    """审批工作流列表响应"""
    pass


class ApprovalCommentListResponse(ListResponse[ApprovalCommentResponse]):
    """审批评论列表响应"""
    pass


class ApprovalHistoryListResponse(ListResponse[ApprovalHistoryResponse]):
    """审批历史列表响应"""
    pass


class ApprovalDelegationListResponse(ListResponse[ApprovalDelegationResponse]):
    """审批委托列表响应"""
    pass


# 特殊请求模式
class ApprovalDecisionRequest(BaseSchema):
    """审批决定请求"""
    decision: str = Field(..., max_length=20, description="决定（approve/reject）")
    comments: Optional[str] = Field(None, max_length=1000, description="评论")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    delegate_to: Optional[int] = Field(None, description="委托给")
    escalate_to: Optional[int] = Field(None, description="升级给")
    conditions: Optional[Dict[str, Any]] = Field(None, description="条件")

    @validator('decision')
    def validate_decision(cls, v):
        if v.lower() not in ['approve', 'reject', 'delegate', 'escalate', 'return']:
            raise ValueError('决定必须是 approve, reject, delegate, escalate 或 return 之一')
        return v.lower()


class BulkApprovalRequest(BaseSchema):
    """批量审批请求"""
    request_ids: List[int] = Field(..., min_items=1, description="请求ID列表")
    decision: str = Field(..., max_length=20, description="决定")
    comments: Optional[str] = Field(None, max_length=1000, description="评论")
    force_approve: bool = Field(False, description="强制审批")

    @validator('decision')
    def validate_decision(cls, v):
        if v.lower() not in ['approve', 'reject']:
            raise ValueError('批量操作决定必须是 approve 或 reject')
        return v.lower()


class ApprovalStatisticsResponse(BaseResponse):
    """审批统计响应"""
    total_requests: int = Field(0, description="总请求数")
    pending_requests: int = Field(0, description="待审批请求数")
    approved_requests: int = Field(0, description="已批准请求数")
    rejected_requests: int = Field(0, description="已拒绝请求数")
    overdue_requests: int = Field(0, description="逾期请求数")
    average_approval_time: Optional[Decimal] = Field(None, description="平均审批时间（小时）")
    approval_rate: Optional[Decimal] = Field(None, description="审批通过率")
    sla_compliance_rate: Optional[Decimal] = Field(None, description="SLA合规率")
    top_approval_types: Optional[List[Dict[str, Any]]] = Field(None, description="热门审批类型")
    monthly_trends: Optional[List[Dict[str, Any]]] = Field(None, description="月度趋势")