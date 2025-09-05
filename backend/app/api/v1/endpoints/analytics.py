"""数据分析API端点

提供分析报表、仪表板、数据指标等相关功能的API接口。
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user, require_permissions
from app.models.auth import User
from app.models.analytics import (
    AnalyticsReport, Dashboard, DashboardWidget, DashboardReport,
    DataMetric, MetricValue, ReportTemplate
)
from app.schemas.base import (
    SuccessResponse, PaginatedResponse, BulkOperationRequest, BulkOperationResponse
)
from app.schemas.analytics import (
    AnalyticsReportCreate, AnalyticsReportUpdate, AnalyticsReportResponse,
    DashboardCreate, DashboardUpdate, DashboardResponse,
    DashboardWidgetCreate, DashboardWidgetUpdate, DashboardWidgetResponse,
    DataMetricCreate, DataMetricUpdate, DataMetricResponse,
    MetricValueCreate, MetricValueResponse,
    ReportTemplateCreate, ReportTemplateUpdate, ReportTemplateResponse
)

router = APIRouter()

# 分析报表相关端点
@router.get("/reports", response_model=PaginatedResponse[AnalyticsReportResponse])
async def get_analytics_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    report_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    data_source: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取分析报表列表"""
    query = db.query(AnalyticsReport)
    
    # 应用过滤条件
    if report_type:
        query = query.filter(AnalyticsReport.report_type == report_type)
    if status:
        query = query.filter(AnalyticsReport.status == status)
    if data_source:
        query = query.filter(AnalyticsReport.data_source == data_source)
    
    total = query.count()
    reports = query.order_by(AnalyticsReport.created_at.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=reports,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/reports/{report_id}", response_model=AnalyticsReportResponse)
async def get_analytics_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取分析报表详情"""
    report = db.query(AnalyticsReport).filter(AnalyticsReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="分析报表不存在")
    return report

@router.post("/reports", response_model=AnalyticsReportResponse, status_code=status.HTTP_201_CREATED)
async def create_analytics_report(
    report_data: AnalyticsReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建分析报表"""
    report = AnalyticsReport(
        **report_data.dict(),
        created_by_id=current_user.id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.put("/reports/{report_id}", response_model=AnalyticsReportResponse)
async def update_analytics_report(
    report_id: int,
    report_data: AnalyticsReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:edit"]))
):
    """更新分析报表"""
    report = db.query(AnalyticsReport).filter(AnalyticsReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="分析报表不存在")
    
    for field, value in report_data.dict(exclude_unset=True).items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    return report

@router.delete("/reports/{report_id}", response_model=SuccessResponse)
async def delete_analytics_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:delete"]))
):
    """删除分析报表"""
    report = db.query(AnalyticsReport).filter(AnalyticsReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="分析报表不存在")
    
    db.delete(report)
    db.commit()
    return SuccessResponse(message="分析报表删除成功")

@router.post("/reports/{report_id}/generate", response_model=SuccessResponse)
async def generate_analytics_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:generate"]))
):
    """生成分析报表"""
    report = db.query(AnalyticsReport).filter(AnalyticsReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="分析报表不存在")
    
    # 更新报表状态为生成中
    report.status = "generating"
    report.last_generated_at = datetime.utcnow()
    db.commit()
    
    # 这里应该触发异步任务来生成报表
    # 暂时直接更新状态为已完成
    report.status = "completed"
    db.commit()
    
    return SuccessResponse(message="分析报表生成成功")

# 仪表板相关端点
@router.get("/dashboards", response_model=List[DashboardResponse])
async def get_dashboards(
    is_public: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取仪表板列表"""
    query = db.query(Dashboard)
    
    # 如果不是管理员，只能看到公开的或自己创建的仪表板
    if not any(role.name == "admin" for role in current_user.roles):
        query = query.filter(
            (Dashboard.is_public == True) | (Dashboard.created_by_id == current_user.id)
        )
    
    if is_public is not None:
        query = query.filter(Dashboard.is_public == is_public)
    
    dashboards = query.order_by(Dashboard.created_at.desc()).all()
    return dashboards

@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取仪表板详情"""
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="仪表板不存在")
    
    # 检查访问权限
    if not dashboard.is_public and dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权访问此仪表板")
    
    return dashboard

