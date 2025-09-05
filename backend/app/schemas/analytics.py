"""数据分析相关的Pydantic模式

本文件定义了数据分析模块的所有数据模型，包括分析报表、仪表板、仪表板组件、数据指标、指标值和报表模板等。
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from .base import BaseSchema, TimestampMixin, BaseResponse, DataResponse, ListResponse, PaginatedResponse


class ReportStatus(str, Enum):
    """报表状态枚举"""
    DRAFT = "draft"  # 草稿
    GENERATING = "generating"  # 生成中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    SCHEDULED = "scheduled"  # 已调度
    CANCELLED = "cancelled"  # 已取消
    ARCHIVED = "archived"  # 已归档


class ReportType(str, Enum):
    """报表类型枚举"""
    OPERATIONAL = "operational"  # 运营报表
    FINANCIAL = "financial"  # 财务报表
    PERFORMANCE = "performance"  # 绩效报表
    COMPLIANCE = "compliance"  # 合规报表
    EXECUTIVE = "executive"  # 高管报表
    CUSTOM = "custom"  # 自定义报表
    DASHBOARD = "dashboard"  # 仪表板报表
    TREND_ANALYSIS = "trend_analysis"  # 趋势分析
    COMPARATIVE = "comparative"  # 对比分析
    PREDICTIVE = "predictive"  # 预测分析


class ReportFormat(str, Enum):
    """报表格式枚举"""
    PDF = "pdf"  # PDF格式
    EXCEL = "excel"  # Excel格式
    CSV = "csv"  # CSV格式
    JSON = "json"  # JSON格式
    HTML = "html"  # HTML格式
    POWERPOINT = "powerpoint"  # PowerPoint格式


class DashboardType(str, Enum):
    """仪表板类型枚举"""
    EXECUTIVE = "executive"  # 高管仪表板
    OPERATIONAL = "operational"  # 运营仪表板
    ANALYTICAL = "analytical"  # 分析仪表板
    REAL_TIME = "real_time"  # 实时仪表板
    DEPARTMENTAL = "departmental"  # 部门仪表板
    PROJECT = "project"  # 项目仪表板
    PERSONAL = "personal"  # 个人仪表板
    PUBLIC = "public"  # 公共仪表板


class ComponentType(str, Enum):
    """组件类型枚举"""
    CHART = "chart"  # 图表
    TABLE = "table"  # 表格
    METRIC = "metric"  # 指标
    TEXT = "text"  # 文本
    IMAGE = "image"  # 图片
    MAP = "map"  # 地图
    GAUGE = "gauge"  # 仪表盘
    PROGRESS = "progress"  # 进度条
    LIST = "list"  # 列表
    CALENDAR = "calendar"  # 日历
    FILTER = "filter"  # 过滤器
    IFRAME = "iframe"  # 内嵌框架


class ChartType(str, Enum):
    """图表类型枚举"""
    LINE = "line"  # 折线图
    BAR = "bar"  # 柱状图
    PIE = "pie"  # 饼图
    AREA = "area"  # 面积图
    SCATTER = "scatter"  # 散点图
    BUBBLE = "bubble"  # 气泡图
    HEATMAP = "heatmap"  # 热力图
    TREEMAP = "treemap"  # 树状图
    FUNNEL = "funnel"  # 漏斗图
    RADAR = "radar"  # 雷达图
    CANDLESTICK = "candlestick"  # 蜡烛图
    WATERFALL = "waterfall"  # 瀑布图


class MetricType(str, Enum):
    """指标类型枚举"""
    COUNT = "count"  # 计数
    SUM = "sum"  # 求和
    AVERAGE = "average"  # 平均值
    PERCENTAGE = "percentage"  # 百分比
    RATIO = "ratio"  # 比率
    GROWTH_RATE = "growth_rate"  # 增长率
    VARIANCE = "variance"  # 方差
    STANDARD_DEVIATION = "standard_deviation"  # 标准差
    MEDIAN = "median"  # 中位数
    MODE = "mode"  # 众数
    MIN = "min"  # 最小值
    MAX = "max"  # 最大值


class AggregationPeriod(str, Enum):
    """聚合周期枚举"""
    HOURLY = "hourly"  # 小时
    DAILY = "daily"  # 日
    WEEKLY = "weekly"  # 周
    MONTHLY = "monthly"  # 月
    QUARTERLY = "quarterly"  # 季度
    YEARLY = "yearly"  # 年
    REAL_TIME = "real_time"  # 实时


class DataSourceType(str, Enum):
    """数据源类型枚举"""
    DATABASE = "database"  # 数据库
    API = "api"  # API接口
    FILE = "file"  # 文件
    STREAM = "stream"  # 数据流
    CACHE = "cache"  # 缓存
    EXTERNAL = "external"  # 外部系统


class TemplateCategory(str, Enum):
    """模板类别枚举"""
    STANDARD = "standard"  # 标准模板
    CUSTOM = "custom"  # 自定义模板
    INDUSTRY = "industry"  # 行业模板
    DEPARTMENT = "department"  # 部门模板
    REGULATORY = "regulatory"  # 监管模板
    BEST_PRACTICE = "best_practice"  # 最佳实践模板


# 分析报表相关模式
class AnalyticsReportBase(BaseSchema):
    """分析报表基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="报表标题")
    description: Optional[str] = Field(None, max_length=1000, description="报表描述")
    report_type: ReportType = Field(..., description="报表类型")
    status: ReportStatus = Field(ReportStatus.DRAFT, description="报表状态")
    format: ReportFormat = Field(ReportFormat.PDF, description="报表格式")
    template_id: Optional[int] = Field(None, description="模板ID")
    data_sources: List[Dict[str, Any]] = Field(..., description="数据源配置")
    parameters: Optional[Dict[str, Any]] = Field(None, description="报表参数")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")
    date_range_start: Optional[date] = Field(None, description="日期范围开始")
    date_range_end: Optional[date] = Field(None, description="日期范围结束")
    schedule_config: Optional[Dict[str, Any]] = Field(None, description="调度配置")
    recipients: Optional[List[str]] = Field(None, description="收件人列表")
    auto_send: bool = Field(False, description="是否自动发送")
    retention_days: Optional[int] = Field(None, ge=0, description="保留天数")
    file_path: Optional[str] = Field(None, max_length=500, description="文件路径")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小")
    generation_time: Optional[int] = Field(None, ge=0, description="生成时间（秒）")
    error_message: Optional[str] = Field(None, max_length=1000, description="错误信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    created_by: int = Field(..., description="创建人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: bool = Field(False, description="是否公开")
    is_active: bool = Field(True, description="是否激活")

    @validator('date_range_end')
    def validate_date_range_end(cls, v, values):
        if v and 'date_range_start' in values and values['date_range_start'] and v < values['date_range_start']:
            raise ValueError('结束日期不能早于开始日期')
        return v


class AnalyticsReportCreate(AnalyticsReportBase):
    """创建分析报表模式"""
    pass


class AnalyticsReportUpdate(BaseSchema):
    """更新分析报表模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="报表标题")
    description: Optional[str] = Field(None, max_length=1000, description="报表描述")
    report_type: Optional[ReportType] = Field(None, description="报表类型")
    status: Optional[ReportStatus] = Field(None, description="报表状态")
    format: Optional[ReportFormat] = Field(None, description="报表格式")
    template_id: Optional[int] = Field(None, description="模板ID")
    data_sources: Optional[List[Dict[str, Any]]] = Field(None, description="数据源配置")
    parameters: Optional[Dict[str, Any]] = Field(None, description="报表参数")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")
    date_range_start: Optional[date] = Field(None, description="日期范围开始")
    date_range_end: Optional[date] = Field(None, description="日期范围结束")
    schedule_config: Optional[Dict[str, Any]] = Field(None, description="调度配置")
    recipients: Optional[List[str]] = Field(None, description="收件人列表")
    auto_send: Optional[bool] = Field(None, description="是否自动发送")
    retention_days: Optional[int] = Field(None, ge=0, description="保留天数")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_active: Optional[bool] = Field(None, description="是否激活")


class AnalyticsReportResponse(AnalyticsReportBase, TimestampMixin):
    """分析报表响应模式"""
    id: int = Field(..., description="报表ID")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    template_name: Optional[str] = Field(None, description="模板名称")
    last_generated_at: Optional[datetime] = Field(None, description="最后生成时间")
    next_generation_at: Optional[datetime] = Field(None, description="下次生成时间")
    generation_count: int = Field(0, description="生成次数")
    download_count: int = Field(0, description="下载次数")
    view_count: int = Field(0, description="查看次数")
    share_count: int = Field(0, description="分享次数")
    average_generation_time: Optional[Decimal] = Field(None, description="平均生成时间")
    success_rate: Optional[Decimal] = Field(None, description="成功率")
    file_exists: bool = Field(True, description="文件是否存在")
    is_scheduled: bool = Field(False, description="是否已调度")
    last_accessed: Optional[datetime] = Field(None, description="最后访问时间")

    class Config:
        from_attributes = True


# 仪表板相关模式
class DashboardBase(BaseSchema):
    """仪表板基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="仪表板标题")
    description: Optional[str] = Field(None, max_length=1000, description="仪表板描述")
    dashboard_type: DashboardType = Field(..., description="仪表板类型")
    layout_config: Dict[str, Any] = Field(..., description="布局配置")
    theme_config: Optional[Dict[str, Any]] = Field(None, description="主题配置")
    refresh_interval: Optional[int] = Field(None, ge=0, description="刷新间隔（秒）")
    auto_refresh: bool = Field(False, description="是否自动刷新")
    filters: Optional[Dict[str, Any]] = Field(None, description="全局过滤器")
    permissions: Optional[Dict[str, Any]] = Field(None, description="权限配置")
    sharing_settings: Optional[Dict[str, Any]] = Field(None, description="分享设置")
    export_settings: Optional[Dict[str, Any]] = Field(None, description="导出设置")
    mobile_optimized: bool = Field(False, description="是否移动端优化")
    full_screen_mode: bool = Field(False, description="是否全屏模式")
    interactive: bool = Field(True, description="是否交互式")
    real_time: bool = Field(False, description="是否实时")
    cache_duration: Optional[int] = Field(None, ge=0, description="缓存时长（秒）")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    created_by: int = Field(..., description="创建人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: bool = Field(False, description="是否公开")
    is_active: bool = Field(True, description="是否激活")
    is_favorite: bool = Field(False, description="是否收藏")


class DashboardCreate(DashboardBase):
    """创建仪表板模式"""
    pass


class DashboardUpdate(BaseSchema):
    """更新仪表板模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="仪表板标题")
    description: Optional[str] = Field(None, max_length=1000, description="仪表板描述")
    dashboard_type: Optional[DashboardType] = Field(None, description="仪表板类型")
    layout_config: Optional[Dict[str, Any]] = Field(None, description="布局配置")
    theme_config: Optional[Dict[str, Any]] = Field(None, description="主题配置")
    refresh_interval: Optional[int] = Field(None, ge=0, description="刷新间隔（秒）")
    auto_refresh: Optional[bool] = Field(None, description="是否自动刷新")
    filters: Optional[Dict[str, Any]] = Field(None, description="全局过滤器")
    permissions: Optional[Dict[str, Any]] = Field(None, description="权限配置")
    sharing_settings: Optional[Dict[str, Any]] = Field(None, description="分享设置")
    export_settings: Optional[Dict[str, Any]] = Field(None, description="导出设置")
    mobile_optimized: Optional[bool] = Field(None, description="是否移动端优化")
    full_screen_mode: Optional[bool] = Field(None, description="是否全屏模式")
    interactive: Optional[bool] = Field(None, description="是否交互式")
    real_time: Optional[bool] = Field(None, description="是否实时")
    cache_duration: Optional[int] = Field(None, ge=0, description="缓存时长（秒）")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_favorite: Optional[bool] = Field(None, description="是否收藏")


class DashboardResponse(DashboardBase, TimestampMixin):
    """仪表板响应模式"""
    id: int = Field(..., description="仪表板ID")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    component_count: int = Field(0, description="组件数量")
    view_count: int = Field(0, description="查看次数")
    share_count: int = Field(0, description="分享次数")
    favorite_count: int = Field(0, description="收藏次数")
    last_viewed_at: Optional[datetime] = Field(None, description="最后查看时间")
    last_modified_at: Optional[datetime] = Field(None, description="最后修改时间")
    performance_score: Optional[Decimal] = Field(None, description="性能评分")
    load_time: Optional[Decimal] = Field(None, description="加载时间（秒）")
    data_freshness: Optional[datetime] = Field(None, description="数据新鲜度")
    health_status: Optional[str] = Field(None, description="健康状态")

    class Config:
        from_attributes = True


# 仪表板组件相关模式
class DashboardComponentBase(BaseSchema):
    """仪表板组件基础模式"""
    dashboard_id: int = Field(..., description="仪表板ID")
    title: str = Field(..., min_length=1, max_length=200, description="组件标题")
    description: Optional[str] = Field(None, max_length=500, description="组件描述")
    component_type: ComponentType = Field(..., description="组件类型")
    chart_type: Optional[ChartType] = Field(None, description="图表类型")
    position_x: int = Field(..., ge=0, description="X坐标")
    position_y: int = Field(..., ge=0, description="Y坐标")
    width: int = Field(..., ge=1, description="宽度")
    height: int = Field(..., ge=1, description="高度")
    z_index: int = Field(0, description="层级")
    data_source: Dict[str, Any] = Field(..., description="数据源配置")
    query_config: Optional[Dict[str, Any]] = Field(None, description="查询配置")
    visualization_config: Dict[str, Any] = Field(..., description="可视化配置")
    style_config: Optional[Dict[str, Any]] = Field(None, description="样式配置")
    interaction_config: Optional[Dict[str, Any]] = Field(None, description="交互配置")
    filters: Optional[Dict[str, Any]] = Field(None, description="组件过滤器")
    refresh_interval: Optional[int] = Field(None, ge=0, description="刷新间隔（秒）")
    auto_refresh: bool = Field(False, description="是否自动刷新")
    cache_duration: Optional[int] = Field(None, ge=0, description="缓存时长（秒）")
    drill_down_config: Optional[Dict[str, Any]] = Field(None, description="下钻配置")
    alert_config: Optional[Dict[str, Any]] = Field(None, description="预警配置")
    export_config: Optional[Dict[str, Any]] = Field(None, description="导出配置")
    responsive: bool = Field(True, description="是否响应式")
    visible: bool = Field(True, description="是否可见")
    interactive: bool = Field(True, description="是否交互式")
    order_index: int = Field(0, description="排序索引")
    is_active: bool = Field(True, description="是否激活")


class DashboardComponentCreate(DashboardComponentBase):
    """创建仪表板组件模式"""
    pass


class DashboardComponentUpdate(BaseSchema):
    """更新仪表板组件模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="组件标题")
    description: Optional[str] = Field(None, max_length=500, description="组件描述")
    component_type: Optional[ComponentType] = Field(None, description="组件类型")
    chart_type: Optional[ChartType] = Field(None, description="图表类型")
    position_x: Optional[int] = Field(None, ge=0, description="X坐标")
    position_y: Optional[int] = Field(None, ge=0, description="Y坐标")
    width: Optional[int] = Field(None, ge=1, description="宽度")
    height: Optional[int] = Field(None, ge=1, description="高度")
    z_index: Optional[int] = Field(None, description="层级")
    data_source: Optional[Dict[str, Any]] = Field(None, description="数据源配置")
    query_config: Optional[Dict[str, Any]] = Field(None, description="查询配置")
    visualization_config: Optional[Dict[str, Any]] = Field(None, description="可视化配置")
    style_config: Optional[Dict[str, Any]] = Field(None, description="样式配置")
    interaction_config: Optional[Dict[str, Any]] = Field(None, description="交互配置")
    filters: Optional[Dict[str, Any]] = Field(None, description="组件过滤器")
    refresh_interval: Optional[int] = Field(None, ge=0, description="刷新间隔（秒）")
    auto_refresh: Optional[bool] = Field(None, description="是否自动刷新")
    cache_duration: Optional[int] = Field(None, ge=0, description="缓存时长（秒）")
    drill_down_config: Optional[Dict[str, Any]] = Field(None, description="下钻配置")
    alert_config: Optional[Dict[str, Any]] = Field(None, description="预警配置")
    export_config: Optional[Dict[str, Any]] = Field(None, description="导出配置")
    responsive: Optional[bool] = Field(None, description="是否响应式")
    visible: Optional[bool] = Field(None, description="是否可见")
    interactive: Optional[bool] = Field(None, description="是否交互式")
    order_index: Optional[int] = Field(None, description="排序索引")
    is_active: Optional[bool] = Field(None, description="是否激活")


