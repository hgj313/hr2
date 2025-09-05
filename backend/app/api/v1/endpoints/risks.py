"""风险管控API端点

提供风险评估、风险缓解计划、风险预警等相关功能的API接口。
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user, require_permissions
from app.models.auth import User
from app.models.risk import (
    RiskAssessment, RiskMitigationPlan, RiskAlert, 
    RiskMonitoringRule, RiskReport
)
from app.schemas.base import (
    SuccessResponse, PaginatedResponse, BulkOperationRequest, BulkOperationResponse
)
from app.schemas.risk import (
    RiskAssessmentCreate, RiskAssessmentUpdate, RiskAssessmentResponse,
    RiskMitigationPlanCreate, RiskMitigationPlanUpdate, RiskMitigationPlanResponse,
    RiskAlertCreate, RiskAlertUpdate, RiskAlertResponse,
    RiskMonitoringRuleCreate, RiskMonitoringRuleUpdate, RiskMonitoringRuleResponse,
    RiskReportCreate, RiskReportUpdate, RiskReportResponse
)

router = APIRouter()

# 风险评估相关端点
@router.get("/assessments", response_model=PaginatedResponse[RiskAssessmentResponse])
async def get_risk_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    risk_level: Optional[str] = Query(None),
    risk_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险评估列表"""
    query = db.query(RiskAssessment)
    
    # 应用过滤条件
    if risk_level:
        query = query.filter(RiskAssessment.risk_level == risk_level)
    if risk_type:
        query = query.filter(RiskAssessment.risk_type == risk_type)
    if status:
        query = query.filter(RiskAssessment.status == status)
    if project_id:
        query = query.filter(RiskAssessment.project_id == project_id)
    
    total = query.count()
    assessments = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=assessments,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/assessments/{assessment_id}", response_model=RiskAssessmentResponse)
async def get_risk_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险评估详情"""
    assessment = db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="风险评估不存在")
    return assessment

@router.post("/assessments", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_assessment(
    assessment_data: RiskAssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:create"]))
):
    """创建风险评估"""
    assessment = RiskAssessment(
        **assessment_data.dict(),
        assessor_id=current_user.id
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

@router.put("/assessments/{assessment_id}", response_model=RiskAssessmentResponse)
async def update_risk_assessment(
    assessment_id: int,
    assessment_data: RiskAssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """更新风险评估"""
    assessment = db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="风险评估不存在")
    
    for field, value in assessment_data.dict(exclude_unset=True).items():
        setattr(assessment, field, value)
    
    db.commit()
    db.refresh(assessment)
    return assessment

@router.delete("/assessments/{assessment_id}", response_model=SuccessResponse)
async def delete_risk_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:delete"]))
):
    """删除风险评估"""
    assessment = db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="风险评估不存在")
    
    db.delete(assessment)
    db.commit()
    return SuccessResponse(message="风险评估删除成功")

# 风险缓解计划相关端点
@router.get("/mitigation-plans", response_model=List[RiskMitigationPlanResponse])
async def get_risk_mitigation_plans(
    risk_assessment_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险缓解计划列表"""
    query = db.query(RiskMitigationPlan)
    
    if risk_assessment_id:
        query = query.filter(RiskMitigationPlan.risk_assessment_id == risk_assessment_id)
    if status:
        query = query.filter(RiskMitigationPlan.status == status)
    
    plans = query.all()
    return plans

