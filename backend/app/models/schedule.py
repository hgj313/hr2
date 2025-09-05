from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import enum

from app.core.database import Base


class ScheduleStatus(enum.Enum):
    """调度状态枚举"""
    DRAFT = "draft"  # 草稿
    PENDING = "pending"  # 待审批
    APPROVED = "approved"  # 已批准
    ACTIVE = "active"  # 生效中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class AssignmentType(enum.Enum):
    """分配类型枚举"""
    PROJECT = "project"  # 项目分配
    TASK = "task"  # 任务分配
    MEETING = "meeting"  # 会议
    TRAINING = "training"  # 培训
    LEAVE = "leave"  # 请假
    OTHER = "other"  # 其他


class ConflictType(enum.Enum):
    """冲突类型枚举"""
    TIME_OVERLAP = "time_overlap"  # 时间重叠
    RESOURCE_OVERALLOCATION = "resource_overallocation"  # 资源过度分配
    SKILL_MISMATCH = "skill_mismatch"  # 技能不匹配
    AVAILABILITY_CONFLICT = "availability_conflict"  # 可用性冲突
    WORKLOAD_EXCEEDED = "workload_exceeded"  # 工作量超限


class Schedule(Base):
    """调度计划表模型"""
    __tablename__ = "schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # 调度周期
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # 调度范围
    department_ids = Column(JSONB)  # 涉及的部门ID列表
    project_ids = Column(JSONB)  # 涉及的项目ID列表
    
    # 调度状态
    status = Column(Enum(ScheduleStatus), nullable=False, default=ScheduleStatus.DRAFT, index=True)
    version = Column(Integer, nullable=False, default=1)
    
    # 创建和审批信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # 调度配置
    auto_assign_enabled = Column(Boolean, default=False)
    conflict_resolution_rules = Column(JSONB)  # 冲突解决规则
    optimization_criteria = Column(JSONB)  # 优化标准
    
    # 统计信息
    total_assignments = Column(Integer, default=0)
    total_conflicts = Column(Integer, default=0)
    utilization_rate = Column(Numeric(5, 2), default=0)  # 资源利用率
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    assignments = relationship("ScheduleAssignment", back_populates="schedule", cascade="all, delete-orphan")
    conflicts = relationship("ScheduleConflict", back_populates="schedule", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, name={self.name}, status={self.status.value})>"
    
    @property
    def duration_days(self) -> int:
        """计算调度周期天数"""
        delta = self.end_date - self.start_date
        return delta.days
    
    @property
    def is_active(self) -> bool:
        """检查调度是否生效"""
        now = datetime.utcnow()
        return (
            self.status == ScheduleStatus.ACTIVE and
            self.start_date.replace(tzinfo=None) <= now <= self.end_date.replace(tzinfo=None)
        )
    
    def get_personnel_workload(self, personnel_id: str) -> Dict:
        """获取指定人员的工作负荷"""
        workload = {
            'total_hours': 0,
            'assignments_count': 0,
            'utilization_rate': 0.0,
            'assignments': []
        }
        
        for assignment in self.assignments:
            if str(assignment.personnel_id) == personnel_id:
                workload['total_hours'] += assignment.allocated_hours or 0
                workload['assignments_count'] += 1
                workload['assignments'].append(assignment)
        
        # 计算利用率（假设标准工作时间为8小时/天）
        standard_hours = self.duration_days * 8
        if standard_hours > 0:
            workload['utilization_rate'] = (workload['total_hours'] / standard_hours) * 100
        
        return workload
    
    def calculate_overall_utilization(self) -> float:
        """计算整体资源利用率"""
        if not self.assignments:
            return 0.0
        
        total_allocated_hours = sum(assignment.allocated_hours or 0 for assignment in self.assignments)
        unique_personnel = set(assignment.personnel_id for assignment in self.assignments)
        total_available_hours = len(unique_personnel) * self.duration_days * 8
        
        if total_available_hours > 0:
            return (total_allocated_hours / total_available_hours) * 100
        return 0.0


