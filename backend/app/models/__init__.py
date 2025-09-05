"""数据模型模块

本模块包含人力资源调度系统的所有数据模型定义。
"""

# 导入基础模型
from app.core.database import Base

# 导入认证相关模型
from app.models.auth import (
    User,
    Role,
    Permission,
    UserRole,
    RolePermission,
    UserSession,
    LoginAttempt,
    PasswordResetToken,
    EmailVerificationToken,
    ApiKey
)

# 导入组织架构相关模型
from app.models.organization import (
    Department,
    Position,
    Personnel,
    PersonnelHistory,
    WorkLocation
)

# 导入项目管理相关模型
from app.models.project import (
    Project,
    ProjectAssignment,
    ProjectMilestone,
    ProjectTask,
    ProjectDocument,
    ProjectStatus,
    ProjectPriority,
    AssignmentStatus,
    TaskStatus,
    TaskPriority
)

# 导入调度管理相关模型
from app.models.schedule import (
    Schedule,
    ScheduleAssignment,
    ScheduleConflict,
    ScheduleTemplate,
    ResourceAvailability,
    WorkloadAnalysis,
    ScheduleStatus,
    AssignmentType,
    ConflictType,
    AvailabilityStatus
)

# 导入审批流程相关模型
from app.models.approval import (
    ApprovalRequest,
    ApprovalStep,
    ApprovalWorkflow,
    ApprovalComment,
    ApprovalHistory,
    ApprovalDelegate,
    ApprovalStatus,
    ApprovalType,
    ApprovalPriority
)

# 导入风险管控相关模型
from app.models.risk import (
    RiskAssessment,
    RiskMitigationPlan,
    RiskAlert,
    RiskMonitoringRule,
    RiskReport,
    RiskLevel,
    RiskType,
    RiskStatus,
    AlertLevel
)

# 导入数据分析相关模型
from app.models.analytics import (
    AnalyticsReport,
    Dashboard,
    DashboardWidget,
    DashboardReport,
    DataMetric,
    MetricValue,
    ReportTemplate,
    ReportType,
    ReportStatus,
    DataSource,
    ChartType
)

# 所有模型类列表
__all__ = [
    # 基础
    "Base",
    
    # 认证模型
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "UserSession",
    "LoginAttempt",
    "PasswordResetToken",
    "EmailVerificationToken",
    "ApiKey",
    
    # 组织架构模型
    "Department",
    "Position",
    "Personnel",
    "PersonnelHistory",
    "WorkLocation",
    
    # 项目管理模型
    "Project",
    "ProjectAssignment",
    "ProjectMilestone",
    "ProjectTask",
    "ProjectDocument",
    "ProjectStatus",
    "ProjectPriority",
    "AssignmentStatus",
    "TaskStatus",
    "TaskPriority",
    
    # 调度管理模型
    "Schedule",
    "ScheduleAssignment",
    "ScheduleConflict",
    "ScheduleTemplate",
    "ResourceAvailability",
    "WorkloadAnalysis",
    "ScheduleStatus",
    "AssignmentType",
    "ConflictType",
    "AvailabilityStatus",
    
    # 审批流程模型
    "ApprovalRequest",
    "ApprovalStep",
    "ApprovalWorkflow",
    "ApprovalComment",
    "ApprovalHistory",
    "ApprovalDelegate",
    "ApprovalStatus",
    "ApprovalType",
    "ApprovalPriority",
    
    # 风险管控模型
    "RiskAssessment",
    "RiskMitigationPlan",
    "RiskAlert",
    "RiskMonitoringRule",
    "RiskReport",
    "RiskLevel",
    "RiskType",
    "RiskStatus",
    "AlertLevel",
    
    # 数据分析模型
    "AnalyticsReport",
    "Dashboard",
    "DashboardWidget",
    "DashboardReport",
    "DataMetric",
    "MetricValue",
    "ReportTemplate",
    "ReportType",
    "ReportStatus",
    "DataSource",
    "ChartType",
]


