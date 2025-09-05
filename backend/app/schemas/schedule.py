"""调度管理相关的Pydantic模式

本文件定义了调度管理模块的所有数据模型，包括调度计划、调度分配、调度冲突、调度模板、资源可用性和工作负荷分析等。
"""

from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from .base import BaseSchema, TimestampMixin, BaseResponse, DataResponse, ListResponse, PaginatedResponse


class ScheduleStatus(str, Enum):
    """调度状态枚举"""
    DRAFT = "draft"  # 草稿
    PENDING = "pending"  # 待确认
    CONFIRMED = "confirmed"  # 已确认
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class SchedulePriority(str, Enum):
    """调度优先级枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


class ConflictType(str, Enum):
    """冲突类型枚举"""
    TIME_OVERLAP = "time_overlap"  # 时间重叠
    RESOURCE_CONFLICT = "resource_conflict"  # 资源冲突
    SKILL_MISMATCH = "skill_mismatch"  # 技能不匹配
    CAPACITY_EXCEEDED = "capacity_exceeded"  # 容量超限
    LOCATION_CONFLICT = "location_conflict"  # 地点冲突


class ConflictSeverity(str, Enum):
    """冲突严重程度枚举"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    CRITICAL = "critical"  # 严重


class ResourceType(str, Enum):
    """资源类型枚举"""
    HUMAN = "human"  # 人力资源
    EQUIPMENT = "equipment"  # 设备资源
    FACILITY = "facility"  # 场地资源
    MATERIAL = "material"  # 物料资源
    VEHICLE = "vehicle"  # 车辆资源


class AvailabilityStatus(str, Enum):
    """可用性状态枚举"""
    AVAILABLE = "available"  # 可用
    BUSY = "busy"  # 忙碌
    UNAVAILABLE = "unavailable"  # 不可用
    MAINTENANCE = "maintenance"  # 维护中
    RESERVED = "reserved"  # 已预留


# 调度计划相关模式
class SchedulePlanBase(BaseSchema):
    """调度计划基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="计划名称")
    description: Optional[str] = Field(None, max_length=2000, description="计划描述")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    start_time: Optional[time] = Field(None, description="开始时间")
    end_time: Optional[time] = Field(None, description="结束时间")
    status: ScheduleStatus = Field(ScheduleStatus.DRAFT, description="调度状态")
    priority: SchedulePriority = Field(SchedulePriority.MEDIUM, description="优先级")
    location: Optional[str] = Field(None, max_length=200, description="地点")
    estimated_duration: Optional[int] = Field(None, ge=0, description="预估时长（分钟）")
    actual_duration: Optional[int] = Field(None, ge=0, description="实际时长（分钟）")
    required_skills: Optional[str] = Field(None, max_length=500, description="所需技能")
    notes: Optional[str] = Field(None, max_length=1000, description="备注")
    created_by: int = Field(..., description="创建人ID")
    is_recurring: bool = Field(False, description="是否重复")
    recurrence_pattern: Optional[str] = Field(None, max_length=100, description="重复模式")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v

    @validator('end_time')
    def validate_end_time(cls, v, values):
        if v and 'start_time' in values and values['start_time']:
            # 如果是同一天，结束时间不能早于开始时间
            if 'start_date' in values and 'end_date' in values:
                if values['start_date'] == values['end_date'] and v <= values['start_time']:
                    raise ValueError('结束时间不能早于或等于开始时间')
        return v


class SchedulePlanCreate(SchedulePlanBase):
    """创建调度计划模式"""
    pass


class SchedulePlanUpdate(BaseSchema):
    """更新调度计划模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="计划名称")
    description: Optional[str] = Field(None, max_length=2000, description="计划描述")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    start_time: Optional[time] = Field(None, description="开始时间")
    end_time: Optional[time] = Field(None, description="结束时间")
    status: Optional[ScheduleStatus] = Field(None, description="调度状态")
    priority: Optional[SchedulePriority] = Field(None, description="优先级")
    location: Optional[str] = Field(None, max_length=200, description="地点")
    estimated_duration: Optional[int] = Field(None, ge=0, description="预估时长（分钟）")
    actual_duration: Optional[int] = Field(None, ge=0, description="实际时长（分钟）")
    required_skills: Optional[str] = Field(None, max_length=500, description="所需技能")
    notes: Optional[str] = Field(None, max_length=1000, description="备注")
    is_recurring: Optional[bool] = Field(None, description="是否重复")
    recurrence_pattern: Optional[str] = Field(None, max_length=100, description="重复模式")