@router.get("/mitigation-plans/{plan_id}", response_model=RiskMitigationPlanResponse)
async def get_risk_mitigation_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险缓解计划详情"""
    plan = db.query(RiskMitigationPlan).filter(RiskMitigationPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="风险缓解计划不存在")
    return plan

@router.post("/mitigation-plans", response_model=RiskMitigationPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_mitigation_plan(
    plan_data: RiskMitigationPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:create"]))
):
    """创建风险缓解计划"""
    plan = RiskMitigationPlan(
        **plan_data.dict(),
        created_by_id=current_user.id
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

@router.put("/mitigation-plans/{plan_id}", response_model=RiskMitigationPlanResponse)
async def update_risk_mitigation_plan(
    plan_id: int,
    plan_data: RiskMitigationPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """更新风险缓解计划"""
    plan = db.query(RiskMitigationPlan).filter(RiskMitigationPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="风险缓解计划不存在")
    
    for field, value in plan_data.dict(exclude_unset=True).items():
        setattr(plan, field, value)
    
    db.commit()
    db.refresh(plan)
    return plan

@router.delete("/mitigation-plans/{plan_id}", response_model=SuccessResponse)
async def delete_risk_mitigation_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:delete"]))
):
    """删除风险缓解计划"""
    plan = db.query(RiskMitigationPlan).filter(RiskMitigationPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="风险缓解计划不存在")
    
    db.delete(plan)
    db.commit()
    return SuccessResponse(message="风险缓解计划删除成功")

# 风险预警相关端点
@router.get("/alerts", response_model=PaginatedResponse[RiskAlertResponse])
async def get_risk_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    alert_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    is_resolved: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险预警列表"""
    query = db.query(RiskAlert)
    
    # 应用过滤条件
    if alert_level:
        query = query.filter(RiskAlert.alert_level == alert_level)
    if status:
        query = query.filter(RiskAlert.status == status)
    if is_resolved is not None:
        query = query.filter(RiskAlert.is_resolved == is_resolved)
    
    total = query.count()
    alerts = query.order_by(RiskAlert.created_at.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=alerts,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/alerts/{alert_id}", response_model=RiskAlertResponse)
async def get_risk_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险预警详情"""
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="风险预警不存在")
    return alert

@router.post("/alerts", response_model=RiskAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_alert(
    alert_data: RiskAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:create"]))
):
    """创建风险预警"""
    alert = RiskAlert(**alert_data.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.put("/alerts/{alert_id}", response_model=RiskAlertResponse)
async def update_risk_alert(
    alert_id: int,
    alert_data: RiskAlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """更新风险预警"""
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="风险预警不存在")
    
    for field, value in alert_data.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/alerts/{alert_id}/resolve", response_model=SuccessResponse)
async def resolve_risk_alert(
    alert_id: int,
    resolution_note: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """解决风险预警"""
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="风险预警不存在")
    
    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    alert.resolved_by_id = current_user.id
    if resolution_note:
        alert.resolution_note = resolution_note
    
    db.commit()
    return SuccessResponse(message="风险预警已解决")

# 风险监控规则相关端点
@router.get("/monitoring-rules", response_model=List[RiskMonitoringRuleResponse])
async def get_risk_monitoring_rules(
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险监控规则列表"""
    query = db.query(RiskMonitoringRule)
    
    if is_active is not None:
        query = query.filter(RiskMonitoringRule.is_active == is_active)
    
    rules = query.all()
    return rules

@router.get("/monitoring-rules/{rule_id}", response_model=RiskMonitoringRuleResponse)
async def get_risk_monitoring_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险监控规则详情"""
    rule = db.query(RiskMonitoringRule).filter(RiskMonitoringRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="风险监控规则不存在")
    return rule

@router.post("/monitoring-rules", response_model=RiskMonitoringRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_monitoring_rule(
    rule_data: RiskMonitoringRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:create"]))
):
    """创建风险监控规则"""
    rule = RiskMonitoringRule(
        **rule_data.dict(),
        created_by_id=current_user.id
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.put("/monitoring-rules/{rule_id}", response_model=RiskMonitoringRuleResponse)
async def update_risk_monitoring_rule(
    rule_id: int,
    rule_data: RiskMonitoringRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """更新风险监控规则"""
    rule = db.query(RiskMonitoringRule).filter(RiskMonitoringRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="风险监控规则不存在")
    
    for field, value in rule_data.dict(exclude_unset=True).items():
        setattr(rule, field, value)
    
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/monitoring-rules/{rule_id}", response_model=SuccessResponse)
async def delete_risk_monitoring_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:delete"]))
):
    """删除风险监控规则"""
    rule = db.query(RiskMonitoringRule).filter(RiskMonitoringRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="风险监控规则不存在")
    
    db.delete(rule)
    db.commit()
    return SuccessResponse(message="风险监控规则删除成功")

# 风险报告相关端点
@router.get("/reports", response_model=List[RiskReportResponse])
async def get_risk_reports(
    report_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险报告列表"""
    query = db.query(RiskReport)
    
    if report_type:
        query = query.filter(RiskReport.report_type == report_type)
    
    reports = query.order_by(RiskReport.created_at.desc()).all()
    return reports

@router.get("/reports/{report_id}", response_model=RiskReportResponse)
async def get_risk_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险报告详情"""
    report = db.query(RiskReport).filter(RiskReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="风险报告不存在")
    return report

@router.post("/reports", response_model=RiskReportResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_report(
    report_data: RiskReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:create"]))
):
    """创建风险报告"""
    report = RiskReport(
        **report_data.dict(),
        generated_by_id=current_user.id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.put("/reports/{report_id}", response_model=RiskReportResponse)
async def update_risk_report(
    report_id: int,
    report_data: RiskReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:edit"]))
):
    """更新风险报告"""
    report = db.query(RiskReport).filter(RiskReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="风险报告不存在")
    
    for field, value in report_data.dict(exclude_unset=True).items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    return report

@router.delete("/reports/{report_id}", response_model=SuccessResponse)
async def delete_risk_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:delete"]))
):
    """删除风险报告"""
    report = db.query(RiskReport).filter(RiskReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="风险报告不存在")
    
    db.delete(report)
    db.commit()
    return SuccessResponse(message="风险报告删除成功")

# 风险统计相关端点
@router.get("/statistics", response_model=dict)
async def get_risk_statistics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["risk:view"]))
):
    """获取风险统计信息"""
    # 设置默认时间范围（最近30天）
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # 风险评估统计
    assessment_query = db.query(RiskAssessment).filter(
        RiskAssessment.created_at >= start_date,
        RiskAssessment.created_at <= end_date
    )
    
    total_assessments = assessment_query.count()
    high_risk_count = assessment_query.filter(RiskAssessment.risk_level == "high").count()
    medium_risk_count = assessment_query.filter(RiskAssessment.risk_level == "medium").count()
    low_risk_count = assessment_query.filter(RiskAssessment.risk_level == "low").count()
    
    # 风险预警统计
    alert_query = db.query(RiskAlert).filter(
        RiskAlert.created_at >= start_date,
        RiskAlert.created_at <= end_date
    )
    
    total_alerts = alert_query.count()
    unresolved_alerts = alert_query.filter(RiskAlert.is_resolved == False).count()
    resolved_alerts = alert_query.filter(RiskAlert.is_resolved == True).count()
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "assessments": {
            "total": total_assessments,
            "high_risk": high_risk_count,
            "medium_risk": medium_risk_count,
            "low_risk": low_risk_count
        },
        "alerts": {
            "total": total_alerts,
            "unresolved": unresolved_alerts,
            "resolved": resolved_alerts
        }
    }