def get_all_models():
    """获取所有模型类的列表
    
    Returns:
        List: 所有继承自Base的模型类列表
    """
    return [
        # 认证模型
        User, Role, Permission, UserRole, RolePermission,
        UserSession, LoginAttempt, PasswordResetToken, EmailVerificationToken, ApiKey,
        
        # 组织架构模型
        Department, Position, Personnel, PersonnelHistory, WorkLocation,
        
        # 项目管理模型
        Project, ProjectAssignment, ProjectMilestone, ProjectTask, ProjectDocument,
        
        # 调度管理模型
        Schedule, ScheduleAssignment, ScheduleConflict, ScheduleTemplate,
        ResourceAvailability, WorkloadAnalysis,
        
        # 审批流程模型
        ApprovalRequest, ApprovalStep, ApprovalWorkflow, ApprovalComment,
        ApprovalHistory, ApprovalDelegate,
        
        # 风险管控模型
        RiskAssessment, RiskMitigationPlan, RiskAlert, RiskMonitoringRule, RiskReport,
        
        # 数据分析模型
        AnalyticsReport, Dashboard, DashboardWidget, DashboardReport,
        DataMetric, MetricValue, ReportTemplate,
    ]


def get_model_by_name(model_name: str):
    """根据模型名称获取模型类
    
    Args:
        model_name (str): 模型名称
        
    Returns:
        Model: 模型类，如果不存在则返回None
    """
    models_dict = {
        # 认证模型
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'UserRole': UserRole,
        'RolePermission': RolePermission,
        'UserSession': UserSession,
        'LoginAttempt': LoginAttempt,
        'PasswordResetToken': PasswordResetToken,
        'EmailVerificationToken': EmailVerificationToken,
        'ApiKey': ApiKey,
        
        # 组织架构模型
        'Department': Department,
        'Position': Position,
        'Personnel': Personnel,
        'PersonnelHistory': PersonnelHistory,
        'WorkLocation': WorkLocation,
        
        # 项目管理模型
        'Project': Project,
        'ProjectAssignment': ProjectAssignment,
        'ProjectMilestone': ProjectMilestone,
        'ProjectTask': ProjectTask,
        'ProjectDocument': ProjectDocument,
        
        # 调度管理模型
        'Schedule': Schedule,
        'ScheduleAssignment': ScheduleAssignment,
        'ScheduleConflict': ScheduleConflict,
        'ScheduleTemplate': ScheduleTemplate,
        'ResourceAvailability': ResourceAvailability,
        'WorkloadAnalysis': WorkloadAnalysis,
        
        # 审批流程模型
        'ApprovalRequest': ApprovalRequest,
        'ApprovalStep': ApprovalStep,
        'ApprovalWorkflow': ApprovalWorkflow,
        'ApprovalComment': ApprovalComment,
        'ApprovalHistory': ApprovalHistory,
        'ApprovalDelegate': ApprovalDelegate,
        
        # 风险管控模型
        'RiskAssessment': RiskAssessment,
        'RiskMitigationPlan': RiskMitigationPlan,
        'RiskAlert': RiskAlert,
        'RiskMonitoringRule': RiskMonitoringRule,
        'RiskReport': RiskReport,
        
        # 数据分析模型
        'AnalyticsReport': AnalyticsReport,
        'Dashboard': Dashboard,
        'DashboardWidget': DashboardWidget,
        'DashboardReport': DashboardReport,
        'DataMetric': DataMetric,
        'MetricValue': MetricValue,
        'ReportTemplate': ReportTemplate,
    }
    
    return models_dict.get(model_name)


def get_table_names():
    """获取所有表名列表
    
    Returns:
        List[str]: 所有表名列表
    """
    return [
        # 认证相关表
        'users', 'roles', 'permissions', 'user_roles', 'role_permissions',
        'user_sessions', 'login_attempts', 'password_reset_tokens', 
        'email_verification_tokens', 'api_keys',
        
        # 组织架构相关表
        'departments', 'positions', 'personnel', 'personnel_history', 'work_locations',
        
        # 项目管理相关表
        'projects', 'project_assignments', 'project_milestones', 
        'project_tasks', 'project_documents',
        
        # 调度管理相关表
        'schedules', 'schedule_assignments', 'schedule_conflicts', 
        'schedule_templates', 'resource_availability', 'workload_analysis',
        
        # 审批流程相关表
        'approval_requests', 'approval_steps', 'approval_workflows',
        'approval_comments', 'approval_history', 'approval_delegates',
        
        # 风险管控相关表
        'risk_assessments', 'risk_mitigation_plans', 'risk_alerts',
        'risk_monitoring_rules', 'risk_reports',
        
        # 数据分析相关表
        'analytics_reports', 'dashboards', 'dashboard_widgets',
        'dashboard_reports', 'data_metrics', 'metric_values', 'report_templates',
    ]