class SchedulePlanResponse(SchedulePlanBase, TimestampMixin):
    """调度计划响应模式"""
    id: int = Field(..., description="计划ID")
    project_name: Optional[str] = Field(None, description="项目名称")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    assignment_count: int = Field(0, description="分配数量")
    conflict_count: int = Field(0, description="冲突数量")
    completion_rate: Optional[Decimal] = Field(None, description="完成率")
    duration_formatted: Optional[str] = Field(None, description="格式化的时长")

    class Config:
        from_attributes = True


# 调度分配相关模式
class ScheduleAssignmentBase(BaseSchema):
    """调度分配基础模式"""
    schedule_plan_id: int = Field(..., description="调度计划ID")
    resource_id: int = Field(..., description="资源ID")
    resource_type: ResourceType = Field(ResourceType.HUMAN, description="资源类型")
    role: Optional[str] = Field(None, max_length=100, description="角色")
    allocation_percentage: int = Field(100, ge=0, le=100, description="分配百分比")
    start_datetime: datetime = Field(..., description="开始时间")
    end_datetime: datetime = Field(..., description="结束时间")
    estimated_hours: Optional[Decimal] = Field(None, ge=0, description="预估工时")
    actual_hours: Optional[Decimal] = Field(None, ge=0, description="实际工时")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    status: ScheduleStatus = Field(ScheduleStatus.PENDING, description="分配状态")
    notes: Optional[str] = Field(None, max_length=500, description="备注")
    assigned_by: int = Field(..., description="分配人ID")

    @validator('end_datetime')
    def validate_end_datetime(cls, v, values):
        if v and 'start_datetime' in values and values['start_datetime'] and v <= values['start_datetime']:
            raise ValueError('结束时间必须晚于开始时间')
        return v


class ScheduleAssignmentCreate(ScheduleAssignmentBase):
    """创建调度分配模式"""
    pass


class ScheduleAssignmentUpdate(BaseSchema):
    """更新调度分配模式"""
    role: Optional[str] = Field(None, max_length=100, description="角色")
    allocation_percentage: Optional[int] = Field(None, ge=0, le=100, description="分配百分比")
    start_datetime: Optional[datetime] = Field(None, description="开始时间")
    end_datetime: Optional[datetime] = Field(None, description="结束时间")
    estimated_hours: Optional[Decimal] = Field(None, ge=0, description="预估工时")
    actual_hours: Optional[Decimal] = Field(None, ge=0, description="实际工时")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    status: Optional[ScheduleStatus] = Field(None, description="分配状态")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class ScheduleAssignmentResponse(ScheduleAssignmentBase, TimestampMixin):
    """调度分配响应模式"""
    id: int = Field(..., description="分配ID")
    schedule_plan_name: Optional[str] = Field(None, description="调度计划名称")
    resource_name: Optional[str] = Field(None, description="资源名称")
    assigner_name: Optional[str] = Field(None, description="分配人姓名")
    total_cost: Optional[Decimal] = Field(None, description="总成本")
    duration_hours: Optional[Decimal] = Field(None, description="时长（小时）")
    utilization_rate: Optional[Decimal] = Field(None, description="利用率")

    class Config:
        from_attributes = True


# 调度冲突相关模式
class ScheduleConflictBase(BaseSchema):
    """调度冲突基础模式"""
    schedule_plan_id: int = Field(..., description="调度计划ID")
    conflicting_schedule_id: Optional[int] = Field(None, description="冲突调度ID")
    resource_id: Optional[int] = Field(None, description="资源ID")
    conflict_type: ConflictType = Field(..., description="冲突类型")
    severity: ConflictSeverity = Field(ConflictSeverity.MEDIUM, description="严重程度")
    description: str = Field(..., max_length=1000, description="冲突描述")
    suggested_resolution: Optional[str] = Field(None, max_length=1000, description="建议解决方案")
    is_resolved: bool = Field(False, description="是否已解决")
    resolved_by: Optional[int] = Field(None, description="解决人ID")
    resolved_at: Optional[datetime] = Field(None, description="解决时间")
    resolution_notes: Optional[str] = Field(None, max_length=500, description="解决备注")
    detected_by: int = Field(..., description="检测人ID")