class DashboardComponentResponse(DashboardComponentBase, TimestampMixin):
    """仪表板组件响应模式"""
    id: int = Field(..., description="组件ID")
    dashboard_title: Optional[str] = Field(None, description="仪表板标题")
    data_last_updated: Optional[datetime] = Field(None, description="数据最后更新时间")
    render_time: Optional[Decimal] = Field(None, description="渲染时间（毫秒）")
    error_count: int = Field(0, description="错误次数")
    last_error: Optional[str] = Field(None, description="最后错误")
    view_count: int = Field(0, description="查看次数")
    interaction_count: int = Field(0, description="交互次数")
    performance_score: Optional[Decimal] = Field(None, description="性能评分")
    health_status: Optional[str] = Field(None, description="健康状态")

    class Config:
        from_attributes = True


# 数据指标相关模式
class DataMetricBase(BaseSchema):
    """数据指标基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="指标名称")
    display_name: str = Field(..., min_length=1, max_length=200, description="显示名称")
    description: Optional[str] = Field(None, max_length=1000, description="指标描述")
    metric_type: MetricType = Field(..., description="指标类型")
    category: str = Field(..., max_length=100, description="指标类别")
    unit: Optional[str] = Field(None, max_length=50, description="单位")
    data_source: Dict[str, Any] = Field(..., description="数据源配置")
    calculation_formula: Optional[str] = Field(None, max_length=1000, description="计算公式")
    aggregation_period: AggregationPeriod = Field(AggregationPeriod.DAILY, description="聚合周期")
    target_value: Optional[Decimal] = Field(None, description="目标值")
    threshold_config: Optional[Dict[str, Any]] = Field(None, description="阈值配置")
    format_config: Optional[Dict[str, Any]] = Field(None, description="格式配置")
    business_context: Optional[str] = Field(None, max_length=500, description="业务背景")
    owner_id: int = Field(..., description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    data_quality_rules: Optional[List[Dict[str, Any]]] = Field(None, description="数据质量规则")
    refresh_schedule: Optional[Dict[str, Any]] = Field(None, description="刷新计划")
    retention_days: Optional[int] = Field(None, ge=0, description="保留天数")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_kpi: bool = Field(False, description="是否KPI")
    is_public: bool = Field(False, description="是否公开")
    is_active: bool = Field(True, description="是否激活")


class DataMetricCreate(DataMetricBase):
    """创建数据指标模式"""
    pass


class DataMetricUpdate(BaseSchema):
    """更新数据指标模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="指标名称")
    display_name: Optional[str] = Field(None, min_length=1, max_length=200, description="显示名称")
    description: Optional[str] = Field(None, max_length=1000, description="指标描述")
    metric_type: Optional[MetricType] = Field(None, description="指标类型")
    category: Optional[str] = Field(None, max_length=100, description="指标类别")
    unit: Optional[str] = Field(None, max_length=50, description="单位")
    data_source: Optional[Dict[str, Any]] = Field(None, description="数据源配置")
    calculation_formula: Optional[str] = Field(None, max_length=1000, description="计算公式")
    aggregation_period: Optional[AggregationPeriod] = Field(None, description="聚合周期")
    target_value: Optional[Decimal] = Field(None, description="目标值")
    threshold_config: Optional[Dict[str, Any]] = Field(None, description="阈值配置")
    format_config: Optional[Dict[str, Any]] = Field(None, description="格式配置")
    business_context: Optional[str] = Field(None, max_length=500, description="业务背景")
    owner_id: Optional[int] = Field(None, description="负责人ID")
    stakeholders: Optional[List[int]] = Field(None, description="利益相关者ID列表")
    data_quality_rules: Optional[List[Dict[str, Any]]] = Field(None, description="数据质量规则")
    refresh_schedule: Optional[Dict[str, Any]] = Field(None, description="刷新计划")
    retention_days: Optional[int] = Field(None, ge=0, description="保留天数")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_kpi: Optional[bool] = Field(None, description="是否KPI")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_active: Optional[bool] = Field(None, description="是否激活")


