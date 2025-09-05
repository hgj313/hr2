"""Pydantic模式定义模块

本模块包含人力资源调度系统的所有API请求和响应模式定义。
"""

# 导入基础模式
from app.schemas.base import (
    BaseResponse,
    PaginatedResponse,
    ErrorResponse,
    SuccessResponse,
    MessageResponse
)

# 导入认证相关模式
from app.schemas.auth import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserRegister,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerificationRequest,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionResponse,
    ApiKeyCreate,
    ApiKeyResponse
)

# 导入组织架构相关模式
from app.schemas.organization import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    PositionCreate,
    PositionUpdate,
    PositionResponse,
    PersonnelCreate,
    PersonnelUpdate,
    PersonnelResponse,
    PersonnelDetailResponse,
    WorkLocationCreate,
    WorkLocationUpdate,
    WorkLocationResponse
)

# 导入项目管理相关模式
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectAssignmentCreate,
    ProjectAssignmentUpdate,
    ProjectAssignmentResponse,
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse
)

# 导入调度管理相关模式
from app.schemas.schedule import (
    SchedulePlanCreate,
    SchedulePlanUpdate,
    SchedulePlanResponse,
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

# 导入审批流程相关模式
from app.schemas.approval import (
    ApprovalRequestCreate,
    ApprovalRequestUpdate,
    ApprovalRequestResponse,
    ApprovalWorkflowCreate,
    ApprovalWorkflowUpdate,
    ApprovalWorkflowResponse,
    ApprovalCommentCreate,
    ApprovalCommentResponse,
    ApprovalHistoryResponse,
    ApprovalDelegationCreate,
    ApprovalDelegationResponse
)

# 导入风险管控相关模式
from app.schemas.risk import (
    RiskAssessmentCreate,
    RiskAssessmentUpdate,
    RiskAssessmentResponse,
    RiskMitigationPlanCreate,
    RiskMitigationPlanUpdate,
    RiskMitigationPlanResponse,
    RiskAlertCreate,
    RiskAlertUpdate,
    RiskAlertResponse,
    RiskMonitoringRuleCreate,
    RiskMonitoringRuleUpdate,
    RiskMonitoringRuleResponse,
    RiskReportCreate,
    RiskReportUpdate,
    RiskReportResponse
)

# 导入数据分析相关模式
from app.schemas.analytics import (
    AnalyticsReportCreate,
    AnalyticsReportUpdate,
    AnalyticsReportResponse,
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    DashboardComponentCreate,
    DashboardComponentUpdate,
    DashboardComponentResponse,
    DataMetricCreate,
    DataMetricUpdate,
    DataMetricResponse,
    MetricValueCreate,
    MetricValueResponse,
    ReportTemplateCreate,
    ReportTemplateUpdate,
    ReportTemplateResponse,
    ReportGenerationRequest,
    DashboardExportRequest,
    MetricCalculationRequest,
    DataStatisticsResponse
)

# 导入项目管理相关模式
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
    ProjectDocumentResponse
)

# 导入调度管理相关模式
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

# 导入审批流程相关模式
from app.schemas.approval import (
    ApprovalRequestCreate,
    ApprovalRequestUpdate,
    ApprovalRequestResponse,
    ApprovalRequestDetailResponse,
    ApprovalWorkflowCreate,
    ApprovalWorkflowUpdate,
    ApprovalWorkflowResponse,
    ApprovalCommentCreate,
    ApprovalCommentResponse,
    ApprovalDelegateCreate,
    ApprovalDelegateResponse
)

# 导入风险管控相关模式
from app.schemas.risk import (
    RiskAssessmentCreate,
    RiskAssessmentUpdate,
    RiskAssessmentResponse,
    RiskMitigationPlanCreate,
    RiskMitigationPlanUpdate,
    RiskMitigationPlanResponse,
    RiskAlertResponse,
    RiskMonitoringRuleCreate,
    RiskMonitoringRuleUpdate,
    RiskMonitoringRuleResponse,
    RiskReportResponse
)