class ScheduleConflictCreate(ScheduleConflictBase):
    """创建调度冲突模式"""
    pass


class ScheduleConflictUpdate(BaseSchema):
    """更新调度冲突模式"""
    severity: Optional[ConflictSeverity] = Field(None, description="严重程度")
    description: Optional[str] = Field(None, max_length=1000, description="冲突描述")
    suggested_resolution: Optional[str] = Field(None, max_length=1000, description="建议解决方案")
    is_resolved: Optional[bool] = Field(None, description="是否已解决")
    resolved_by: Optional[int] = Field(None, description="解决人ID")
    resolved_at: Optional[datetime] = Field(None, description="解决时间")
    resolution_notes: Optional[str] = Field(None, max_length=500, description="解决备注")


class ScheduleConflictResponse(ScheduleConflictBase, TimestampMixin):
    """调度冲突响应模式"""
    id: int = Field(..., description="冲突ID")
    schedule_plan_name: Optional[str] = Field(None, description="调度计划名称")
    conflicting_schedule_name: Optional[str] = Field(None, description="冲突调度名称")
    resource_name: Optional[str] = Field(None, description="资源名称")
    detector_name: Optional[str] = Field(None, description="检测人姓名")
    resolver_name: Optional[str] = Field(None, description="解决人姓名")
    days_since_detected: Optional[int] = Field(None, description="检测后天数")

    class Config:
        from_attributes = True


# 调度模板相关模式
class ScheduleTemplateBase(BaseSchema):
    """调度模板基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="模板名称")
    description: Optional[str] = Field(None, max_length=1000, description="模板描述")
    category: Optional[str] = Field(None, max_length=100, description="模板分类")
    template_data: Dict[str, Any] = Field(..., description="模板数据")
    default_duration: Optional[int] = Field(None, ge=0, description="默认时长（分钟）")
    required_skills: Optional[str] = Field(None, max_length=500, description="所需技能")
    resource_requirements: Optional[Dict[str, Any]] = Field(None, description="资源需求")
    is_public: bool = Field(False, description="是否公开")
    is_active: bool = Field(True, description="是否激活")
    created_by: int = Field(..., description="创建人ID")
    usage_count: int = Field(0, description="使用次数")


class ScheduleTemplateCreate(ScheduleTemplateBase):
    """创建调度模板模式"""
    pass


class ScheduleTemplateUpdate(BaseSchema):
    """更新调度模板模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="模板名称")
    description: Optional[str] = Field(None, max_length=1000, description="模板描述")
    category: Optional[str] = Field(None, max_length=100, description="模板分类")
    template_data: Optional[Dict[str, Any]] = Field(None, description="模板数据")
    default_duration: Optional[int] = Field(None, ge=0, description="默认时长（分钟）")
    required_skills: Optional[str] = Field(None, max_length=500, description="所需技能")
    resource_requirements: Optional[Dict[str, Any]] = Field(None, description="资源需求")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ScheduleTemplateResponse(ScheduleTemplateBase, TimestampMixin):
    """调度模板响应模式"""
    id: int = Field(..., description="模板ID")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")
    rating: Optional[Decimal] = Field(None, description="评分")
    rating_count: int = Field(0, description="评分次数")

    class Config:
        from_attributes = True


