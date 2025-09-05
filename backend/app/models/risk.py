from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import enum

from app.core.database import Base


class RiskLevel(enum.Enum):
    """风险等级枚举"""
    LOW = "low"  # 低风险
    MEDIUM = "medium"  # 中风险
    HIGH = "high"  # 高风险
    CRITICAL = "critical"  # 严重风险


class RiskType(enum.Enum):
    """风险类型枚举"""
    RESOURCE_SHORTAGE = "resource_shortage"  # 资源短缺
    SCHEDULE_CONFLICT = "schedule_conflict"  # 调度冲突
    SKILL_MISMATCH = "skill_mismatch"  # 技能不匹配
    WORKLOAD_OVERLOAD = "workload_overload"  # 工作负荷过载
    DEADLINE_RISK = "deadline_risk"  # 截止日期风险
    BUDGET_OVERRUN = "budget_overrun"  # 预算超支
    QUALITY_RISK = "quality_risk"  # 质量风险
    COMPLIANCE_RISK = "compliance_risk"  # 合规风险
    PERSONNEL_RISK = "personnel_risk"  # 人员风险
    SYSTEM_RISK = "system_risk"  # 系统风险
    EXTERNAL_RISK = "external_risk"  # 外部风险
    OTHER = "other"  # 其他


class RiskStatus(enum.Enum):
    """风险状态枚举"""
    IDENTIFIED = "identified"  # 已识别
    ASSESSED = "assessed"  # 已评估
    MITIGATING = "mitigating"  # 缓解中
    MONITORING = "monitoring"  # 监控中
    RESOLVED = "resolved"  # 已解决
    ACCEPTED = "accepted"  # 已接受
    ESCALATED = "escalated"  # 已升级


class AlertLevel(enum.Enum):
    """预警等级枚举"""
    INFO = "info"  # 信息
    WARNING = "warning"  # 警告
    ALERT = "alert"  # 告警
    CRITICAL = "critical"  # 严重