# 导入数据分析相关模式
from app.schemas.analytics import (
    AnalyticsReportCreate,
    AnalyticsReportUpdate,
    AnalyticsReportResponse,
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    DashboardDetailResponse,
    DashboardWidgetCreate,
    DashboardWidgetUpdate,
    DashboardWidgetResponse,
    DataMetricResponse,
    MetricValueResponse,
    ReportTemplateCreate,
    ReportTemplateUpdate,
    ReportTemplateResponse
)

__all__ = [
    # 基础模式
    "BaseResponse",
    "PaginatedResponse",
    "ErrorResponse",
    "SuccessResponse",
    "MessageResponse",
    
    # 认证模式
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "UserRegister",
    "TokenResponse",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "EmailVerificationRequest",
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    "PermissionResponse",
    "ApiKeyCreate",
    "ApiKeyResponse",
    
    # 组织架构模式
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "PositionCreate",
    "PositionUpdate",
    "PositionResponse",
    "PersonnelCreate",
    "PersonnelUpdate",
    "PersonnelResponse",
    "PersonnelDetailResponse",
    "WorkLocationCreate",
    "WorkLocationUpdate",
    "WorkLocationResponse",
    
    # 项目管理模式
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectDetailResponse",
    "ProjectAssignmentCreate",
    "ProjectAssignmentUpdate",
    "ProjectAssignmentResponse",
    "ProjectMilestoneCreate",
    "ProjectMilestoneUpdate",
    "ProjectMilestoneResponse",
    "ProjectTaskCreate",
    "ProjectTaskUpdate",
    "ProjectTaskResponse",
    "ProjectDocumentCreate",
    "ProjectDocumentResponse",
    
    # 调度管理模式
    "ScheduleCreate",
    "ScheduleUpdate",
    "ScheduleResponse",
    "ScheduleDetailResponse",
    "ScheduleAssignmentCreate",
    "ScheduleAssignmentUpdate",
    "ScheduleAssignmentResponse",
    "ScheduleConflictResponse",
    "ScheduleTemplateCreate",
    "ScheduleTemplateUpdate",
    "ScheduleTemplateResponse",
    "ResourceAvailabilityCreate",
    "ResourceAvailabilityUpdate",
    "ResourceAvailabilityResponse",
    "WorkloadAnalysisResponse",
    
    # 审批流程模式
    "ApprovalRequestCreate",
    "ApprovalRequestUpdate",
    "ApprovalRequestResponse",
    "ApprovalRequestDetailResponse",
    "ApprovalWorkflowCreate",
    "ApprovalWorkflowUpdate",
    "ApprovalWorkflowResponse",
    "ApprovalCommentCreate",
    "ApprovalCommentResponse",
    "ApprovalDelegateCreate",
    "ApprovalDelegateResponse",
    
    # 风险管控模式
    "RiskAssessmentCreate",
    "RiskAssessmentUpdate",
    "RiskAssessmentResponse",
    "RiskMitigationPlanCreate",
    "RiskMitigationPlanUpdate",
    "RiskMitigationPlanResponse",
    "RiskAlertResponse",
    "RiskMonitoringRuleCreate",
    "RiskMonitoringRuleUpdate",
    "RiskMonitoringRuleResponse",
    "RiskReportResponse",
    
    # 数据分析模式
    "AnalyticsReportCreate",
    "AnalyticsReportUpdate",
    "AnalyticsReportResponse",
    "DashboardCreate",
    "DashboardUpdate",
    "DashboardResponse",
    "DashboardDetailResponse",
    "DashboardWidgetCreate",
    "DashboardWidgetUpdate",
    "DashboardWidgetResponse",
    "DataMetricResponse",
    "MetricValueResponse",
    "ReportTemplateCreate",
    "ReportTemplateUpdate",
    "ReportTemplateResponse",
]