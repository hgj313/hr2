from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from typing import List, Optional
import enum

from app.core.database import Base


class ProjectStatus(enum.Enum):
    """项目状态枚举"""
    PLANNING = "planning"  # 规划中
    ACTIVE = "active"  # 进行中
    ON_HOLD = "on_hold"  # 暂停
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    ARCHIVED = "archived"  # 已归档


class ProjectPriority(enum.Enum):
    """项目优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    CRITICAL = "critical"  # 紧急


class AssignmentStatus(enum.Enum):
    """分配状态枚举"""
    PENDING = "pending"  # 待确认
    ACTIVE = "active"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class Project(Base):
    """项目表模型"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    objectives = Column(JSONB)  # 项目目标
    
    # 项目基本信息
    client_name = Column(String(200), index=True)
    client_contact = Column(JSONB)  # 客户联系信息
    project_manager_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id"), nullable=False, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False, index=True)
    
    # 项目状态和优先级
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING, index=True)
    priority = Column(Enum(ProjectPriority), nullable=False, default=ProjectPriority.MEDIUM, index=True)
    
    # 时间信息
    planned_start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    planned_end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    actual_start_date = Column(DateTime(timezone=True), index=True)
    actual_end_date = Column(DateTime(timezone=True), index=True)
    
    # 预算信息
    budget = Column(Numeric(15, 2))
    actual_cost = Column(Numeric(15, 2), default=0)
    currency = Column(String(10), default="CNY")
    
    # 资源需求
    required_skills = Column(JSONB)  # 所需技能
    estimated_hours = Column(Integer)  # 预估工时
    actual_hours = Column(Integer, default=0)  # 实际工时
    
    # 项目配置
    settings = Column(JSONB)  # 项目设置
    tags = Column(JSONB)  # 项目标签
    
    # 风险和问题
    risk_level = Column(String(20), default="medium", index=True)
    risks = Column(JSONB)  # 风险列表
    issues = Column(JSONB)  # 问题列表
    
    # 系统字段
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project_manager = relationship("Personnel", foreign_keys=[project_manager_id])
    department = relationship("Department")
    assignments = relationship("ProjectAssignment", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, code={self.code}, status={self.status.value})>"
    
    @property
    def duration_days(self) -> int:
        """计算项目计划持续天数"""
        if self.planned_start_date and self.planned_end_date:
            delta = self.planned_end_date - self.planned_start_date
            return delta.days
        return 0
    
    @property
    def actual_duration_days(self) -> Optional[int]:
        """计算项目实际持续天数"""
        if self.actual_start_date and self.actual_end_date:
            delta = self.actual_end_date - self.actual_start_date
            return delta.days
        return None
    
    @property
    def progress_percentage(self) -> float:
        """计算项目进度百分比"""
        if not self.tasks:
            return 0.0
        
        completed_tasks = sum(1 for task in self.tasks if task.status == 'completed')
        total_tasks = len(self.tasks)
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0
    
    @property
    def budget_utilization(self) -> float:
        """计算预算使用率"""
        if self.budget and self.budget > 0:
            return (float(self.actual_cost or 0) / float(self.budget)) * 100
        return 0.0
    
    @property
    def is_overdue(self) -> bool:
        """检查项目是否逾期"""
        if self.status in [ProjectStatus.COMPLETED, ProjectStatus.CANCELLED, ProjectStatus.ARCHIVED]:
            return False
        return datetime.utcnow() > self.planned_end_date.replace(tzinfo=None)
    
    @property
    def is_over_budget(self) -> bool:
        """检查项目是否超预算"""
        if self.budget:
            return (self.actual_cost or 0) > self.budget
        return False
    
    def get_team_members(self) -> List['Personnel']:
        """获取项目团队成员"""
        return [assignment.personnel for assignment in self.assignments if assignment.status == AssignmentStatus.ACTIVE]
    
    def get_required_skills_summary(self) -> dict:
        """获取所需技能汇总"""
        skills_summary = {}
        if self.required_skills:
            for skill in self.required_skills:
                skill_name = skill.get('name')
                required_level = skill.get('level')
                required_count = skill.get('count', 1)
                skills_summary[skill_name] = {
                    'required_level': required_level,
                    'required_count': required_count,
                    'assigned_count': 0  # 需要通过分配记录计算
                }
        return skills_summary


