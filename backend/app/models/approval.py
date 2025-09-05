from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from typing import List, Optional, Dict
import enum

from app.core.database import Base


class ApprovalStatus(enum.Enum):
    """审批状态枚举"""
    DRAFT = "draft"  # 草稿
    SUBMITTED = "submitted"  # 已提交
    PENDING = "pending"  # 待审批
    IN_REVIEW = "in_review"  # 审批中
    APPROVED = "approved"  # 已批准
    REJECTED = "rejected"  # 已拒绝
    CANCELLED = "cancelled"  # 已取消
    EXPIRED = "expired"  # 已过期


class ApprovalType(enum.Enum):
    """审批类型枚举"""
    SCHEDULE_CHANGE = "schedule_change"  # 调度变更
    RESOURCE_ALLOCATION = "resource_allocation"  # 资源分配
    PROJECT_ASSIGNMENT = "project_assignment"  # 项目分配
    LEAVE_REQUEST = "leave_request"  # 请假申请
    OVERTIME_REQUEST = "overtime_request"  # 加班申请
    BUDGET_APPROVAL = "budget_approval"  # 预算审批
    PERSONNEL_CHANGE = "personnel_change"  # 人事变更
    SYSTEM_CONFIG = "system_config"  # 系统配置
    OTHER = "other"  # 其他


class ApprovalPriority(enum.Enum):
    """审批优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


class ApprovalRequest(Base):
    """审批请求表模型"""
    __tablename__ = "approval_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_number = Column(String(50), unique=True, nullable=False, index=True)  # 申请编号
    
    # 申请基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    approval_type = Column(String(50), nullable=False, index=True)
    priority = Column(String(20), nullable=False, default="medium", index=True)
    
    # 申请人信息
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    requester_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), index=True)
    
    # 申请内容
    request_data = Column(JSONB, nullable=False)  # 申请的具体数据
    attachments = Column(JSONB)  # 附件信息
    
    # 关联对象
    related_project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
    related_schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), index=True)
    related_personnel_ids = Column(JSONB)  # 相关人员ID列表
    
    # 审批状态
    status = Column(String(20), nullable=False, default="draft", index=True)
    current_step = Column(Integer, default=0)  # 当前审批步骤
    total_steps = Column(Integer, default=1)  # 总审批步骤数
    
    # 时间信息
    submitted_at = Column(DateTime(timezone=True), index=True)
    expected_approval_date = Column(DateTime(timezone=True))
    actual_approval_date = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))  # 过期时间
    
    # 审批流程配置
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("approval_workflows.id"), index=True)
    approval_rules = Column(JSONB)  # 审批规则
    
    # 影响评估
    impact_assessment = Column(JSONB)  # 影响评估
    risk_level = Column(String(20), default="medium")  # 风险等级
    
    # 成本信息
    estimated_cost = Column(Numeric(15, 2))
    actual_cost = Column(Numeric(15, 2))
    budget_impact = Column(JSONB)  # 预算影响
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    requester = relationship("User", foreign_keys=[requester_id])
    requester_department = relationship("Department")
    related_project = relationship("Project")
    related_schedule = relationship("Schedule")
    workflow = relationship("ApprovalWorkflow")
    steps = relationship("ApprovalStep", back_populates="request", cascade="all, delete-orphan")
    comments = relationship("ApprovalComment", back_populates="request", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ApprovalRequest(id={self.id}, number={self.request_number}, status={self.status})>"
    
    @property
    def is_pending(self) -> bool:
        """检查是否待审批"""
        return self.status in ['submitted', 'pending', 'in_review']
    
    @property
    def is_completed(self) -> bool:
        """检查是否已完成（批准或拒绝）"""
        return self.status in ['approved', 'rejected', 'cancelled', 'expired']
    
    @property
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        if self.expected_approval_date and not self.is_completed:
            return datetime.utcnow() > self.expected_approval_date.replace(tzinfo=None)
        return False
    
    @property
    def is_expired(self) -> bool:
        """检查是否已过期"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at.replace(tzinfo=None)
        return False
    
    @property
    def processing_days(self) -> Optional[int]:
        """计算处理天数"""
        if self.submitted_at:
            end_date = self.actual_approval_date or datetime.utcnow()
            delta = end_date - self.submitted_at.replace(tzinfo=None)
            return delta.days
        return None
    
    def get_current_approvers(self) -> List[str]:
        """获取当前审批人ID列表"""
        current_steps = [step for step in self.steps if step.step_number == self.current_step and step.status == 'pending']
        return [step.approver_id for step in current_steps if step.approver_id]
    
    def get_approval_progress(self) -> float:
        """计算审批进度百分比"""
        if self.total_steps == 0:
            return 0.0
        return (self.current_step / self.total_steps) * 100
    
    def can_be_cancelled(self, user_id: str) -> bool:
        """检查是否可以取消"""
        return (
            not self.is_completed and
            (str(self.requester_id) == user_id or self.has_cancel_permission(user_id))
        )
    
    def has_cancel_permission(self, user_id: str) -> bool:
        """检查用户是否有取消权限"""
        # 这里需要根据业务规则实现权限检查
        return False


