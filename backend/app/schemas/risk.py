"""风险管控相关的Pydantic模式

本文件定义了风险管控模块的所有数据模型，包括风险评估、风险缓解计划、风险预警、风险监控规则和风险报告等。
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from .base import BaseSchema, TimestampMixin, BaseResponse, DataResponse, ListResponse, PaginatedResponse


class RiskLevel(str, Enum):
    """风险等级枚举"""
    VERY_LOW = "very_low"  # 极低
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    VERY_HIGH = "very_high"  # 极高
    CRITICAL = "critical"  # 严重


class RiskStatus(str, Enum):
    """风险状态枚举"""
    IDENTIFIED = "identified"  # 已识别
    ASSESSED = "assessed"  # 已评估
    MITIGATING = "mitigating"  # 缓解中
    MONITORING = "monitoring"  # 监控中
    CLOSED = "closed"  # 已关闭
    ESCALATED = "escalated"  # 已升级


class RiskCategory(str, Enum):
    """风险类别枚举"""
    OPERATIONAL = "operational"  # 运营风险
    FINANCIAL = "financial"  # 财务风险
    STRATEGIC = "strategic"  # 战略风险
    COMPLIANCE = "compliance"  # 合规风险
    TECHNOLOGY = "technology"  # 技术风险
    HUMAN_RESOURCE = "human_resource"  # 人力资源风险
    ENVIRONMENTAL = "environmental"  # 环境风险
    REPUTATION = "reputation"  # 声誉风险
    SECURITY = "security"  # 安全风险
    PROJECT = "project"  # 项目风险
    MARKET = "market"  # 市场风险
    LEGAL = "legal"  # 法律风险


class RiskImpact(str, Enum):
    """风险影响枚举"""
    NEGLIGIBLE = "negligible"  # 可忽略
    MINOR = "minor"  # 轻微
    MODERATE = "moderate"  # 中等
    MAJOR = "major"  # 重大
    SEVERE = "severe"  # 严重
    CATASTROPHIC = "catastrophic"  # 灾难性


class RiskProbability(str, Enum):
    """风险概率枚举"""
    VERY_UNLIKELY = "very_unlikely"  # 极不可能
    UNLIKELY = "unlikely"  # 不太可能
    POSSIBLE = "possible"  # 可能
    LIKELY = "likely"  # 很可能
    VERY_LIKELY = "very_likely"  # 极可能
    CERTAIN = "certain"  # 确定


class MitigationStatus(str, Enum):
    """缓解状态枚举"""
    PLANNED = "planned"  # 已计划
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    ON_HOLD = "on_hold"  # 暂停
    OVERDUE = "overdue"  # 逾期


class AlertSeverity(str, Enum):
    """预警严重程度枚举"""
    INFO = "info"  # 信息
    WARNING = "warning"  # 警告
    CRITICAL = "critical"  # 严重
    EMERGENCY = "emergency"  # 紧急


class AlertStatus(str, Enum):
    """预警状态枚举"""
    ACTIVE = "active"  # 激活
    ACKNOWLEDGED = "acknowledged"  # 已确认
    RESOLVED = "resolved"  # 已解决
    DISMISSED = "dismissed"  # 已忽略
    ESCALATED = "escalated"  # 已升级


class MonitoringRuleStatus(str, Enum):
    """监控规则状态枚举"""
    ACTIVE = "active"  # 激活
    INACTIVE = "inactive"  # 停用
    TESTING = "testing"  # 测试中
    ARCHIVED = "archived"  # 已归档


class ReportType(str, Enum):
    """报告类型枚举"""
    RISK_ASSESSMENT = "risk_assessment"  # 风险评估报告
    MITIGATION_PROGRESS = "mitigation_progress"  # 缓解进度报告
    COMPLIANCE_STATUS = "compliance_status"  # 合规状态报告
    INCIDENT_ANALYSIS = "incident_analysis"  # 事件分析报告
    TREND_ANALYSIS = "trend_analysis"  # 趋势分析报告
    EXECUTIVE_SUMMARY = "executive_summary"  # 执行摘要
    DETAILED_ANALYSIS = "detailed_analysis"  # 详细分析
    QUARTERLY_REVIEW = "quarterly_review"  # 季度回顾
    ANNUAL_REVIEW = "annual_review"  # 年度回顾


# 风险评估相关模式
class RiskAssessmentBase(BaseSchema):
    """风险评估基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="风险标题")
    description: str = Field(..., min_length=1, max_length=2000, description="风险描述")
    category: RiskCategory = Field(..., description="风险类别")
    probability: RiskProbability = Field(..., description="发生概率")
    impact: RiskImpact = Field(..., description="影响程度")
    risk_level: RiskLevel = Field(..., description="风险等级")
    status: RiskStatus = Field(RiskStatus.IDENTIFIED, description="风险状态")
    risk_score: Decimal = Field(..., ge=0, le=100, description="风险评分")
    inherent_risk_score: Optional[Decimal] = Field(None, ge=0, le=100, description="固有风险评分")
    residual_risk_score: Optional[Decimal] = Field(None, ge=0, le=100, description="剩余风险评分")
    risk_appetite: Optional[Decimal] = Field(None, ge=0, le=100, description="风险偏好")
    risk_tolerance: Optional[Decimal] = Field(None, ge=0, le=100, description="风险容忍度")
    potential_causes: Optional[List[str]] = Field(None, description="潜在原因")
    potential_consequences: Optional[List[str]] = Field(None, description="潜在后果")
    affected_assets: Optional[List[str]] = Field(None, description="受影响资产")
    stakeholders: Optional[List[str]] = Field(None, description="利益相关者")
    regulatory_requirements: Optional[List[str]] = Field(None, description="监管要求")
    assessment_method: Optional[str] = Field(None, max_length=100, description="评估方法")
    assessment_date: date = Field(..., description="评估日期")
    next_review_date: Optional[date] = Field(None, description="下次审查日期")
    assessor_id: int = Field(..., description="评估人ID")
    reviewer_id: Optional[int] = Field(None, description="审查人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    is_active: bool = Field(True, description="是否激活")
    requires_board_attention: bool = Field(False, description="是否需要董事会关注")

    @validator('next_review_date')
    def validate_next_review_date(cls, v, values):
        if v and 'assessment_date' in values and values['assessment_date'] and v <= values['assessment_date']:
            raise ValueError('下次审查日期必须晚于评估日期')
        return v


class RiskAssessmentCreate(RiskAssessmentBase):
    """创建风险评估模式"""
    pass


class RiskAssessmentUpdate(BaseSchema):
    """更新风险评估模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="风险标题")
    description: Optional[str] = Field(None, min_length=1, max_length=2000, description="风险描述")
    category: Optional[RiskCategory] = Field(None, description="风险类别")
    probability: Optional[RiskProbability] = Field(None, description="发生概率")
    impact: Optional[RiskImpact] = Field(None, description="影响程度")
    risk_level: Optional[RiskLevel] = Field(None, description="风险等级")
    status: Optional[RiskStatus] = Field(None, description="风险状态")
    risk_score: Optional[Decimal] = Field(None, ge=0, le=100, description="风险评分")
    inherent_risk_score: Optional[Decimal] = Field(None, ge=0, le=100, description="固有风险评分")
    residual_risk_score: Optional[Decimal] = Field(None, ge=0, le=100, description="剩余风险评分")
    risk_appetite: Optional[Decimal] = Field(None, ge=0, le=100, description="风险偏好")
    risk_tolerance: Optional[Decimal] = Field(None, ge=0, le=100, description="风险容忍度")
    potential_causes: Optional[List[str]] = Field(None, description="潜在原因")
    potential_consequences: Optional[List[str]] = Field(None, description="潜在后果")
    affected_assets: Optional[List[str]] = Field(None, description="受影响资产")
    stakeholders: Optional[List[str]] = Field(None, description="利益相关者")
    regulatory_requirements: Optional[List[str]] = Field(None, description="监管要求")
    assessment_method: Optional[str] = Field(None, max_length=100, description="评估方法")
    assessment_date: Optional[date] = Field(None, description="评估日期")
    next_review_date: Optional[date] = Field(None, description="下次审查日期")
    reviewer_id: Optional[int] = Field(None, description="审查人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    is_active: Optional[bool] = Field(None, description="是否激活")
    requires_board_attention: Optional[bool] = Field(None, description="是否需要董事会关注")


class RiskAssessmentResponse(RiskAssessmentBase, TimestampMixin):
    """风险评估响应模式"""
    id: int = Field(..., description="评估ID")
    assessor_name: Optional[str] = Field(None, description="评估人姓名")
    reviewer_name: Optional[str] = Field(None, description="审查人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    project_name: Optional[str] = Field(None, description="关联项目名称")
    days_since_assessment: Optional[int] = Field(None, description="评估后天数")
    days_until_review: Optional[int] = Field(None, description="距离审查天数")
    is_overdue_review: bool = Field(False, description="是否逾期审查")
    mitigation_plan_count: int = Field(0, description="缓解计划数量")
    alert_count: int = Field(0, description="预警数量")
    risk_trend: Optional[str] = Field(None, description="风险趋势")
    last_updated_by: Optional[str] = Field(None, description="最后更新人")

    class Config:
        from_attributes = True


# 风险缓解计划相关模式
class RiskMitigationPlanBase(BaseSchema):
    """风险缓解计划基础模式"""
    risk_assessment_id: int = Field(..., description="风险评估ID")
    title: str = Field(..., min_length=1, max_length=200, description="计划标题")
    description: str = Field(..., min_length=1, max_length=2000, description="计划描述")
    mitigation_strategy: str = Field(..., max_length=100, description="缓解策略")
    action_items: List[Dict[str, Any]] = Field(..., description="行动项目")
    status: MitigationStatus = Field(MitigationStatus.PLANNED, description="缓解状态")
    priority: str = Field("medium", max_length=20, description="优先级")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="预估成本")
    actual_cost: Optional[Decimal] = Field(None, ge=0, description="实际成本")
    estimated_effort_hours: Optional[int] = Field(None, ge=0, description="预估工时")
    actual_effort_hours: Optional[int] = Field(None, ge=0, description="实际工时")
    start_date: date = Field(..., description="开始日期")
    target_completion_date: date = Field(..., description="目标完成日期")
    actual_completion_date: Optional[date] = Field(None, description="实际完成日期")
    responsible_person_id: int = Field(..., description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    success_criteria: Optional[List[str]] = Field(None, description="成功标准")
    kpis: Optional[List[Dict[str, Any]]] = Field(None, description="关键绩效指标")
    dependencies: Optional[List[str]] = Field(None, description="依赖项")
    risks: Optional[List[str]] = Field(None, description="计划风险")
    contingency_plan: Optional[str] = Field(None, max_length=1000, description="应急计划")
    progress_percentage: Decimal = Field(0, ge=0, le=100, description="进度百分比")
    effectiveness_rating: Optional[Decimal] = Field(None, ge=0, le=10, description="有效性评级")
    lessons_learned: Optional[str] = Field(None, max_length=1000, description="经验教训")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    is_active: bool = Field(True, description="是否激活")

    @validator('target_completion_date')
    def validate_target_completion_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('目标完成日期必须晚于开始日期')
        return v

    @validator('actual_completion_date')
    def validate_actual_completion_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('实际完成日期不能早于开始日期')
        return v


class RiskMitigationPlanCreate(RiskMitigationPlanBase):
    """创建风险缓解计划模式"""
    pass


class RiskMitigationPlanUpdate(BaseSchema):
    """更新风险缓解计划模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="计划标题")
    description: Optional[str] = Field(None, min_length=1, max_length=2000, description="计划描述")
    mitigation_strategy: Optional[str] = Field(None, max_length=100, description="缓解策略")
    action_items: Optional[List[Dict[str, Any]]] = Field(None, description="行动项目")
    status: Optional[MitigationStatus] = Field(None, description="缓解状态")
    priority: Optional[str] = Field(None, max_length=20, description="优先级")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="预估成本")
    actual_cost: Optional[Decimal] = Field(None, ge=0, description="实际成本")
    estimated_effort_hours: Optional[int] = Field(None, ge=0, description="预估工时")
    actual_effort_hours: Optional[int] = Field(None, ge=0, description="实际工时")
    start_date: Optional[date] = Field(None, description="开始日期")
    target_completion_date: Optional[date] = Field(None, description="目标完成日期")
    actual_completion_date: Optional[date] = Field(None, description="实际完成日期")
    responsible_person_id: Optional[int] = Field(None, description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    success_criteria: Optional[List[str]] = Field(None, description="成功标准")
    kpis: Optional[List[Dict[str, Any]]] = Field(None, description="关键绩效指标")
    dependencies: Optional[List[str]] = Field(None, description="依赖项")
    risks: Optional[List[str]] = Field(None, description="计划风险")
    contingency_plan: Optional[str] = Field(None, max_length=1000, description="应急计划")
    progress_percentage: Optional[Decimal] = Field(None, ge=0, le=100, description="进度百分比")
    effectiveness_rating: Optional[Decimal] = Field(None, ge=0, le=10, description="有效性评级")
    lessons_learned: Optional[str] = Field(None, max_length=1000, description="经验教训")
    attachments: Optional[List[str]] = Field(None, description="附件列表")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RiskMitigationPlanResponse(RiskMitigationPlanBase, TimestampMixin):
    """风险缓解计划响应模式"""
    id: int = Field(..., description="计划ID")
    risk_title: Optional[str] = Field(None, description="风险标题")
    risk_level: Optional[RiskLevel] = Field(None, description="风险等级")
    responsible_person_name: Optional[str] = Field(None, description="负责人姓名")
    stakeholder_names: Optional[List[str]] = Field(None, description="利益相关者姓名")
    days_remaining: Optional[int] = Field(None, description="剩余天数")
    is_overdue: bool = Field(False, description="是否逾期")
    budget_variance: Optional[Decimal] = Field(None, description="预算差异")
    effort_variance: Optional[int] = Field(None, description="工时差异")
    completion_rate: Optional[Decimal] = Field(None, description="完成率")
    risk_reduction_percentage: Optional[Decimal] = Field(None, description="风险降低百分比")
    last_status_update: Optional[datetime] = Field(None, description="最后状态更新时间")

    class Config:
        from_attributes = True


# 风险预警相关模式
class RiskAlertBase(BaseSchema):
    """风险预警基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="预警标题")
    description: str = Field(..., min_length=1, max_length=2000, description="预警描述")
    severity: AlertSeverity = Field(..., description="严重程度")
    status: AlertStatus = Field(AlertStatus.ACTIVE, description="预警状态")
    alert_type: str = Field(..., max_length=50, description="预警类型")
    source: str = Field(..., max_length=100, description="预警来源")
    risk_assessment_id: Optional[int] = Field(None, description="关联风险评估ID")
    monitoring_rule_id: Optional[int] = Field(None, description="监控规则ID")
    threshold_value: Optional[Decimal] = Field(None, description="阈值")
    current_value: Optional[Decimal] = Field(None, description="当前值")
    trigger_conditions: Optional[Dict[str, Any]] = Field(None, description="触发条件")
    affected_systems: Optional[List[str]] = Field(None, description="受影响系统")
    recommended_actions: Optional[List[str]] = Field(None, description="建议行动")
    escalation_level: int = Field(1, ge=1, le=5, description="升级级别")
    auto_resolve: bool = Field(False, description="是否自动解决")
    resolution_deadline: Optional[datetime] = Field(None, description="解决截止时间")
    assigned_to: Optional[int] = Field(None, description="分配给")
    notification_sent: bool = Field(False, description="是否已发送通知")
    acknowledgment_required: bool = Field(True, description="是否需要确认")
    acknowledged_by: Optional[int] = Field(None, description="确认人ID")
    acknowledged_at: Optional[datetime] = Field(None, description="确认时间")
    resolved_by: Optional[int] = Field(None, description="解决人ID")
    resolved_at: Optional[datetime] = Field(None, description="解决时间")
    resolution_notes: Optional[str] = Field(None, max_length=1000, description="解决备注")
    false_positive: bool = Field(False, description="是否误报")
    recurrence_count: int = Field(0, ge=0, description="重复次数")
    last_occurrence: Optional[datetime] = Field(None, description="最后发生时间")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: bool = Field(True, description="是否激活")


class RiskAlertCreate(RiskAlertBase):
    """创建风险预警模式"""
    pass


class RiskAlertUpdate(BaseSchema):
    """更新风险预警模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="预警标题")
    description: Optional[str] = Field(None, min_length=1, max_length=2000, description="预警描述")
    severity: Optional[AlertSeverity] = Field(None, description="严重程度")
    status: Optional[AlertStatus] = Field(None, description="预警状态")
    alert_type: Optional[str] = Field(None, max_length=50, description="预警类型")
    source: Optional[str] = Field(None, max_length=100, description="预警来源")
    threshold_value: Optional[Decimal] = Field(None, description="阈值")
    current_value: Optional[Decimal] = Field(None, description="当前值")
    trigger_conditions: Optional[Dict[str, Any]] = Field(None, description="触发条件")
    affected_systems: Optional[List[str]] = Field(None, description="受影响系统")
    recommended_actions: Optional[List[str]] = Field(None, description="建议行动")
    escalation_level: Optional[int] = Field(None, ge=1, le=5, description="升级级别")
    auto_resolve: Optional[bool] = Field(None, description="是否自动解决")
    resolution_deadline: Optional[datetime] = Field(None, description="解决截止时间")
    assigned_to: Optional[int] = Field(None, description="分配给")
    acknowledgment_required: Optional[bool] = Field(None, description="是否需要确认")
    resolution_notes: Optional[str] = Field(None, max_length=1000, description="解决备注")
    false_positive: Optional[bool] = Field(None, description="是否误报")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RiskAlertResponse(RiskAlertBase, TimestampMixin):
    """风险预警响应模式"""
    id: int = Field(..., description="预警ID")
    risk_title: Optional[str] = Field(None, description="关联风险标题")
    monitoring_rule_name: Optional[str] = Field(None, description="监控规则名称")
    assigned_to_name: Optional[str] = Field(None, description="分配人姓名")
    acknowledged_by_name: Optional[str] = Field(None, description="确认人姓名")
    resolved_by_name: Optional[str] = Field(None, description="解决人姓名")
    duration_minutes: Optional[int] = Field(None, description="持续时间（分钟）")
    response_time_minutes: Optional[int] = Field(None, description="响应时间（分钟）")
    resolution_time_minutes: Optional[int] = Field(None, description="解决时间（分钟）")
    is_overdue: bool = Field(False, description="是否逾期")
    sla_breach: bool = Field(False, description="是否违反SLA")
    impact_score: Optional[Decimal] = Field(None, description="影响评分")
    trend_direction: Optional[str] = Field(None, description="趋势方向")

    class Config:
        from_attributes = True