class ProjectAssignment(Base):
    """项目人员分配表模型"""
    __tablename__ = "project_assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    personnel_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 分配信息
    role = Column(String(100), nullable=False, index=True)  # 项目角色
    responsibilities = Column(JSONB)  # 职责描述
    allocation_percentage = Column(Integer, nullable=False, default=100)  # 分配比例（%）
    hourly_rate = Column(Numeric(8, 2))  # 小时费率
    
    # 时间信息
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # 状态信息
    status = Column(Enum(AssignmentStatus), nullable=False, default=AssignmentStatus.PENDING, index=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at = Column(DateTime(timezone=True))
    
    # 工时统计
    estimated_hours = Column(Integer, default=0)
    actual_hours = Column(Integer, default=0)
    billable_hours = Column(Integer, default=0)
    
    # 评价信息
    performance_rating = Column(String(20))
    feedback = Column(Text)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="assignments")
    personnel = relationship("Personnel", back_populates="project_assignments")
    assigner = relationship("User")
    
    def __repr__(self):
        return f"<ProjectAssignment(id={self.id}, project_id={self.project_id}, personnel_id={self.personnel_id}, role={self.role})>"
    
    @property
    def duration_days(self) -> int:
        """计算分配持续天数"""
        delta = self.end_date - self.start_date
        return delta.days
    
    @property
    def is_active(self) -> bool:
        """检查分配是否活跃"""
        now = datetime.utcnow()
        return (
            self.status == AssignmentStatus.ACTIVE and
            self.start_date.replace(tzinfo=None) <= now <= self.end_date.replace(tzinfo=None)
        )
    
    @property
    def utilization_rate(self) -> float:
        """计算工时利用率"""
        if self.estimated_hours and self.estimated_hours > 0:
            return (self.actual_hours / self.estimated_hours) * 100
        return 0.0
    
    def calculate_cost(self) -> float:
        """计算分配成本"""
        if self.hourly_rate and self.actual_hours:
            return float(self.hourly_rate) * self.actual_hours
        return 0.0


class ProjectMilestone(Base):
    """项目里程碑表模型"""
    __tablename__ = "project_milestones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    planned_date = Column(DateTime(timezone=True), nullable=False, index=True)
    actual_date = Column(DateTime(timezone=True))
    status = Column(String(20), nullable=False, default="pending", index=True)  # pending, completed, delayed
    deliverables = Column(JSONB)  # 交付物
    acceptance_criteria = Column(JSONB)  # 验收标准
    is_critical = Column(Boolean, default=False, index=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="milestones")
    
    def __repr__(self):
        return f"<ProjectMilestone(id={self.id}, name={self.name}, status={self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """检查里程碑是否逾期"""
        if self.status == "completed":
            return False
        return datetime.utcnow() > self.planned_date.replace(tzinfo=None)
    
    @property
    def days_until_due(self) -> int:
        """计算距离截止日期的天数"""
        if self.status == "completed":
            return 0
        delta = self.planned_date.replace(tzinfo=None) - datetime.utcnow()
        return delta.days


class ProjectTask(Base):
    """项目任务表模型"""
    __tablename__ = "project_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    milestone_id = Column(UUID(as_uuid=True), ForeignKey("project_milestones.id"), index=True)
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("project_tasks.id"), index=True)
    
    # 任务基本信息
    name = Column(String(200), nullable=False)
    description = Column(Text)
    task_type = Column(String(50), nullable=False, index=True)  # development, testing, design, etc.
    priority = Column(Enum(ProjectPriority), nullable=False, default=ProjectPriority.MEDIUM, index=True)
    status = Column(String(20), nullable=False, default="todo", index=True)  # todo, in_progress, completed, blocked
    
    # 分配信息
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("personnel.id"), index=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone=True))
    
    # 时间信息
    planned_start_date = Column(DateTime(timezone=True), index=True)
    planned_end_date = Column(DateTime(timezone=True), index=True)
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # 工时信息
    estimated_hours = Column(Integer, default=0)
    actual_hours = Column(Integer, default=0)
    remaining_hours = Column(Integer, default=0)
    
    # 依赖关系
    dependencies = Column(JSONB)  # 依赖的任务ID列表
    
    # 其他信息
    tags = Column(JSONB)
    attachments = Column(JSONB)
    notes = Column(Text)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="tasks")
    milestone = relationship("ProjectMilestone")
    parent_task = relationship("ProjectTask", remote_side=[id], back_populates="subtasks")
    subtasks = relationship("ProjectTask", back_populates="parent_task")
    assignee = relationship("Personnel")
    assigner = relationship("User")
    
    def __repr__(self):
        return f"<ProjectTask(id={self.id}, name={self.name}, status={self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """检查任务是否逾期"""
        if self.status == "completed" or not self.planned_end_date:
            return False
        return datetime.utcnow() > self.planned_end_date.replace(tzinfo=None)
    
    @property
    def progress_percentage(self) -> float:
        """计算任务进度百分比"""
        if self.status == "completed":
            return 100.0
        elif self.status == "in_progress" and self.estimated_hours > 0:
            return (self.actual_hours / self.estimated_hours) * 100
        return 0.0
    
    def can_start(self) -> bool:
        """检查任务是否可以开始"""
        if self.status != "todo":
            return False
        
        # 检查依赖任务是否完成
        if self.dependencies:
            # 这里需要查询依赖任务的状态
            pass
        
        return True


class ProjectDocument(Base):
    """项目文档表模型"""
    __tablename__ = "project_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    document_type = Column(String(50), nullable=False, index=True)  # requirement, design, test, etc.
    file_path = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    version = Column(String(20), default="1.0")
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="documents")
    uploader = relationship("User")
    
    def __repr__(self):
        return f"<ProjectDocument(id={self.id}, name={self.name}, type={self.document_type})>"
    
    @property
    def file_size_mb(self) -> float:
        """获取文件大小（MB）"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0