class ApprovalStep(Base):
    """审批步骤表模型"""
    __tablename__ = "approval_steps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("approval_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 步骤信息
    step_number = Column(Integer, nullable=False, index=True)
    step_name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # 审批人信息
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    approver_role = Column(String(50))  # 审批角色
    approver_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    
    # 审批配置
    is_required = Column(Boolean, default=True)  # 是否必须审批
    is_parallel = Column(Boolean, default=False)  # 是否并行审批
    approval_type = Column(String(50), default="single")  # single, multiple, consensus
    required_approvers_count = Column(Integer, default=1)  # 需要的审批人数
    
    # 审批状态
    status = Column(String(20), nullable=False, default="pending", index=True)
    decision = Column(String(20))  # approve, reject, delegate
    decision_reason = Column(Text)
    
    # 时间信息
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # 审批结果
    approval_data = Column(JSONB)  # 审批相关数据
    conditions = Column(JSONB)  # 审批条件
    
    # 委托信息
    delegated_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    delegation_reason = Column(Text)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    request = relationship("ApprovalRequest", back_populates="steps")
    approver = relationship("User", foreign_keys=[approver_id])
    approver_department = relationship("Department")
    delegate = relationship("User", foreign_keys=[delegated_to])
    
    def __repr__(self):
        return f"<ApprovalStep(id={self.id}, step={self.step_number}, status={self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        if self.due_date and self.status == 'pending':
            return datetime.utcnow() > self.due_date.replace(tzinfo=None)
        return False
    
    @property
    def processing_hours(self) -> Optional[float]:
        """计算处理时长（小时）"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds() / 3600
        return None
    
    def can_approve(self, user_id: str) -> bool:
        """检查用户是否可以审批"""
        return (
            self.status == 'pending' and
            (str(self.approver_id) == user_id or str(self.delegated_to) == user_id)
        )
    
    def approve(self, user_id: str, reason: str = None, data: dict = None):
        """执行审批"""
        if not self.can_approve(user_id):
            raise ValueError("User cannot approve this step")
        
        self.status = 'completed'
        self.decision = 'approve'
        self.decision_reason = reason
        self.approval_data = data
        self.completed_at = datetime.utcnow()
    
    def reject(self, user_id: str, reason: str):
        """执行拒绝"""
        if not self.can_approve(user_id):
            raise ValueError("User cannot reject this step")
        
        self.status = 'completed'
        self.decision = 'reject'
        self.decision_reason = reason
        self.completed_at = datetime.utcnow()


class ApprovalWorkflow(Base):
    """审批工作流表模型"""
    __tablename__ = "approval_workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # 工作流配置
    approval_type = Column(String(50), nullable=False, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), index=True)
    
    # 工作流定义
    workflow_definition = Column(JSONB, nullable=False)  # 工作流步骤定义
    conditions = Column(JSONB)  # 触发条件
    
    # 审批规则
    auto_approval_rules = Column(JSONB)  # 自动审批规则
    escalation_rules = Column(JSONB)  # 升级规则
    timeout_rules = Column(JSONB)  # 超时规则
    
    # 通知配置
    notification_settings = Column(JSONB)  # 通知设置
    
    # 状态信息
    is_active = Column(Boolean, default=True, index=True)
    version = Column(String(20), default="1.0")
    
    # 创建信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 使用统计
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    department = relationship("Department")
    creator = relationship("User")
    requests = relationship("ApprovalRequest", back_populates="workflow")
    
    def __repr__(self):
        return f"<ApprovalWorkflow(id={self.id}, name={self.name}, type={self.approval_type})>"
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
    
    def get_steps_definition(self) -> List[Dict]:
        """获取步骤定义"""
        return self.workflow_definition.get('steps', []) if self.workflow_definition else []
    
    def is_applicable(self, request_data: Dict) -> bool:
        """检查工作流是否适用于给定请求"""
        if not self.conditions:
            return True
        
        # 这里需要实现条件匹配逻辑
        return True


class ApprovalComment(Base):
    """审批评论表模型"""
    __tablename__ = "approval_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("approval_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    step_id = Column(UUID(as_uuid=True), ForeignKey("approval_steps.id"), index=True)
    
    # 评论信息
    comment_type = Column(String(50), default="general", index=True)  # general, question, suggestion, objection
    content = Column(Text, nullable=False)
    
    # 评论人信息
    commenter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    commenter_role = Column(String(50))  # 评论人角色
    
    # 可见性
    is_internal = Column(Boolean, default=False)  # 是否内部评论
    visibility = Column(String(20), default="all")  # all, approvers, requester
    
    # 附件
    attachments = Column(JSONB)
    
    # 回复信息
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("approval_comments.id"))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    request = relationship("ApprovalRequest", back_populates="comments")
    step = relationship("ApprovalStep")
    commenter = relationship("User")
    parent_comment = relationship("ApprovalComment", remote_side=[id], back_populates="replies")
    replies = relationship("ApprovalComment", back_populates="parent_comment")
    
    def __repr__(self):
        return f"<ApprovalComment(id={self.id}, type={self.comment_type}, commenter_id={self.commenter_id})>"
    
    @property
    def is_reply(self) -> bool:
        """检查是否为回复评论"""
        return self.parent_comment_id is not None
    
    def can_edit(self, user_id: str) -> bool:
        """检查用户是否可以编辑评论"""
        return str(self.commenter_id) == user_id
    
    def can_view(self, user_id: str, user_role: str) -> bool:
        """检查用户是否可以查看评论"""
        if self.visibility == "all":
            return True
        elif self.visibility == "approvers":
            # 需要检查用户是否为审批人
            return user_role in ['approver', 'admin']
        elif self.visibility == "requester":
            # 需要检查用户是否为申请人
            return str(self.request.requester_id) == user_id
        return False


class ApprovalHistory(Base):
    """审批历史表模型"""
    __tablename__ = "approval_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("approval_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 操作信息
    action = Column(String(50), nullable=False, index=True)  # submit, approve, reject, cancel, etc.
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    actor_role = Column(String(50))
    
    # 操作详情
    old_status = Column(String(20))
    new_status = Column(String(20))
    old_data = Column(JSONB)  # 操作前数据
    new_data = Column(JSONB)  # 操作后数据
    
    # 操作原因和备注
    reason = Column(Text)
    notes = Column(Text)
    
    # 系统信息
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # 时间信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    request = relationship("ApprovalRequest")
    actor = relationship("User")
    
    def __repr__(self):
        return f"<ApprovalHistory(id={self.id}, action={self.action}, actor_id={self.actor_id})>"
    
    @classmethod
    def log_action(cls, request_id: str, action: str, actor_id: str, 
                   old_status: str = None, new_status: str = None,
                   old_data: dict = None, new_data: dict = None,
                   reason: str = None, notes: str = None,
                   ip_address: str = None, user_agent: str = None):
        """记录审批操作"""
        history = cls(
            request_id=request_id,
            action=action,
            actor_id=actor_id,
            old_status=old_status,
            new_status=new_status,
            old_data=old_data,
            new_data=new_data,
            reason=reason,
            notes=notes,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return history


class ApprovalDelegate(Base):
    """审批委托表模型"""
    __tablename__ = "approval_delegates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    delegator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    delegate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # 委托范围
    approval_types = Column(JSONB)  # 委托的审批类型
    department_ids = Column(JSONB)  # 委托的部门范围
    amount_limit = Column(Numeric(15, 2))  # 金额限制
    
    # 委托时间
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # 委托原因
    reason = Column(Text)
    
    # 状态
    is_active = Column(Boolean, default=True, index=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    delegator = relationship("User", foreign_keys=[delegator_id])
    delegate = relationship("User", foreign_keys=[delegate_id])
    
    def __repr__(self):
        return f"<ApprovalDelegate(id={self.id}, delegator_id={self.delegator_id}, delegate_id={self.delegate_id})>"
    
    @property
    def is_current(self) -> bool:
        """检查委托是否当前有效"""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        return self.start_date.replace(tzinfo=None) <= now <= self.end_date.replace(tzinfo=None)
    
    def can_approve_type(self, approval_type: str) -> bool:
        """检查是否可以审批指定类型"""
        if not self.approval_types:
            return True  # 如果没有限制，则可以审批所有类型
        return approval_type in self.approval_types
    
    def can_approve_amount(self, amount: float) -> bool:
        """检查是否可以审批指定金额"""
        if not self.amount_limit:
            return True  # 如果没有限制，则可以审批任意金额
        return amount <= float(self.amount_limit)