# 风险监控规则相关模式
class RiskMonitoringRuleBase(BaseSchema):
    """风险监控规则基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="规则名称")
    description: str = Field(..., min_length=1, max_length=1000, description="规则描述")
    rule_type: str = Field(..., max_length=50, description="规则类型")
    status: MonitoringRuleStatus = Field(MonitoringRuleStatus.ACTIVE, description="规则状态")
    conditions: Dict[str, Any] = Field(..., description="监控条件")
    thresholds: Dict[str, Any] = Field(..., description="阈值设置")
    data_sources: List[str] = Field(..., description="数据源")
    monitoring_frequency: str = Field(..., max_length=50, description="监控频率")
    alert_template: Dict[str, Any] = Field(..., description="预警模板")
    escalation_rules: Optional[Dict[str, Any]] = Field(None, description="升级规则")
    notification_settings: Optional[Dict[str, Any]] = Field(None, description="通知设置")
    auto_remediation: Optional[Dict[str, Any]] = Field(None, description="自动修复")
    risk_category: Optional[RiskCategory] = Field(None, description="风险类别")
    business_impact: Optional[str] = Field(None, max_length=100, description="业务影响")
    compliance_requirement: Optional[str] = Field(None, max_length=200, description="合规要求")
    owner_id: int = Field(..., description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    effective_date: date = Field(..., description="生效日期")
    expiry_date: Optional[date] = Field(None, description="失效日期")
    last_execution: Optional[datetime] = Field(None, description="最后执行时间")
    next_execution: Optional[datetime] = Field(None, description="下次执行时间")
    execution_count: int = Field(0, ge=0, description="执行次数")
    alert_count: int = Field(0, ge=0, description="预警次数")
    false_positive_count: int = Field(0, ge=0, description="误报次数")
    accuracy_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="准确率")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: bool = Field(True, description="是否激活")

    @validator('expiry_date')
    def validate_expiry_date(cls, v, values):
        if v and 'effective_date' in values and values['effective_date'] and v <= values['effective_date']:
            raise ValueError('失效日期必须晚于生效日期')
        return v


class RiskMonitoringRuleCreate(RiskMonitoringRuleBase):
    """创建风险监控规则模式"""
    pass


class RiskMonitoringRuleUpdate(BaseSchema):
    """更新风险监控规则模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="规则名称")
    description: Optional[str] = Field(None, min_length=1, max_length=1000, description="规则描述")
    rule_type: Optional[str] = Field(None, max_length=50, description="规则类型")
    status: Optional[MonitoringRuleStatus] = Field(None, description="规则状态")
    conditions: Optional[Dict[str, Any]] = Field(None, description="监控条件")
    thresholds: Optional[Dict[str, Any]] = Field(None, description="阈值设置")
    data_sources: Optional[List[str]] = Field(None, description="数据源")
    monitoring_frequency: Optional[str] = Field(None, max_length=50, description="监控频率")
    alert_template: Optional[Dict[str, Any]] = Field(None, description="预警模板")
    escalation_rules: Optional[Dict[str, Any]] = Field(None, description="升级规则")
    notification_settings: Optional[Dict[str, Any]] = Field(None, description="通知设置")
    auto_remediation: Optional[Dict[str, Any]] = Field(None, description="自动修复")
    risk_category: Optional[RiskCategory] = Field(None, description="风险类别")
    business_impact: Optional[str] = Field(None, max_length=100, description="业务影响")
    compliance_requirement: Optional[str] = Field(None, max_length=200, description="合规要求")
    owner_id: Optional[int] = Field(None, description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    effective_date: Optional[date] = Field(None, description="生效日期")
    expiry_date: Optional[date] = Field(None, description="失效日期")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RiskMonitoringRuleResponse(RiskMonitoringRuleBase, TimestampMixin):
    """风险监控规则响应模式"""
    id: int = Field(..., description="规则ID")
    owner_name: Optional[str] = Field(None, description="负责人姓名")
    stakeholder_names: Optional[List[str]] = Field(None, description="利益相关者姓名")
    days_since_last_execution: Optional[int] = Field(None, description="距离最后执行天数")
    days_until_expiry: Optional[int] = Field(None, description="距离失效天数")
    is_expired: bool = Field(False, description="是否已失效")
    performance_score: Optional[Decimal] = Field(None, description="性能评分")
    reliability_score: Optional[Decimal] = Field(None, description="可靠性评分")
    average_execution_time: Optional[Decimal] = Field(None, description="平均执行时间")
    last_alert_time: Optional[datetime] = Field(None, description="最后预警时间")
    health_status: Optional[str] = Field(None, description="健康状态")

    class Config:
        from_attributes = True


# 风险报告相关模式
class RiskReportBase(BaseSchema):
    """风险报告基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="报告标题")
    description: Optional[str] = Field(None, max_length=1000, description="报告描述")
    report_type: ReportType = Field(..., description="报告类型")
    report_period_start: date = Field(..., description="报告期间开始")
    report_period_end: date = Field(..., description="报告期间结束")
    scope: Optional[str] = Field(None, max_length=500, description="报告范围")
    methodology: Optional[str] = Field(None, max_length=500, description="方法论")
    key_findings: Optional[List[str]] = Field(None, description="关键发现")
    recommendations: Optional[List[str]] = Field(None, description="建议")
    risk_summary: Optional[Dict[str, Any]] = Field(None, description="风险摘要")
    metrics: Optional[Dict[str, Any]] = Field(None, description="指标")
    charts_data: Optional[Dict[str, Any]] = Field(None, description="图表数据")
    executive_summary: Optional[str] = Field(None, max_length=2000, description="执行摘要")
    detailed_analysis: Optional[str] = Field(None, description="详细分析")
    appendices: Optional[List[Dict[str, Any]]] = Field(None, description="附录")
    data_sources: Optional[List[str]] = Field(None, description="数据源")
    limitations: Optional[str] = Field(None, max_length=1000, description="局限性")
    next_steps: Optional[List[str]] = Field(None, description="下一步行动")
    author_id: int = Field(..., description="作者ID")
    reviewers: Optional[List[int]] = Field(None, description="审查人ID列表")
    approval_status: str = Field("draft", max_length=20, description="审批状态")
    approved_by: Optional[int] = Field(None, description="批准人ID")
    approved_at: Optional[datetime] = Field(None, description="批准时间")
    published_at: Optional[datetime] = Field(None, description="发布时间")
    distribution_list: Optional[List[str]] = Field(None, description="分发列表")
    confidentiality_level: str = Field("internal", max_length=20, description="保密级别")
    retention_period: Optional[int] = Field(None, ge=0, description="保留期限（天）")
    file_path: Optional[str] = Field(None, max_length=500, description="文件路径")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小")
    version: str = Field("1.0", max_length=20, description="版本号")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: bool = Field(True, description="是否激活")

    @validator('report_period_end')
    def validate_report_period_end(cls, v, values):
        if v and 'report_period_start' in values and values['report_period_start'] and v <= values['report_period_start']:
            raise ValueError('报告期间结束日期必须晚于开始日期')
        return v


class RiskReportCreate(RiskReportBase):
    """创建风险报告模式"""
    pass


class RiskReportUpdate(BaseSchema):
    """更新风险报告模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="报告标题")
    description: Optional[str] = Field(None, max_length=1000, description="报告描述")
    report_type: Optional[ReportType] = Field(None, description="报告类型")
    report_period_start: Optional[date] = Field(None, description="报告期间开始")
    report_period_end: Optional[date] = Field(None, description="报告期间结束")
    scope: Optional[str] = Field(None, max_length=500, description="报告范围")
    methodology: Optional[str] = Field(None, max_length=500, description="方法论")
    key_findings: Optional[List[str]] = Field(None, description="关键发现")
    recommendations: Optional[List[str]] = Field(None, description="建议")
    risk_summary: Optional[Dict[str, Any]] = Field(None, description="风险摘要")
    metrics: Optional[Dict[str, Any]] = Field(None, description="指标")
    charts_data: Optional[Dict[str, Any]] = Field(None, description="图表数据")
    executive_summary: Optional[str] = Field(None, max_length=2000, description="执行摘要")
    detailed_analysis: Optional[str] = Field(None, description="详细分析")
    appendices: Optional[List[Dict[str, Any]]] = Field(None, description="附录")
    data_sources: Optional[List[str]] = Field(None, description="数据源")
    limitations: Optional[str] = Field(None, max_length=1000, description="局限性")
    next_steps: Optional[List[str]] = Field(None, description="下一步行动")
    reviewers: Optional[List[int]] = Field(None, description="审查人ID列表")
    approval_status: Optional[str] = Field(None, max_length=20, description="审批状态")
    distribution_list: Optional[List[str]] = Field(None, description="分发列表")
    confidentiality_level: Optional[str] = Field(None, max_length=20, description="保密级别")
    retention_period: Optional[int] = Field(None, ge=0, description="保留期限（天）")
    file_path: Optional[str] = Field(None, max_length=500, description="文件路径")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小")
    version: Optional[str] = Field(None, max_length=20, description="版本号")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RiskReportResponse(RiskReportBase, TimestampMixin):
    """风险报告响应模式"""
    id: int = Field(..., description="报告ID")
    author_name: Optional[str] = Field(None, description="作者姓名")
    reviewer_names: Optional[List[str]] = Field(None, description="审查人姓名")
    approver_name: Optional[str] = Field(None, description="批准人姓名")
    days_since_published: Optional[int] = Field(None, description="发布后天数")
    download_count: int = Field(0, description="下载次数")
    view_count: int = Field(0, description="查看次数")
    feedback_count: int = Field(0, description="反馈数量")
    average_rating: Optional[Decimal] = Field(None, description="平均评分")
    is_expired: bool = Field(False, description="是否已过期")
    file_exists: bool = Field(True, description="文件是否存在")
    last_accessed: Optional[datetime] = Field(None, description="最后访问时间")

    class Config:
        from_attributes = True