class RiskAssessment(Base):
    """风险评估表模型"""
    __tablename__ = "risk_assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assessment_number = Column(String(50), unique=True, nullable=False, index=True)  # 评估编号
    
    # 风险基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    risk_type = Column(String(50), nullable=False, index=True)
    risk_category = Column(String(50), index=True)  # 风险分类
    
    # 风险来源
    source_type = Column(String(50), index=True)  # project, schedule, personnel, system
    source_id = Column(UUID(as_uuid=True), index=True)  # 来源对象ID
    
    # 关联对象
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), index=True)
    affected_personnel_ids = Column(JSONB)  # 受影响人员ID列表
    
    # 风险评估
    probability = Column(Float, nullable=False)  # 发生概率 (0-1)
    impact_score = Column(Float, nullable=False)  # 影响分数 (1-10)
    risk_score = Column(Float, nullable=False, index=True)  # 风险分数 = 概率 * 影响
    risk_level = Column(String(20), nullable=False, index=True)  # 风险等级
    
    # 影响分析
    impact_analysis = Column(JSONB)  # 影响分析详情
    cost_impact = Column(Numeric(15, 2))  # 成本影响
    time_impact = Column(Integer)  # 时间影响（天）
    quality_impact = Column(String(20))  # 质量影响等级
    
    # 风险状态
    status = Column(String(20), nullable=False, default="identified", index=True)
    
    # 评估人员
    assessor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    
    # 时间信息
    identified_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    assessed_at = Column(DateTime(timezone=True))
    review_due_date = Column(DateTime(timezone=True))
    next_review_date = Column(DateTime(timezone=True))
    
    # 风险触发条件
    trigger_conditions = Column(JSONB)  # 触发条件
    monitoring_metrics = Column(JSONB)  # 监控指标
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project")
    schedule = relationship("Schedule")
    department = relationship("Department")
    assessor = relationship("User", foreign_keys=[assessor_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    mitigation_plans = relationship("RiskMitigationPlan", back_populates="risk_assessment", cascade="all, delete-orphan")
    alerts = relationship("RiskAlert", back_populates="risk_assessment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RiskAssessment(id={self.id}, title={self.title}, level={self.risk_level})>"
    
    @property
    def is_high_risk(self) -> bool:
        """检查是否为高风险"""
        return self.risk_level in ['high', 'critical']
    
    @property
    def is_overdue_review(self) -> bool:
        """检查是否逾期复查"""
        if self.next_review_date:
            return datetime.utcnow() > self.next_review_date.replace(tzinfo=None)
        return False
    
    @property
    def days_since_identified(self) -> int:
        """计算识别后天数"""
        delta = datetime.utcnow() - self.identified_at.replace(tzinfo=None)
        return delta.days
    
    def calculate_risk_score(self) -> float:
        """计算风险分数"""
        return self.probability * self.impact_score
    
    def update_risk_level(self):
        """根据风险分数更新风险等级"""
        score = self.calculate_risk_score()
        if score >= 8:
            self.risk_level = "critical"
        elif score >= 6:
            self.risk_level = "high"
        elif score >= 3:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"
        self.risk_score = score
    
    def get_affected_personnel(self) -> List[str]:
        """获取受影响人员ID列表"""
        return self.affected_personnel_ids or []
    
    def add_affected_personnel(self, personnel_id: str):
        """添加受影响人员"""
        if not self.affected_personnel_ids:
            self.affected_personnel_ids = []
        if personnel_id not in self.affected_personnel_ids:
            self.affected_personnel_ids.append(personnel_id)
    
    def schedule_next_review(self, days: int = 30):
        """安排下次复查"""
        self.next_review_date = datetime.utcnow() + timedelta(days=days)


class RiskMitigationPlan(Base):
    """风险缓解计划表模型"""
    __tablename__ = "risk_mitigation_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    risk_assessment_id = Column(UUID(as_uuid=True), ForeignKey("risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 计划基本信息
    plan_name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    strategy_type = Column(String(50), nullable=False, index=True)  # avoid, mitigate, transfer, accept
    
    # 执行信息
    responsible_person_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    backup_person_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    
    # 计划详情
    action_items = Column(JSONB, nullable=False)  # 行动项列表
    resources_required = Column(JSONB)  # 所需资源
    estimated_cost = Column(Numeric(15, 2))  # 预估成本
    estimated_duration = Column(Integer)  # 预估持续时间（天）
    
    # 时间计划
    planned_start_date = Column(DateTime(timezone=True), nullable=False)
    planned_end_date = Column(DateTime(timezone=True), nullable=False)
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # 执行状态
    status = Column(String(20), nullable=False, default="planned", index=True)  # planned, in_progress, completed, cancelled
    progress_percentage = Column(Float, default=0.0)  # 进度百分比
    
    # 效果评估
    effectiveness_score = Column(Float)  # 有效性评分 (1-10)
    residual_risk_level = Column(String(20))  # 剩余风险等级
    lessons_learned = Column(Text)  # 经验教训
    
    # 监控信息
    monitoring_frequency = Column(String(20), default="weekly")  # daily, weekly, monthly
    last_monitored_at = Column(DateTime(timezone=True))
    next_monitoring_date = Column(DateTime(timezone=True))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    risk_assessment = relationship("RiskAssessment", back_populates="mitigation_plans")
    responsible_person = relationship("User", foreign_keys=[responsible_person_id])
    backup_person = relationship("User", foreign_keys=[backup_person_id])
    
    def __repr__(self):
        return f"<RiskMitigationPlan(id={self.id}, name={self.plan_name}, status={self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        if self.planned_end_date and self.status not in ['completed', 'cancelled']:
            return datetime.utcnow() > self.planned_end_date.replace(tzinfo=None)
        return False
    
    @property
    def is_behind_schedule(self) -> bool:
        """检查是否落后于计划"""
        if not self.planned_start_date or not self.planned_end_date:
            return False
        
        now = datetime.utcnow()
        if now < self.planned_start_date.replace(tzinfo=None):
            return False
        
        total_duration = (self.planned_end_date - self.planned_start_date).days
        elapsed_duration = (now - self.planned_start_date.replace(tzinfo=None)).days
        
        if total_duration > 0:
            expected_progress = (elapsed_duration / total_duration) * 100
            return self.progress_percentage < expected_progress - 10  # 10%容差
        
        return False
    
    def update_progress(self, percentage: float, notes: str = None):
        """更新进度"""
        self.progress_percentage = max(0, min(100, percentage))
        if percentage >= 100:
            self.status = "completed"
            self.actual_end_date = datetime.utcnow()
        elif percentage > 0 and self.status == "planned":
            self.status = "in_progress"
            if not self.actual_start_date:
                self.actual_start_date = datetime.utcnow()
    
    def get_action_items(self) -> List[Dict]:
        """获取行动项列表"""
        return self.action_items or []
    
    def add_action_item(self, item: Dict):
        """添加行动项"""
        if not self.action_items:
            self.action_items = []
        self.action_items.append(item)
    
    def schedule_next_monitoring(self):
        """安排下次监控"""
        frequency_days = {
            'daily': 1,
            'weekly': 7,
            'monthly': 30
        }
        days = frequency_days.get(self.monitoring_frequency, 7)
        self.next_monitoring_date = datetime.utcnow() + timedelta(days=days)


class RiskAlert(Base):
    """风险预警表模型"""
    __tablename__ = "risk_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    alert_number = Column(String(50), unique=True, nullable=False, index=True)  # 预警编号
    
    # 预警基本信息
    title = Column(String(200), nullable=False, index=True)
    message = Column(Text, nullable=False)
    alert_level = Column(String(20), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False, index=True)
    
    # 关联风险
    risk_assessment_id = Column(UUID(as_uuid=True), ForeignKey("risk_assessments.id"), index=True)
    
    # 触发信息
    trigger_condition = Column(JSONB)  # 触发条件
    trigger_data = Column(JSONB)  # 触发数据
    threshold_value = Column(Float)  # 阈值
    actual_value = Column(Float)  # 实际值
    
    # 影响范围
    affected_projects = Column(JSONB)  # 受影响项目
    affected_departments = Column(JSONB)  # 受影响部门
    affected_personnel = Column(JSONB)  # 受影响人员
    
    # 预警状态
    status = Column(String(20), nullable=False, default="active", index=True)  # active, acknowledged, resolved, dismissed
    
    # 处理信息
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    
    # 通知信息
    notification_sent = Column(Boolean, default=False)
    notification_recipients = Column(JSONB)  # 通知接收人
    escalation_level = Column(Integer, default=0)  # 升级级别
    
    # 自动处理
    auto_resolve = Column(Boolean, default=False)  # 是否自动解决
    auto_resolve_condition = Column(JSONB)  # 自动解决条件
    
    # 时间信息
    triggered_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # 过期时间
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    risk_assessment = relationship("RiskAssessment", back_populates="alerts")
    assignee = relationship("User", foreign_keys=[assigned_to])
    acknowledger = relationship("User", foreign_keys=[acknowledged_by])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<RiskAlert(id={self.id}, title={self.title}, level={self.alert_level})>"
    
    @property
    def is_critical(self) -> bool:
        """检查是否为严重预警"""
        return self.alert_level == "critical"
    
    @property
    def is_expired(self) -> bool:
        """检查是否已过期"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at.replace(tzinfo=None)
        return False
    
    @property
    def response_time_hours(self) -> Optional[float]:
        """计算响应时间（小时）"""
        if self.acknowledged_at:
            delta = self.acknowledged_at - self.triggered_at
            return delta.total_seconds() / 3600
        return None
    
    @property
    def resolution_time_hours(self) -> Optional[float]:
        """计算解决时间（小时）"""
        if self.resolved_at:
            delta = self.resolved_at - self.triggered_at
            return delta.total_seconds() / 3600
        return None
    
    def acknowledge(self, user_id: str, notes: str = None):
        """确认预警"""
        if self.status == "active":
            self.status = "acknowledged"
            self.acknowledged_by = user_id
            self.acknowledged_at = datetime.utcnow()
            if notes:
                self.resolution_notes = notes
    
    def resolve(self, user_id: str, notes: str):
        """解决预警"""
        if self.status in ["active", "acknowledged"]:
            self.status = "resolved"
            self.resolved_by = user_id
            self.resolved_at = datetime.utcnow()
            self.resolution_notes = notes
    
    def dismiss(self, user_id: str, reason: str):
        """忽略预警"""
        if self.status in ["active", "acknowledged"]:
            self.status = "dismissed"
            self.resolved_by = user_id
            self.resolved_at = datetime.utcnow()
            self.resolution_notes = f"Dismissed: {reason}"
    
    def escalate(self):
        """升级预警"""
        self.escalation_level += 1
        # 这里可以添加升级逻辑，如通知更高级别的管理人员
    
    def get_affected_projects(self) -> List[str]:
        """获取受影响项目ID列表"""
        return self.affected_projects or []
    
    def get_affected_departments(self) -> List[str]:
        """获取受影响部门ID列表"""
        return self.affected_departments or []
    
    def get_affected_personnel(self) -> List[str]:
        """获取受影响人员ID列表"""
        return self.affected_personnel or []


class RiskMonitoringRule(Base):
    """风险监控规则表模型"""
    __tablename__ = "risk_monitoring_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    rule_name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # 规则配置
    rule_type = Column(String(50), nullable=False, index=True)  # threshold, trend, pattern, composite
    risk_type = Column(String(50), nullable=False, index=True)
    
    # 监控条件
    monitoring_conditions = Column(JSONB, nullable=False)  # 监控条件
    threshold_config = Column(JSONB)  # 阈值配置
    
    # 数据源
    data_source = Column(String(50), nullable=False)  # database, api, file, manual
    data_query = Column(Text)  # 数据查询语句
    data_fields = Column(JSONB)  # 数据字段映射
    
    # 执行配置
    check_frequency = Column(String(20), default="hourly")  # minutely, hourly, daily, weekly
    is_active = Column(Boolean, default=True, index=True)
    
    # 预警配置
    alert_level = Column(String(20), default="warning")
    alert_template = Column(Text)  # 预警消息模板
    notification_config = Column(JSONB)  # 通知配置
    
    # 自动处理
    auto_create_mitigation = Column(Boolean, default=False)  # 自动创建缓解计划
    mitigation_template = Column(JSONB)  # 缓解计划模板
    
    # 执行统计
    last_executed_at = Column(DateTime(timezone=True))
    next_execution_at = Column(DateTime(timezone=True))
    execution_count = Column(Integer, default=0)
    alert_count = Column(Integer, default=0)
    
    # 创建信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User")
    
    def __repr__(self):
        return f"<RiskMonitoringRule(id={self.id}, name={self.rule_name}, type={self.rule_type})>"
    
    def schedule_next_execution(self):
        """安排下次执行"""
        frequency_minutes = {
            'minutely': 1,
            'hourly': 60,
            'daily': 1440,
            'weekly': 10080
        }
        minutes = frequency_minutes.get(self.check_frequency, 60)
        self.next_execution_at = datetime.utcnow() + timedelta(minutes=minutes)
    
    def increment_execution_count(self):
        """增加执行次数"""
        self.execution_count += 1
        self.last_executed_at = datetime.utcnow()
        self.schedule_next_execution()
    
    def increment_alert_count(self):
        """增加预警次数"""
        self.alert_count += 1
    
    def is_due_for_execution(self) -> bool:
        """检查是否到执行时间"""
        if not self.is_active:
            return False
        if not self.next_execution_at:
            return True
        return datetime.utcnow() >= self.next_execution_at.replace(tzinfo=None)
    
    def get_monitoring_conditions(self) -> Dict:
        """获取监控条件"""
        return self.monitoring_conditions or {}
    
    def get_threshold_config(self) -> Dict:
        """获取阈值配置"""
        return self.threshold_config or {}


class RiskReport(Base):
    """风险报告表模型"""
    __tablename__ = "risk_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report_number = Column(String(50), unique=True, nullable=False, index=True)  # 报告编号
    
    # 报告基本信息
    title = Column(String(200), nullable=False, index=True)
    report_type = Column(String(50), nullable=False, index=True)  # daily, weekly, monthly, quarterly, annual, ad_hoc
    report_period_start = Column(DateTime(timezone=True), nullable=False)
    report_period_end = Column(DateTime(timezone=True), nullable=False)
    
    # 报告范围
    scope_departments = Column(JSONB)  # 报告范围部门
    scope_projects = Column(JSONB)  # 报告范围项目
    scope_risk_types = Column(JSONB)  # 报告范围风险类型
    
    # 报告内容
    executive_summary = Column(Text)  # 执行摘要
    risk_overview = Column(JSONB)  # 风险概览
    key_findings = Column(JSONB)  # 主要发现
    recommendations = Column(JSONB)  # 建议
    
    # 统计数据
    total_risks = Column(Integer, default=0)
    high_risks = Column(Integer, default=0)
    new_risks = Column(Integer, default=0)
    resolved_risks = Column(Integer, default=0)
    overdue_mitigations = Column(Integer, default=0)
    
    # 趋势分析
    risk_trend_data = Column(JSONB)  # 风险趋势数据
    mitigation_effectiveness = Column(JSONB)  # 缓解有效性
    
    # 报告状态
    status = Column(String(20), nullable=False, default="draft", index=True)  # draft, review, approved, published
    
    # 生成信息
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # 时间信息
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    
    # 文件信息
    report_file_path = Column(String(500))  # 报告文件路径
    report_format = Column(String(20), default="pdf")  # pdf, excel, html
    
    # 分发信息
    distribution_list = Column(JSONB)  # 分发列表
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    generator = relationship("User", foreign_keys=[generated_by])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<RiskReport(id={self.id}, title={self.title}, type={self.report_type})>"
    
    @property
    def is_overdue(self) -> bool:
        """检查报告是否逾期"""
        # 这里可以根据报告类型设置不同的逾期标准
        return False
    
    def approve(self, user_id: str):
        """批准报告"""
        if self.status == "review":
            self.status = "approved"
            self.approved_by = user_id
            self.approved_at = datetime.utcnow()
    
    def publish(self):
        """发布报告"""
        if self.status == "approved":
            self.status = "published"
            self.published_at = datetime.utcnow()
    
    def get_scope_departments(self) -> List[str]:
        """获取报告范围部门"""
        return self.scope_departments or []
    
    def get_scope_projects(self) -> List[str]:
        """获取报告范围项目"""
        return self.scope_projects or []
    
    def get_key_findings(self) -> List[Dict]:
        """获取主要发现"""
        return self.key_findings or []
    
    def get_recommendations(self) -> List[Dict]:
        """获取建议"""
        return self.recommendations or []
    
    def calculate_risk_metrics(self) -> Dict:
        """计算风险指标"""
        return {
            'total_risks': self.total_risks,
            'high_risks': self.high_risks,
            'new_risks': self.new_risks,
            'resolved_risks': self.resolved_risks,
            'overdue_mitigations': self.overdue_mitigations,
            'high_risk_percentage': (self.high_risks / self.total_risks * 100) if self.total_risks > 0 else 0,
            'resolution_rate': (self.resolved_risks / self.total_risks * 100) if self.total_risks > 0 else 0
        }