from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import enum

from app.core.database import Base


class ReportType(enum.Enum):
    """报表类型枚举"""
    PERSONNEL_UTILIZATION = "personnel_utilization"  # 人员利用率
    PROJECT_PROGRESS = "project_progress"  # 项目进度
    RESOURCE_ALLOCATION = "resource_allocation"  # 资源分配
    WORKLOAD_ANALYSIS = "workload_analysis"  # 工作负荷分析
    PERFORMANCE_METRICS = "performance_metrics"  # 绩效指标
    COST_ANALYSIS = "cost_analysis"  # 成本分析
    SCHEDULE_EFFICIENCY = "schedule_efficiency"  # 调度效率
    RISK_DASHBOARD = "risk_dashboard"  # 风险仪表板
    COMPLIANCE_REPORT = "compliance_report"  # 合规报告
    CUSTOM = "custom"  # 自定义报表


class ReportStatus(enum.Enum):
    """报表状态枚举"""
    DRAFT = "draft"  # 草稿
    GENERATING = "generating"  # 生成中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 生成失败
    SCHEDULED = "scheduled"  # 已调度
    CANCELLED = "cancelled"  # 已取消


class DataSource(enum.Enum):
    """数据源枚举"""
    DATABASE = "database"  # 数据库
    API = "api"  # API接口
    FILE = "file"  # 文件
    EXTERNAL = "external"  # 外部系统
    MANUAL = "manual"  # 手动输入


class ChartType(enum.Enum):
    """图表类型枚举"""
    LINE = "line"  # 折线图
    BAR = "bar"  # 柱状图
    PIE = "pie"  # 饼图
    AREA = "area"  # 面积图
    SCATTER = "scatter"  # 散点图
    HEATMAP = "heatmap"  # 热力图
    GAUGE = "gauge"  # 仪表盘
    TABLE = "table"  # 表格
    CARD = "card"  # 卡片