# 响应模式
class RiskAssessmentListResponse(ListResponse[RiskAssessmentResponse]):
    """风险评估列表响应"""
    pass


class RiskAssessmentPaginatedResponse(PaginatedResponse[RiskAssessmentResponse]):
    """风险评估分页响应"""
    pass


class RiskMitigationPlanListResponse(ListResponse[RiskMitigationPlanResponse]):
    """风险缓解计划列表响应"""
    pass


class RiskAlertListResponse(ListResponse[RiskAlertResponse]):
    """风险预警列表响应"""
    pass


class RiskMonitoringRuleListResponse(ListResponse[RiskMonitoringRuleResponse]):
    """风险监控规则列表响应"""
    pass


class RiskReportListResponse(ListResponse[RiskReportResponse]):
    """风险报告列表响应"""
    pass


# 特殊请求模式
class RiskAlertResolveRequest(BaseSchema):
    """风险预警解决请求"""
    resolution_notes: str = Field(..., min_length=1, max_length=1000, description="解决备注")
    false_positive: bool = Field(False, description="是否误报")
    preventive_actions: Optional[List[str]] = Field(None, description="预防措施")
    lessons_learned: Optional[str] = Field(None, max_length=500, description="经验教训")


class BulkRiskActionRequest(BaseSchema):
    """批量风险操作请求"""
    risk_ids: List[int] = Field(..., min_items=1, description="风险ID列表")
    action: str = Field(..., max_length=50, description="操作类型")
    parameters: Optional[Dict[str, Any]] = Field(None, description="操作参数")
    reason: Optional[str] = Field(None, max_length=500, description="操作原因")

    @validator('action')
    def validate_action(cls, v):
        allowed_actions = ['activate', 'deactivate', 'archive', 'escalate', 'assign', 'update_status']
        if v.lower() not in allowed_actions:
            raise ValueError(f'操作类型必须是 {allowed_actions} 之一')
        return v.lower()


class RiskStatisticsResponse(BaseResponse):
    """风险统计响应"""
    total_risks: int = Field(0, description="总风险数")
    high_risks: int = Field(0, description="高风险数")
    medium_risks: int = Field(0, description="中风险数")
    low_risks: int = Field(0, description="低风险数")
    active_mitigations: int = Field(0, description="活跃缓解计划数")
    active_alerts: int = Field(0, description="活跃预警数")
    overdue_mitigations: int = Field(0, description="逾期缓解计划数")
    average_risk_score: Optional[Decimal] = Field(None, description="平均风险评分")
    risk_trend: Optional[str] = Field(None, description="风险趋势")
    compliance_rate: Optional[Decimal] = Field(None, description="合规率")
    mitigation_effectiveness: Optional[Decimal] = Field(None, description="缓解有效性")
    alert_response_time: Optional[Decimal] = Field(None, description="预警响应时间")
    top_risk_categories: Optional[List[Dict[str, Any]]] = Field(None, description="热门风险类别")
    monthly_trends: Optional[List[Dict[str, Any]]] = Field(None, description="月度趋势")
    department_breakdown: Optional[List[Dict[str, Any]]] = Field(None, description="部门分解")