class ScheduleAssignment(Base):
    """调度分配表模型"""
    __tablename__ = "schedule_assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    personnel_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 分配基本信息
    assignment_type = Column(Enum(AssignmentType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 关联对象
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("project_tasks.id"), index=True)
    
    # 时间安排
    start_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    end_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    allocated_hours = Column(Numeric(6, 2))  # 分配工时
    
    # 工作安排
    work_location = Column(String(100))
    remote_work_allowed = Column(Boolean, default=False)
    
    # 优先级和状态
    priority = Column(String(20), nullable=False, default="medium", index=True)
    status = Column(String(20), nullable=False, default="assigned", index=True)  # assigned, confirmed, in_progress, completed, cancelled
    
    # 技能要求
    required_skills = Column(JSONB)
    skill_match_score = Column(Numeric(5, 2))  # 技能匹配分数
    
    # 分配信息
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at = Column(DateTime(timezone=True))
    
    # 自动分配相关
    is_auto_assigned = Column(Boolean, default=False, index=True)
    assignment_score = Column(Numeric(8, 4))  # 分配算法评分
    assignment_reason = Column(Text)  # 分配原因
    
    # 备注和标签
    notes = Column(Text)
    tags = Column(JSONB)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    schedule = relationship("Schedule", back_populates="assignments")
    personnel = relationship("Personnel", back_populates="schedule_assignments")
    project = relationship("Project")
    task = relationship("ProjectTask")
    assigner = relationship("User")
    
    def __repr__(self):
        return f"<ScheduleAssignment(id={self.id}, personnel_id={self.personnel_id}, title={self.title})>"
    
    @property
    def duration_hours(self) -> float:
        """计算分配持续时间（小时）"""
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / 3600
    
    @property
    def is_current(self) -> bool:
        """检查分配是否正在进行"""
        now = datetime.utcnow()
        return (
            self.start_datetime.replace(tzinfo=None) <= now <= self.end_datetime.replace(tzinfo=None) and
            self.status in ['confirmed', 'in_progress']
        )
    
    @property
    def is_overdue(self) -> bool:
        """检查分配是否逾期"""
        if self.status == 'completed':
            return False
        return datetime.utcnow() > self.end_datetime.replace(tzinfo=None)
    
    def calculate_workload_percentage(self, standard_hours_per_day: int = 8) -> float:
        """计算工作负荷百分比"""
        if not self.allocated_hours:
            return 0.0
        
        duration_days = (self.end_datetime.date() - self.start_datetime.date()).days + 1
        total_standard_hours = duration_days * standard_hours_per_day
        
        if total_standard_hours > 0:
            return (float(self.allocated_hours) / total_standard_hours) * 100
        return 0.0


class ScheduleConflict(Base):
    """调度冲突表模型"""
    __tablename__ = "schedule_conflicts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 冲突基本信息
    conflict_type = Column(Enum(ConflictType), nullable=False, index=True)
    severity = Column(String(20), nullable=False, default="medium", index=True)  # low, medium, high, critical
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 涉及的分配
    assignment_ids = Column(JSONB, nullable=False)  # 冲突涉及的分配ID列表
    personnel_ids = Column(JSONB)  # 涉及的人员ID列表
    
    # 冲突详情
    conflict_details = Column(JSONB)  # 冲突详细信息
    suggested_solutions = Column(JSONB)  # 建议解决方案
    
    # 解决状态
    status = Column(String(20), nullable=False, default="open", index=True)  # open, in_progress, resolved, ignored
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    
    # 自动检测信息
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    detection_rule = Column(String(100))  # 检测规则名称
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    schedule = relationship("Schedule", back_populates="conflicts")
    resolver = relationship("User")
    
    def __repr__(self):
        return f"<ScheduleConflict(id={self.id}, type={self.conflict_type.value}, severity={self.severity})>"
    
    @property
    def is_resolved(self) -> bool:
        """检查冲突是否已解决"""
        return self.status in ['resolved', 'ignored']
    
    @property
    def days_since_detected(self) -> int:
        """计算冲突检测后的天数"""
        delta = datetime.utcnow() - self.detected_at.replace(tzinfo=None)
        return delta.days
    
    def get_involved_assignments(self) -> List[str]:
        """获取涉及的分配ID列表"""
        return self.assignment_ids or []
    
    def get_involved_personnel(self) -> List[str]:
        """获取涉及的人员ID列表"""
        return self.personnel_ids or []


class ScheduleTemplate(Base):
    """调度模板表模型"""
    __tablename__ = "schedule_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # 模板类型和分类
    template_type = Column(String(50), nullable=False, index=True)  # weekly, monthly, project, etc.
    category = Column(String(50), index=True)
    
    # 模板配置
    duration_days = Column(Integer, nullable=False)
    working_hours_per_day = Column(Integer, default=8)
    working_days_per_week = Column(Integer, default=5)
    
    # 规则配置
    assignment_rules = Column(JSONB)  # 分配规则
    conflict_rules = Column(JSONB)  # 冲突检测规则
    optimization_rules = Column(JSONB)  # 优化规则
    
    # 默认设置
    default_settings = Column(JSONB)
    
    # 使用统计
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # 创建信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User")
    
    def __repr__(self):
        return f"<ScheduleTemplate(id={self.id}, name={self.name}, type={self.template_type})>"
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()


class ResourceAvailability(Base):
    """资源可用性表模型"""
    __tablename__ = "resource_availability"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    personnel_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 可用性时间范围
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # 可用性类型
    availability_type = Column(String(50), nullable=False, index=True)  # available, unavailable, limited
    reason = Column(String(100))  # 原因：vacation, sick_leave, training, etc.
    
    # 可用性详情
    available_hours_per_day = Column(Numeric(4, 2))  # 每天可用小时数
    capacity_percentage = Column(Integer, default=100)  # 可用容量百分比
    
    # 工作偏好
    preferred_work_location = Column(String(100))
    remote_work_preference = Column(Boolean)
    
    # 技能可用性
    available_skills = Column(JSONB)  # 在此期间可用的技能
    
    # 备注
    notes = Column(Text)
    
    # 创建信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_approved = Column(Boolean, default=False, index=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    personnel = relationship("Personnel")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<ResourceAvailability(id={self.id}, personnel_id={self.personnel_id}, type={self.availability_type})>"
    
    @property
    def duration_days(self) -> int:
        """计算可用性持续天数"""
        delta = self.end_date - self.start_date
        return delta.days
    
    @property
    def is_current(self) -> bool:
        """检查可用性是否当前有效"""
        now = datetime.utcnow()
        return self.start_date.replace(tzinfo=None) <= now <= self.end_date.replace(tzinfo=None)
    
    def calculate_total_available_hours(self) -> float:
        """计算总可用工时"""
        if self.available_hours_per_day:
            return float(self.available_hours_per_day) * self.duration_days
        return 0.0
    
    def overlaps_with(self, start: datetime, end: datetime) -> bool:
        """检查是否与指定时间范围重叠"""
        return not (
            end <= self.start_date.replace(tzinfo=None) or 
            start >= self.end_date.replace(tzinfo=None)
        )


class WorkloadAnalysis(Base):
    """工作负荷分析表模型"""
    __tablename__ = "workload_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    personnel_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 分析周期
    analysis_date = Column(DateTime(timezone=True), nullable=False, index=True)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    
    # 工作负荷统计
    total_assigned_hours = Column(Numeric(8, 2), default=0)
    total_available_hours = Column(Numeric(8, 2), default=0)
    utilization_rate = Column(Numeric(5, 2), default=0)  # 利用率百分比
    
    # 项目分布
    active_projects_count = Column(Integer, default=0)
    project_hours_distribution = Column(JSONB)  # 各项目工时分布
    
    # 技能利用
    skill_utilization = Column(JSONB)  # 技能利用情况
    
    # 工作负荷评估
    workload_status = Column(String(20), index=True)  # underutilized, optimal, overloaded
    stress_level = Column(String(20))  # low, medium, high
    
    # 预测信息
    predicted_utilization = Column(Numeric(5, 2))  # 预测利用率
    capacity_forecast = Column(JSONB)  # 容量预测
    
    # 建议
    recommendations = Column(JSONB)  # 优化建议
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    personnel = relationship("Personnel")
    
    def __repr__(self):
        return f"<WorkloadAnalysis(id={self.id}, personnel_id={self.personnel_id}, utilization={self.utilization_rate}%)>"
    
    @property
    def is_overloaded(self) -> bool:
        """检查是否工作负荷过重"""
        return self.workload_status == 'overloaded' or (self.utilization_rate and self.utilization_rate > 100)
    
    @property
    def is_underutilized(self) -> bool:
        """检查是否利用不足"""
        return self.workload_status == 'underutilized' or (self.utilization_rate and self.utilization_rate < 70)
    
    def get_efficiency_score(self) -> float:
        """计算效率评分"""
        if not self.utilization_rate:
            return 0.0
        
        # 最优利用率范围为80-95%
        optimal_min, optimal_max = 80, 95
        
        if optimal_min <= self.utilization_rate <= optimal_max:
            return 100.0
        elif self.utilization_rate < optimal_min:
            return (self.utilization_rate / optimal_min) * 100
        else:
            # 超过最优范围，效率递减
            excess = self.utilization_rate - optimal_max
            penalty = min(excess * 2, 50)  # 最大扣50分
            return max(100 - penalty, 0)