class AnalyticsReport(Base):
    """分析报表表模型"""
    __tablename__ = "analytics_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report_number = Column(String(50), unique=True, nullable=False, index=True)  # 报表编号
    
    # 报表基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    report_type = Column(String(50), nullable=False, index=True)
    category = Column(String(50), index=True)  # 报表分类
    
    # 报表配置
    report_config = Column(JSONB, nullable=False)  # 报表配置
    data_sources = Column(JSONB)  # 数据源配置
    filters = Column(JSONB)  # 过滤条件
    parameters = Column(JSONB)  # 参数配置
    
    # 时间范围
    date_range_type = Column(String(20), default="custom")  # custom, last_7_days, last_30_days, last_quarter, last_year
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # 报表数据
    report_data = Column(JSONB)  # 报表数据
    summary_metrics = Column(JSONB)  # 汇总指标
    chart_data = Column(JSONB)  # 图表数据
    
    # 生成状态
    status = Column(String(20), nullable=False, default="draft", index=True)
    generation_progress = Column(Float, default=0.0)  # 生成进度
    error_message = Column(Text)  # 错误信息
    
    # 创建和生成信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # 时间信息
    generation_started_at = Column(DateTime(timezone=True))
    generation_completed_at = Column(DateTime(timezone=True))
    last_refreshed_at = Column(DateTime(timezone=True))
    
    # 调度信息
    is_scheduled = Column(Boolean, default=False)
    schedule_config = Column(JSONB)  # 调度配置
    next_generation_at = Column(DateTime(timezone=True))
    
    # 共享和权限
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSONB)  # 共享用户/角色列表
    access_permissions = Column(JSONB)  # 访问权限
    
    # 文件信息
    export_formats = Column(JSONB)  # 支持的导出格式
    file_paths = Column(JSONB)  # 导出文件路径
    
    # 使用统计
    view_count = Column(Integer, default=0)
    export_count = Column(Integer, default=0)
    last_viewed_at = Column(DateTime(timezone=True))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User", foreign_keys=[created_by])
    generator = relationship("User", foreign_keys=[generated_by])
    dashboards = relationship("Dashboard", secondary="dashboard_reports", back_populates="reports")
    
    def __repr__(self):
        return f"<AnalyticsReport(id={self.id}, title={self.title}, type={self.report_type})>"
    
    @property
    def is_generating(self) -> bool:
        """检查是否正在生成"""
        return self.status == "generating"
    
    @property
    def is_completed(self) -> bool:
        """检查是否已完成"""
        return self.status == "completed"
    
    @property
    def is_failed(self) -> bool:
        """检查是否生成失败"""
        return self.status == "failed"
    
    @property
    def generation_duration_minutes(self) -> Optional[float]:
        """计算生成耗时（分钟）"""
        if self.generation_started_at and self.generation_completed_at:
            delta = self.generation_completed_at - self.generation_started_at
            return delta.total_seconds() / 60
        return None
    
    @property
    def is_stale(self, hours: int = 24) -> bool:
        """检查数据是否过期"""
        if not self.last_refreshed_at:
            return True
        return datetime.utcnow() > self.last_refreshed_at.replace(tzinfo=None) + timedelta(hours=hours)
    
    def start_generation(self, user_id: str):
        """开始生成报表"""
        self.status = "generating"
        self.generated_by = user_id
        self.generation_started_at = datetime.utcnow()
        self.generation_progress = 0.0
        self.error_message = None
    
    def complete_generation(self, data: Dict, summary: Dict = None, charts: Dict = None):
        """完成报表生成"""
        self.status = "completed"
        self.generation_completed_at = datetime.utcnow()
        self.last_refreshed_at = datetime.utcnow()
        self.generation_progress = 100.0
        self.report_data = data
        if summary:
            self.summary_metrics = summary
        if charts:
            self.chart_data = charts
    
    def fail_generation(self, error: str):
        """标记生成失败"""
        self.status = "failed"
        self.generation_completed_at = datetime.utcnow()
        self.error_message = error
    
    def update_progress(self, progress: float):
        """更新生成进度"""
        self.generation_progress = max(0, min(100, progress))
    
    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        self.last_viewed_at = datetime.utcnow()
    
    def increment_export_count(self):
        """增加导出次数"""
        self.export_count += 1
    
    def get_filters(self) -> Dict:
        """获取过滤条件"""
        return self.filters or {}
    
    def get_parameters(self) -> Dict:
        """获取参数配置"""
        return self.parameters or {}
    
    def get_summary_metrics(self) -> Dict:
        """获取汇总指标"""
        return self.summary_metrics or {}
    
    def get_chart_data(self) -> Dict:
        """获取图表数据"""
        return self.chart_data or {}
    
    def can_access(self, user_id: str, user_roles: List[str]) -> bool:
        """检查用户是否可以访问"""
        # 创建者可以访问
        if str(self.created_by) == user_id:
            return True
        
        # 公开报表可以访问
        if self.is_public:
            return True
        
        # 检查共享权限
        if self.shared_with:
            shared_users = self.shared_with.get('users', [])
            shared_roles = self.shared_with.get('roles', [])
            
            if user_id in shared_users:
                return True
            
            for role in user_roles:
                if role in shared_roles:
                    return True
        
        return False