@router.post("/dashboards", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    dashboard_data: DashboardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建仪表板"""
    dashboard = Dashboard(
        **dashboard_data.dict(),
        created_by_id=current_user.id
    )
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    return dashboard

@router.put("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: int,
    dashboard_data: DashboardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:edit"]))
):
    """更新仪表板"""
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="仪表板不存在")
    
    # 检查编辑权限
    if dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权编辑此仪表板")
    
    for field, value in dashboard_data.dict(exclude_unset=True).items():
        setattr(dashboard, field, value)
    
    db.commit()
    db.refresh(dashboard)
    return dashboard

@router.delete("/dashboards/{dashboard_id}", response_model=SuccessResponse)
async def delete_dashboard(
    dashboard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:delete"]))
):
    """删除仪表板"""
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="仪表板不存在")
    
    # 检查删除权限
    if dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权删除此仪表板")
    
    db.delete(dashboard)
    db.commit()
    return SuccessResponse(message="仪表板删除成功")

# 仪表板组件相关端点
@router.get("/dashboards/{dashboard_id}/widgets", response_model=List[DashboardWidgetResponse])
async def get_dashboard_widgets(
    dashboard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取仪表板组件列表"""
    # 检查仪表板是否存在和访问权限
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="仪表板不存在")
    
    if not dashboard.is_public and dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权访问此仪表板")
    
    widgets = db.query(DashboardWidget).filter(
        DashboardWidget.dashboard_id == dashboard_id
    ).order_by(DashboardWidget.position).all()
    
    return widgets