# 资源可用性相关模式
class ResourceAvailabilityBase(BaseSchema):
    """资源可用性基础模式"""
    resource_id: int = Field(..., description="资源ID")
    resource_type: ResourceType = Field(ResourceType.HUMAN, description="资源类型")
    start_datetime: datetime = Field(..., description="开始时间")
    end_datetime: datetime = Field(..., description="结束时间")
    status: AvailabilityStatus = Field(AvailabilityStatus.AVAILABLE, description="可用性状态")
    capacity: Optional[Decimal] = Field(None, ge=0, description="容量")
    allocated_capacity: Optional[Decimal] = Field(None, ge=0, description="已分配容量")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    location: Optional[str] = Field(None, max_length=200, description="地点")
    skills: Optional[str] = Field(None, max_length=500, description="技能")
    notes: Optional[str] = Field(None, max_length=500, description="备注")
    created_by: int = Field(..., description="创建人ID")

    @validator('end_datetime')
    def validate_end_datetime(cls, v, values):
        if v and 'start_datetime' in values and values['start_datetime'] and v <= values['start_datetime']:
            raise ValueError('结束时间必须晚于开始时间')
        return v

    @validator('allocated_capacity')
    def validate_allocated_capacity(cls, v, values):
        if v and 'capacity' in values and values['capacity'] and v > values['capacity']:
            raise ValueError('已分配容量不能超过总容量')
        return v


class ResourceAvailabilityCreate(ResourceAvailabilityBase):
    """创建资源可用性模式"""
    pass


class ResourceAvailabilityUpdate(BaseSchema):
    """更新资源可用性模式"""
    start_datetime: Optional[datetime] = Field(None, description="开始时间")
    end_datetime: Optional[datetime] = Field(None, description="结束时间")
    status: Optional[AvailabilityStatus] = Field(None, description="可用性状态")
    capacity: Optional[Decimal] = Field(None, ge=0, description="容量")
    allocated_capacity: Optional[Decimal] = Field(None, ge=0, description="已分配容量")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="小时费率")
    location: Optional[str] = Field(None, max_length=200, description="地点")
    skills: Optional[str] = Field(None, max_length=500, description="技能")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class ResourceAvailabilityResponse(ResourceAvailabilityBase, TimestampMixin):
    """资源可用性响应模式"""
    id: int = Field(..., description="可用性ID")
    resource_name: Optional[str] = Field(None, description="资源名称")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    utilization_rate: Optional[Decimal] = Field(None, description="利用率")
    remaining_capacity: Optional[Decimal] = Field(None, description="剩余容量")
    duration_hours: Optional[Decimal] = Field(None, description="时长（小时）")

    class Config:
        from_attributes = True


# 工作负荷分析相关模式
class WorkloadAnalysisBase(BaseSchema):
    """工作负荷分析基础模式"""
    resource_id: int = Field(..., description="资源ID")
    resource_type: ResourceType = Field(ResourceType.HUMAN, description="资源类型")
    analysis_period_start: date = Field(..., description="分析期间开始")
    analysis_period_end: date = Field(..., description="分析期间结束")
    total_capacity: Decimal = Field(..., ge=0, description="总容量")
    allocated_capacity: Decimal = Field(..., ge=0, description="已分配容量")
    utilization_rate: Decimal = Field(..., ge=0, le=100, description="利用率")
    overload_hours: Optional[Decimal] = Field(None, ge=0, description="超负荷工时")
    idle_hours: Optional[Decimal] = Field(None, ge=0, description="空闲工时")
    efficiency_score: Optional[Decimal] = Field(None, ge=0, le=100, description="效率评分")
    cost_per_hour: Optional[Decimal] = Field(None, ge=0, description="每小时成本")
    total_cost: Optional[Decimal] = Field(None, ge=0, description="总成本")
    revenue_per_hour: Optional[Decimal] = Field(None, ge=0, description="每小时收入")
    total_revenue: Optional[Decimal] = Field(None, ge=0, description="总收入")
    analysis_notes: Optional[str] = Field(None, max_length=1000, description="分析备注")
    generated_by: int = Field(..., description="生成人ID")

    @validator('analysis_period_end')
    def validate_analysis_period_end(cls, v, values):
        if v and 'analysis_period_start' in values and values['analysis_period_start'] and v < values['analysis_period_start']:
            raise ValueError('分析期间结束日期不能早于开始日期')
        return v


class WorkloadAnalysisCreate(WorkloadAnalysisBase):
    """创建工作负荷分析模式"""
    pass