class Dashboard(Base):
    """仪表板表模型"""
    __tablename__ = "dashboards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # 仪表板配置
    layout_config = Column(JSONB, nullable=False)  # 布局配置
    theme_config = Column(JSONB)  # 主题配置
    refresh_interval = Column(Integer, default=300)  # 刷新间隔（秒）
    
    # 权限设置
    is_public = Column(Boolean, default=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    shared_with = Column(JSONB)  # 共享设置
    
    # 状态信息
    is_active = Column(Boolean, default=True, index=True)
    is_default = Column(Boolean, default=False)  # 是否为默认仪表板
    
    # 使用统计
    view_count = Column(Integer, default=0)
    last_viewed_at = Column(DateTime(timezone=True))
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    owner = relationship("User")
    reports = relationship("AnalyticsReport", secondary="dashboard_reports", back_populates="dashboards")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dashboard(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
    
    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        self.last_viewed_at = datetime.utcnow()
    
    def get_layout_config(self) -> Dict:
        """获取布局配置"""
        return self.layout_config or {}
    
    def get_theme_config(self) -> Dict:
        """获取主题配置"""
        return self.theme_config or {}
    
    def can_access(self, user_id: str, user_roles: List[str]) -> bool:
        """检查用户是否可以访问"""
        # 所有者可以访问
        if str(self.owner_id) == user_id:
            return True
        
        # 公开仪表板可以访问
        if self.is_public:
            return True
        
        # 检查共享权限
        if self.shared_with:
            shared_users = self.shared_with.get('users', [])
            shared_roles = self.shared_with.get('roles', [])
            
            if user_id in shared_users:
                return True
            
            for role in user_roles:
                if role in shared_roles:
                    return True
        
        return False
    
    def can_edit(self, user_id: str) -> bool:
        """检查用户是否可以编辑"""
        return str(self.owner_id) == user_id


class DashboardWidget(Base):
    """仪表板组件表模型"""
    __tablename__ = "dashboard_widgets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 组件基本信息
    title = Column(String(200), nullable=False)
    widget_type = Column(String(50), nullable=False, index=True)  # chart, metric, table, text
    
    # 布局信息
    position_x = Column(Integer, nullable=False, default=0)
    position_y = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=4)
    height = Column(Integer, nullable=False, default=3)
    
    # 组件配置
    widget_config = Column(JSONB, nullable=False)  # 组件配置
    data_source_config = Column(JSONB)  # 数据源配置
    style_config = Column(JSONB)  # 样式配置
    
    # 数据设置
    data_query = Column(Text)  # 数据查询
    refresh_interval = Column(Integer, default=300)  # 刷新间隔（秒）
    last_refreshed_at = Column(DateTime(timezone=True))
    
    # 缓存数据
    cached_data = Column(JSONB)  # 缓存的数据
    cache_expires_at = Column(DateTime(timezone=True))
    
    # 状态信息
    is_active = Column(Boolean, default=True, index=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    dashboard = relationship("Dashboard", back_populates="widgets")
    
    def __repr__(self):
        return f"<DashboardWidget(id={self.id}, title={self.title}, type={self.widget_type})>"
    
    @property
    def is_cache_expired(self) -> bool:
        """检查缓存是否过期"""
        if not self.cache_expires_at:
            return True
        return datetime.utcnow() > self.cache_expires_at.replace(tzinfo=None)
    
    def update_cached_data(self, data: Dict, cache_duration_minutes: int = 5):
        """更新缓存数据"""
        self.cached_data = data
        self.last_refreshed_at = datetime.utcnow()
        self.cache_expires_at = datetime.utcnow() + timedelta(minutes=cache_duration_minutes)
    
    def get_widget_config(self) -> Dict:
        """获取组件配置"""
        return self.widget_config or {}
    
    def get_data_source_config(self) -> Dict:
        """获取数据源配置"""
        return self.data_source_config or {}
    
    def get_style_config(self) -> Dict:
        """获取样式配置"""
        return self.style_config or {}
    
    def get_cached_data(self) -> Optional[Dict]:
        """获取缓存数据"""
        if self.is_cache_expired:
            return None
        return self.cached_data


class DashboardReport(Base):
    """仪表板报表关联表模型"""
    __tablename__ = "dashboard_reports"
    
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id", ondelete="CASCADE"), primary_key=True)
    report_id = Column(UUID(as_uuid=True), ForeignKey("analytics_reports.id", ondelete="CASCADE"), primary_key=True)
    
    # 关联配置
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DataMetric(Base):
    """数据指标表模型"""
    __tablename__ = "data_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_key = Column(String(100), unique=True, nullable=False, index=True)  # 指标唯一标识
    
    # 指标基本信息
    description = Column(Text)
    category = Column(String(50), index=True)  # 指标分类
    unit = Column(String(20))  # 单位
    
    # 计算配置
    calculation_method = Column(String(50), nullable=False)  # sum, avg, count, max, min, custom
    calculation_formula = Column(Text)  # 计算公式
    data_source = Column(String(50), nullable=False)  # 数据源
    
    # 数据查询
    source_table = Column(String(100))  # 源表
    source_field = Column(String(100))  # 源字段
    filter_conditions = Column(JSONB)  # 过滤条件
    group_by_fields = Column(JSONB)  # 分组字段
    
    # 时间维度
    time_dimension = Column(String(50))  # 时间维度字段
    time_granularity = Column(String(20), default="day")  # hour, day, week, month, quarter, year
    
    # 阈值设置
    target_value = Column(Numeric(15, 4))  # 目标值
    warning_threshold = Column(Numeric(15, 4))  # 警告阈值
    critical_threshold = Column(Numeric(15, 4))  # 严重阈值
    
    # 显示配置
    display_format = Column(String(50), default="number")  # number, percentage, currency, duration
    decimal_places = Column(Integer, default=2)  # 小数位数
    
    # 更新配置
    update_frequency = Column(String(20), default="daily")  # real_time, hourly, daily, weekly
    last_calculated_at = Column(DateTime(timezone=True))
    next_calculation_at = Column(DateTime(timezone=True))
    
    # 状态信息
    is_active = Column(Boolean, default=True, index=True)
    
    # 创建信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User")
    values = relationship("MetricValue", back_populates="metric", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DataMetric(id={self.id}, name={self.metric_name}, key={self.metric_key})>"
    
    def schedule_next_calculation(self):
        """安排下次计算"""
        frequency_hours = {
            'real_time': 0,
            'hourly': 1,
            'daily': 24,
            'weekly': 168
        }
        hours = frequency_hours.get(self.update_frequency, 24)
        if hours > 0:
            self.next_calculation_at = datetime.utcnow() + timedelta(hours=hours)
    
    def is_due_for_calculation(self) -> bool:
        """检查是否到计算时间"""
        if not self.is_active:
            return False
        if not self.next_calculation_at:
            return True
        return datetime.utcnow() >= self.next_calculation_at.replace(tzinfo=None)
    
    def get_filter_conditions(self) -> Dict:
        """获取过滤条件"""
        return self.filter_conditions or {}
    
    def get_group_by_fields(self) -> List[str]:
        """获取分组字段"""
        return self.group_by_fields or []


class MetricValue(Base):
    """指标值表模型"""
    __tablename__ = "metric_values"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("data_metrics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 时间维度
    time_period = Column(DateTime(timezone=True), nullable=False, index=True)
    time_granularity = Column(String(20), nullable=False, index=True)
    
    # 维度信息
    dimensions = Column(JSONB)  # 维度值（如部门、项目等）
    
    # 指标值
    value = Column(Numeric(15, 4), nullable=False)
    previous_value = Column(Numeric(15, 4))  # 上期值
    
    # 计算信息
    calculation_method = Column(String(50))
    data_points_count = Column(Integer)  # 数据点数量
    
    # 状态信息
    status = Column(String(20), default="normal")  # normal, warning, critical
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    metric = relationship("DataMetric", back_populates="values")
    
    def __repr__(self):
        return f"<MetricValue(id={self.id}, metric_id={self.metric_id}, value={self.value})>"
    
    @property
    def change_percentage(self) -> Optional[float]:
        """计算变化百分比"""
        if self.previous_value and self.previous_value != 0:
            return ((float(self.value) - float(self.previous_value)) / float(self.previous_value)) * 100
        return None
    
    @property
    def change_amount(self) -> Optional[float]:
        """计算变化量"""
        if self.previous_value:
            return float(self.value) - float(self.previous_value)
        return None
    
    def get_dimensions(self) -> Dict:
        """获取维度信息"""
        return self.dimensions or {}
    
    def set_status_by_thresholds(self, warning_threshold: float = None, critical_threshold: float = None):
        """根据阈值设置状态"""
        value = float(self.value)
        
        if critical_threshold and value >= critical_threshold:
            self.status = "critical"
        elif warning_threshold and value >= warning_threshold:
            self.status = "warning"
        else:
            self.status = "normal"


class ReportTemplate(Base):
    """报表模板表模型"""
    __tablename__ = "report_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    template_name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # 模板配置
    template_type = Column(String(50), nullable=False, index=True)
    category = Column(String(50), index=True)
    
    # 模板定义
    template_config = Column(JSONB, nullable=False)  # 模板配置
    default_parameters = Column(JSONB)  # 默认参数
    required_parameters = Column(JSONB)  # 必需参数
    
    # 数据源配置
    data_sources = Column(JSONB)  # 数据源配置
    sql_templates = Column(JSONB)  # SQL模板
    
    # 布局配置
    layout_config = Column(JSONB)  # 布局配置
    style_config = Column(JSONB)  # 样式配置
    
    # 权限设置
    is_public = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 使用统计
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # 版本信息
    version = Column(String(20), default="1.0")
    is_active = Column(Boolean, default=True, index=True)
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    creator = relationship("User")
    
    def __repr__(self):
        return f"<ReportTemplate(id={self.id}, name={self.template_name}, type={self.template_type})>"
    
    def increment_usage_count(self):
        """增加使用次数"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
    
    def get_template_config(self) -> Dict:
        """获取模板配置"""
        return self.template_config or {}
    
    def get_default_parameters(self) -> Dict:
        """获取默认参数"""
        return self.default_parameters or {}
    
    def get_required_parameters(self) -> List[str]:
        """获取必需参数列表"""
        return self.required_parameters or []
    
    def validate_parameters(self, parameters: Dict) -> List[str]:
        """验证参数，返回缺失的必需参数列表"""
        required = self.get_required_parameters()
        missing = []
        
        for param in required:
            if param not in parameters or parameters[param] is None:
                missing.append(param)
        
        return missing