@router.post("/dashboards/{dashboard_id}/widgets", response_model=DashboardWidgetResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard_widget(
    dashboard_id: int,
    widget_data: DashboardWidgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建仪表板组件"""
    # 检查仪表板是否存在和编辑权限
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="仪表板不存在")
    
    if dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权编辑此仪表板")
    
    widget = DashboardWidget(
        **widget_data.dict(),
        dashboard_id=dashboard_id
    )
    db.add(widget)
    db.commit()
    db.refresh(widget)
    return widget

@router.put("/widgets/{widget_id}", response_model=DashboardWidgetResponse)
async def update_dashboard_widget(
    widget_id: int,
    widget_data: DashboardWidgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:edit"]))
):
    """更新仪表板组件"""
    widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="仪表板组件不存在")
    
    # 检查编辑权限
    dashboard = widget.dashboard
    if dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权编辑此仪表板组件")
    
    for field, value in widget_data.dict(exclude_unset=True).items():
        setattr(widget, field, value)
    
    db.commit()
    db.refresh(widget)
    return widget

@router.delete("/widgets/{widget_id}", response_model=SuccessResponse)
async def delete_dashboard_widget(
    widget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:delete"]))
):
    """删除仪表板组件"""
    widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="仪表板组件不存在")
    
    # 检查删除权限
    dashboard = widget.dashboard
    if dashboard.created_by_id != current_user.id:
        if not any(role.name == "admin" for role in current_user.roles):
            raise HTTPException(status_code=403, detail="无权删除此仪表板组件")
    
    db.delete(widget)
    db.commit()
    return SuccessResponse(message="仪表板组件删除成功")

# 数据指标相关端点
@router.get("/metrics", response_model=List[DataMetricResponse])
async def get_data_metrics(
    category: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取数据指标列表"""
    query = db.query(DataMetric)
    
    if category:
        query = query.filter(DataMetric.category == category)
    if is_active is not None:
        query = query.filter(DataMetric.is_active == is_active)
    
    metrics = query.order_by(DataMetric.name).all()
    return metrics

@router.get("/metrics/{metric_id}", response_model=DataMetricResponse)
async def get_data_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取数据指标详情"""
    metric = db.query(DataMetric).filter(DataMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="数据指标不存在")
    return metric

@router.post("/metrics", response_model=DataMetricResponse, status_code=status.HTTP_201_CREATED)
async def create_data_metric(
    metric_data: DataMetricCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建数据指标"""
    metric = DataMetric(
        **metric_data.dict(),
        created_by_id=current_user.id
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.put("/metrics/{metric_id}", response_model=DataMetricResponse)
async def update_data_metric(
    metric_id: int,
    metric_data: DataMetricUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:edit"]))
):
    """更新数据指标"""
    metric = db.query(DataMetric).filter(DataMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="数据指标不存在")
    
    for field, value in metric_data.dict(exclude_unset=True).items():
        setattr(metric, field, value)
    
    db.commit()
    db.refresh(metric)
    return metric

@router.delete("/metrics/{metric_id}", response_model=SuccessResponse)
async def delete_data_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:delete"]))
):
    """删除数据指标"""
    metric = db.query(DataMetric).filter(DataMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="数据指标不存在")
    
    db.delete(metric)
    db.commit()
    return SuccessResponse(message="数据指标删除成功")

# 指标值相关端点
@router.get("/metrics/{metric_id}/values", response_model=List[MetricValueResponse])
async def get_metric_values(
    metric_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取指标值列表"""
    query = db.query(MetricValue).filter(MetricValue.metric_id == metric_id)
    
    if start_date:
        query = query.filter(MetricValue.timestamp >= start_date)
    if end_date:
        query = query.filter(MetricValue.timestamp <= end_date)
    
    values = query.order_by(MetricValue.timestamp.desc()).limit(limit).all()
    return values

@router.post("/metrics/{metric_id}/values", response_model=MetricValueResponse, status_code=status.HTTP_201_CREATED)
async def create_metric_value(
    metric_id: int,
    value_data: MetricValueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建指标值"""
    # 检查指标是否存在
    metric = db.query(DataMetric).filter(DataMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="数据指标不存在")
    
    value = MetricValue(
        **value_data.dict(),
        metric_id=metric_id
    )
    db.add(value)
    db.commit()
    db.refresh(value)
    return value

# 报表模板相关端点
@router.get("/templates", response_model=List[ReportTemplateResponse])
async def get_report_templates(
    template_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取报表模板列表"""
    query = db.query(ReportTemplate)
    
    if template_type:
        query = query.filter(ReportTemplate.template_type == template_type)
    if is_active is not None:
        query = query.filter(ReportTemplate.is_active == is_active)
    
    templates = query.order_by(ReportTemplate.name).all()
    return templates

@router.get("/templates/{template_id}", response_model=ReportTemplateResponse)
async def get_report_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取报表模板详情"""
    template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="报表模板不存在")
    return template

@router.post("/templates", response_model=ReportTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_report_template(
    template_data: ReportTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:create"]))
):
    """创建报表模板"""
    template = ReportTemplate(
        **template_data.dict(),
        created_by_id=current_user.id
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

@router.put("/templates/{template_id}", response_model=ReportTemplateResponse)
async def update_report_template(
    template_id: int,
    template_data: ReportTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:edit"]))
):
    """更新报表模板"""
    template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="报表模板不存在")
    
    for field, value in template_data.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template

@router.delete("/templates/{template_id}", response_model=SuccessResponse)
async def delete_report_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:delete"]))
):
    """删除报表模板"""
    template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="报表模板不存在")
    
    db.delete(template)
    db.commit()
    return SuccessResponse(message="报表模板删除成功")

# 数据统计相关端点
@router.get("/statistics", response_model=Dict[str, Any])
async def get_analytics_statistics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["analytics:view"]))
):
    """获取数据分析统计信息"""
    # 设置默认时间范围（最近30天）
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # 报表统计
    total_reports = db.query(AnalyticsReport).count()
    active_reports = db.query(AnalyticsReport).filter(
        AnalyticsReport.status == "active"
    ).count()
    
    # 仪表板统计
    total_dashboards = db.query(Dashboard).count()
    public_dashboards = db.query(Dashboard).filter(
        Dashboard.is_public == True
    ).count()
    
    # 指标统计
    total_metrics = db.query(DataMetric).count()
    active_metrics = db.query(DataMetric).filter(
        DataMetric.is_active == True
    ).count()
    
    # 模板统计
    total_templates = db.query(ReportTemplate).count()
    active_templates = db.query(ReportTemplate).filter(
        ReportTemplate.is_active == True
    ).count()
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "reports": {
            "total": total_reports,
            "active": active_reports
        },
        "dashboards": {
            "total": total_dashboards,
            "public": public_dashboards
        },
        "metrics": {
            "total": total_metrics,
            "active": active_metrics
        },
        "templates": {
            "total": total_templates,
            "active": active_templates
        }
    }