class WorkloadAnalysisUpdate(BaseSchema):
    """更新工作负荷分析模式"""
    analysis_period_start: Optional[date] = Field(None, description="分析期间开始")
    analysis_period_end: Optional[date] = Field(None, description="分析期间结束")
    total_capacity: Optional[Decimal] = Field(None, ge=0, description="总容量")
    allocated_capacity: Optional[Decimal] = Field(None, ge=0, description="已分配容量")
    utilization_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="利用率")
    overload_hours: Optional[Decimal] = Field(None, ge=0, description="超负荷工时")
    idle_hours: Optional[Decimal] = Field(None, ge=0, description="空闲工时")
    efficiency_score: Optional[Decimal] = Field(None, ge=0, le=100, description="效率评分")
    cost_per_hour: Optional[Decimal] = Field(None, ge=0, description="每小时成本")
    total_cost: Optional[Decimal] = Field(None, ge=0, description="总成本")
    revenue_per_hour: Optional[Decimal] = Field(None, ge=0, description="每小时收入")
    total_revenue: Optional[Decimal] = Field(None, ge=0, description="总收入")
    analysis_notes: Optional[str] = Field(None, max_length=1000, description="分析备注")


class WorkloadAnalysisResponse(WorkloadAnalysisBase, TimestampMixin):
    """工作负荷分析响应模式"""
    id: int = Field(..., description="分析ID")
    resource_name: Optional[str] = Field(None, description="资源名称")
    generator_name: Optional[str] = Field(None, description="生成人姓名")
    profit_margin: Optional[Decimal] = Field(None, description="利润率")
    roi: Optional[Decimal] = Field(None, description="投资回报率")
    performance_trend: Optional[str] = Field(None, description="绩效趋势")
    recommendations: Optional[List[str]] = Field(None, description="建议")

    class Config:
        from_attributes = True


# 响应模式
class SchedulePlanListResponse(ListResponse[SchedulePlanResponse]):
    """调度计划列表响应"""
    pass


class SchedulePlanPaginatedResponse(PaginatedResponse[SchedulePlanResponse]):
    """调度计划分页响应"""
    pass


class ScheduleAssignmentListResponse(ListResponse[ScheduleAssignmentResponse]):
    """调度分配列表响应"""
    pass


class ScheduleConflictListResponse(ListResponse[ScheduleConflictResponse]):
    """调度冲突列表响应"""
    pass


class ScheduleTemplateListResponse(ListResponse[ScheduleTemplateResponse]):
    """调度模板列表响应"""
    pass


class ResourceAvailabilityListResponse(ListResponse[ResourceAvailabilityResponse]):
    """资源可用性列表响应"""
    pass


class WorkloadAnalysisListResponse(ListResponse[WorkloadAnalysisResponse]):
    """工作负荷分析列表响应"""
    pass


# 特殊请求模式
class ConflictDetectionRequest(BaseSchema):
    """冲突检测请求"""
    schedule_plan_id: int = Field(..., description="调度计划ID")
    check_time_overlap: bool = Field(True, description="检查时间重叠")
    check_resource_conflict: bool = Field(True, description="检查资源冲突")
    check_skill_mismatch: bool = Field(True, description="检查技能不匹配")
    check_capacity: bool = Field(True, description="检查容量")
    check_location: bool = Field(True, description="检查地点冲突")


class ConflictResolutionRequest(BaseSchema):
    """冲突解决请求"""
    conflict_id: int = Field(..., description="冲突ID")
    resolution_type: str = Field(..., max_length=50, description="解决方案类型")
    resolution_data: Optional[Dict[str, Any]] = Field(None, description="解决方案数据")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class WorkloadAnalysisRequest(BaseSchema):
    """工作负荷分析请求"""
    resource_ids: List[int] = Field(..., description="资源ID列表")
    resource_type: Optional[ResourceType] = Field(None, description="资源类型")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    include_cost_analysis: bool = Field(True, description="包含成本分析")
    include_efficiency_analysis: bool = Field(True, description="包含效率分析")
    include_recommendations: bool = Field(True, description="包含建议")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v