class DataMetricResponse(DataMetricBase, TimestampMixin):
    """数据指标响应模式"""
    id: int = Field(..., description="指标ID")
    owner_name: Optional[str] = Field(None, description="负责人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    stakeholder_names: Optional[List[str]] = Field(None, description="利益相关者姓名")
    current_value: Optional[Union[Decimal, int, float, str]] = Field(None, description="当前值")
    previous_value: Optional[Union[Decimal, int, float, str]] = Field(None, description="上期值")
    change_percentage: Optional[Decimal] = Field(None, description="变化百分比")
    trend_direction: Optional[str] = Field(None, description="趋势方向")
    last_calculated_at: Optional[datetime] = Field(None, description="最后计算时间")
    next_calculation_at: Optional[datetime] = Field(None, description="下次计算时间")
    calculation_count: int = Field(0, description="计算次数")
    error_count: int = Field(0, description="错误次数")
    data_quality_score: Optional[Decimal] = Field(None, description="数据质量评分")
    usage_count: int = Field(0, description="使用次数")
    dashboard_count: int = Field(0, description="仪表板使用数")
    alert_count: int = Field(0, description="预警数量")
    health_status: Optional[str] = Field(None, description="健康状态")

    class Config:
        from_attributes = True


# 指标值相关模式
class MetricValueBase(BaseSchema):
    """指标值基础模式"""
    metric_id: int = Field(..., description="指标ID")
    value: Union[Decimal, int, float, str] = Field(..., description="指标值")
    timestamp: datetime = Field(..., description="时间戳")
    period_start: Optional[datetime] = Field(None, description="周期开始时间")
    period_end: Optional[datetime] = Field(None, description="周期结束时间")
    dimensions: Optional[Dict[str, Any]] = Field(None, description="维度信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    data_source: Optional[str] = Field(None, max_length=100, description="数据源")
    calculation_method: Optional[str] = Field(None, max_length=100, description="计算方法")
    confidence_level: Optional[Decimal] = Field(None, ge=0, le=100, description="置信度")
    quality_score: Optional[Decimal] = Field(None, ge=0, le=100, description="质量评分")
    is_estimated: bool = Field(False, description="是否估算值")
    is_anomaly: bool = Field(False, description="是否异常值")
    anomaly_score: Optional[Decimal] = Field(None, ge=0, le=100, description="异常评分")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class MetricValueCreate(MetricValueBase):
    """创建指标值模式"""
    pass


class MetricValueResponse(MetricValueBase, TimestampMixin):
    """指标值响应模式"""
    id: int = Field(..., description="指标值ID")
    metric_name: Optional[str] = Field(None, description="指标名称")
    metric_display_name: Optional[str] = Field(None, description="指标显示名称")
    metric_unit: Optional[str] = Field(None, description="指标单位")
    formatted_value: Optional[str] = Field(None, description="格式化值")
    change_from_previous: Optional[Decimal] = Field(None, description="与上期变化")
    change_percentage: Optional[Decimal] = Field(None, description="变化百分比")
    target_achievement: Optional[Decimal] = Field(None, description="目标达成率")
    percentile_rank: Optional[Decimal] = Field(None, description="百分位排名")
    z_score: Optional[Decimal] = Field(None, description="Z分数")
    trend_indicator: Optional[str] = Field(None, description="趋势指示器")

    class Config:
        from_attributes = True


# 报表模板相关模式
class ReportTemplateBase(BaseSchema):
    """报表模板基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="模板名称")
    description: Optional[str] = Field(None, max_length=1000, description="模板描述")
    category: TemplateCategory = Field(..., description="模板类别")
    report_type: ReportType = Field(..., description="报表类型")
    template_config: Dict[str, Any] = Field(..., description="模板配置")
    layout_config: Dict[str, Any] = Field(..., description="布局配置")
    style_config: Optional[Dict[str, Any]] = Field(None, description="样式配置")
    data_source_template: Optional[Dict[str, Any]] = Field(None, description="数据源模板")
    parameter_definitions: Optional[List[Dict[str, Any]]] = Field(None, description="参数定义")
    filter_definitions: Optional[List[Dict[str, Any]]] = Field(None, description="过滤器定义")
    chart_templates: Optional[List[Dict[str, Any]]] = Field(None, description="图表模板")
    table_templates: Optional[List[Dict[str, Any]]] = Field(None, description="表格模板")
    export_formats: Optional[List[ReportFormat]] = Field(None, description="支持的导出格式")
    preview_image: Optional[str] = Field(None, max_length=500, description="预览图片")
    usage_instructions: Optional[str] = Field(None, max_length=2000, description="使用说明")
    version: str = Field("1.0", max_length=20, description="版本号")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    created_by: int = Field(..., description="创建人ID")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: bool = Field(False, description="是否公开")
    is_system: bool = Field(False, description="是否系统模板")
    is_active: bool = Field(True, description="是否激活")


class ReportTemplateCreate(ReportTemplateBase):
    """创建报表模板模式"""
    pass


class ReportTemplateUpdate(BaseSchema):
    """更新报表模板模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="模板名称")
    description: Optional[str] = Field(None, max_length=1000, description="模板描述")
    category: Optional[TemplateCategory] = Field(None, description="模板类别")
    report_type: Optional[ReportType] = Field(None, description="报表类型")
    template_config: Optional[Dict[str, Any]] = Field(None, description="模板配置")
    layout_config: Optional[Dict[str, Any]] = Field(None, description="布局配置")
    style_config: Optional[Dict[str, Any]] = Field(None, description="样式配置")
    data_source_template: Optional[Dict[str, Any]] = Field(None, description="数据源模板")
    parameter_definitions: Optional[List[Dict[str, Any]]] = Field(None, description="参数定义")
    filter_definitions: Optional[List[Dict[str, Any]]] = Field(None, description="过滤器定义")
    chart_templates: Optional[List[Dict[str, Any]]] = Field(None, description="图表模板")
    table_templates: Optional[List[Dict[str, Any]]] = Field(None, description="表格模板")
    export_formats: Optional[List[ReportFormat]] = Field(None, description="支持的导出格式")
    preview_image: Optional[str] = Field(None, max_length=500, description="预览图片")
    usage_instructions: Optional[str] = Field(None, max_length=2000, description="使用说明")
    version: Optional[str] = Field(None, max_length=20, description="版本号")
    tags: Optional[str] = Field(None, max_length=500, description="标签")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ReportTemplateResponse(ReportTemplateBase, TimestampMixin):
    """报表模板响应模式"""
    id: int = Field(..., description="模板ID")
    creator_name: Optional[str] = Field(None, description="创建人姓名")
    department_name: Optional[str] = Field(None, description="所属部门名称")
    usage_count: int = Field(0, description="使用次数")
    rating: Optional[Decimal] = Field(None, description="评分")
    rating_count: int = Field(0, description="评分次数")
    download_count: int = Field(0, description="下载次数")
    clone_count: int = Field(0, description="克隆次数")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")
    complexity_score: Optional[Decimal] = Field(None, description="复杂度评分")
    performance_score: Optional[Decimal] = Field(None, description="性能评分")
    compatibility_score: Optional[Decimal] = Field(None, description="兼容性评分")
    maintenance_score: Optional[Decimal] = Field(None, description="维护性评分")

    class Config:
        from_attributes = True


# 响应模式
class AnalyticsReportListResponse(ListResponse[AnalyticsReportResponse]):
    """分析报表列表响应"""
    pass


class AnalyticsReportPaginatedResponse(PaginatedResponse[AnalyticsReportResponse]):
    """分析报表分页响应"""
    pass


class DashboardListResponse(ListResponse[DashboardResponse]):
    """仪表板列表响应"""
    pass


class DashboardComponentListResponse(ListResponse[DashboardComponentResponse]):
    """仪表板组件列表响应"""
    pass


class DataMetricListResponse(ListResponse[DataMetricResponse]):
    """数据指标列表响应"""
    pass


class MetricValueListResponse(ListResponse[MetricValueResponse]):
    """指标值列表响应"""
    pass


class ReportTemplateListResponse(ListResponse[ReportTemplateResponse]):
    """报表模板列表响应"""
    pass


# 特殊请求模式
class ReportGenerationRequest(BaseSchema):
    """报表生成请求"""
    template_id: Optional[int] = Field(None, description="模板ID")
    parameters: Optional[Dict[str, Any]] = Field(None, description="参数")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")
    format: ReportFormat = Field(ReportFormat.PDF, description="输出格式")
    async_generation: bool = Field(False, description="是否异步生成")
    send_email: bool = Field(False, description="是否发送邮件")
    recipients: Optional[List[str]] = Field(None, description="收件人")
    custom_title: Optional[str] = Field(None, max_length=200, description="自定义标题")
    include_raw_data: bool = Field(False, description="是否包含原始数据")


class DashboardExportRequest(BaseSchema):
    """仪表板导出请求"""
    format: ReportFormat = Field(ReportFormat.PDF, description="导出格式")
    include_filters: bool = Field(True, description="是否包含过滤器")
    include_data: bool = Field(False, description="是否包含数据")
    page_size: Optional[str] = Field(None, description="页面大小")
    orientation: Optional[str] = Field(None, description="页面方向")
    quality: Optional[str] = Field(None, description="导出质量")


class MetricCalculationRequest(BaseSchema):
    """指标计算请求"""
    metric_ids: List[int] = Field(..., min_items=1, description="指标ID列表")
    start_date: Optional[datetime] = Field(None, description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    force_recalculation: bool = Field(False, description="是否强制重新计算")
    include_historical: bool = Field(False, description="是否包含历史数据")
    dimensions: Optional[Dict[str, Any]] = Field(None, description="维度过滤")


class DataStatisticsResponse(BaseResponse):
    """数据统计响应"""
    total_reports: int = Field(0, description="总报表数")
    active_dashboards: int = Field(0, description="活跃仪表板数")
    total_metrics: int = Field(0, description="总指标数")
    kpi_metrics: int = Field(0, description="KPI指标数")
    dashboard_views_today: int = Field(0, description="今日仪表板查看数")
    report_generations_today: int = Field(0, description="今日报表生成数")
    average_dashboard_load_time: Optional[Decimal] = Field(None, description="平均仪表板加载时间")
    data_freshness_score: Optional[Decimal] = Field(None, description="数据新鲜度评分")
    system_performance_score: Optional[Decimal] = Field(None, description="系统性能评分")
    user_engagement_score: Optional[Decimal] = Field(None, description="用户参与度评分")
    top_dashboards: Optional[List[Dict[str, Any]]] = Field(None, description="热门仪表板")
    top_reports: Optional[List[Dict[str, Any]]] = Field(None, description="热门报表")
    usage_trends: Optional[List[Dict[str, Any]]] = Field(None, description="使用趋势")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="性能指标")