"""审批流程API端点

提供审批请求、审批步骤、审批工作流等相关功能的API接口。
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_permissions
from app.models.auth import User
from app.models.approval import (
    ApprovalRequest, ApprovalStep, ApprovalWorkflow, 
    ApprovalComment, ApprovalHistory, ApprovalDelegate
)
from app.schemas.base import (
    SuccessResponse, PaginatedResponse, BulkOperationRequest, BulkOperationResponse
)
from app.schemas.approval import (
    ApprovalRequestCreate, ApprovalRequestUpdate, ApprovalRequestResponse,
    ApprovalStepCreate, ApprovalStepUpdate, ApprovalStepResponse,
    ApprovalWorkflowCreate, ApprovalWorkflowUpdate, ApprovalWorkflowResponse,
    ApprovalCommentCreate, ApprovalCommentResponse,
    ApprovalHistoryResponse, ApprovalDelegateCreate, ApprovalDelegateResponse
)

router = APIRouter()

# 审批请求相关端点
@router.get("/requests", response_model=PaginatedResponse[ApprovalRequestResponse])
async def get_approval_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    requester_id: Optional[int] = Query(None),
    approver_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审批请求列表"""
    query = db.query(ApprovalRequest)
    
    # 应用过滤条件
    if status:
        query = query.filter(ApprovalRequest.status == status)
    if type:
        query = query.filter(ApprovalRequest.type == type)
    if priority:
        query = query.filter(ApprovalRequest.priority == priority)
    if requester_id:
        query = query.filter(ApprovalRequest.requester_id == requester_id)
    if approver_id:
        query = query.filter(ApprovalRequest.current_approver_id == approver_id)
    
    total = query.count()
    requests = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=requests,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/requests/{request_id}", response_model=ApprovalRequestResponse)
async def get_approval_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审批请求详情"""
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    return request

@router.post("/requests", response_model=ApprovalRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_request(
    request_data: ApprovalRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建审批请求"""
    request = ApprovalRequest(
        **request_data.dict(),
        requester_id=current_user.id
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

@router.put("/requests/{request_id}", response_model=ApprovalRequestResponse)
async def update_approval_request(
    request_id: int,
    request_data: ApprovalRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新审批请求"""
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    
    # 检查权限：只有请求者或管理员可以更新
    if request.requester_id != current_user.id:
        require_permissions(current_user, ["approval:manage"])
    
    for field, value in request_data.dict(exclude_unset=True).items():
        setattr(request, field, value)
    
    db.commit()
    db.refresh(request)
    return request

@router.delete("/requests/{request_id}", response_model=SuccessResponse)
async def delete_approval_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:manage"]))
):
    """删除审批请求"""
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    
    db.delete(request)
    db.commit()
    return SuccessResponse(message="审批请求删除成功")

@router.post("/requests/{request_id}/approve", response_model=SuccessResponse)
async def approve_request(
    request_id: int,
    comment: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批准审批请求"""
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    
    # 检查是否为当前审批人
    if request.current_approver_id != current_user.id:
        raise HTTPException(status_code=403, detail="您不是当前审批人")
    
    # 更新审批状态
    request.status = "approved"
    request.approved_at = db.func.now()
    request.approved_by_id = current_user.id
    
    # 添加审批评论
    if comment:
        approval_comment = ApprovalComment(
            request_id=request_id,
            user_id=current_user.id,
            comment=comment,
            action="approve"
        )
        db.add(approval_comment)
    
    # 记录审批历史
    history = ApprovalHistory(
        request_id=request_id,
        user_id=current_user.id,
        action="approve",
        comment=comment
    )
    db.add(history)
    
    db.commit()
    return SuccessResponse(message="审批请求已批准")

@router.post("/requests/{request_id}/reject", response_model=SuccessResponse)
async def reject_request(
    request_id: int,
    comment: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """拒绝审批请求"""
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    
    # 检查是否为当前审批人
    if request.current_approver_id != current_user.id:
        raise HTTPException(status_code=403, detail="您不是当前审批人")
    
    # 更新审批状态
    request.status = "rejected"
    request.rejected_at = db.func.now()
    request.rejected_by_id = current_user.id
    
    # 添加审批评论
    approval_comment = ApprovalComment(
        request_id=request_id,
        user_id=current_user.id,
        comment=comment,
        action="reject"
    )
    db.add(approval_comment)
    
    # 记录审批历史
    history = ApprovalHistory(
        request_id=request_id,
        user_id=current_user.id,
        action="reject",
        comment=comment
    )
    db.add(history)
    
    db.commit()
    return SuccessResponse(message="审批请求已拒绝")

# 审批工作流相关端点
@router.get("/workflows", response_model=List[ApprovalWorkflowResponse])
async def get_approval_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:view"]))
):
    """获取审批工作流列表"""
    workflows = db.query(ApprovalWorkflow).filter(ApprovalWorkflow.is_active == True).all()
    return workflows

@router.get("/workflows/{workflow_id}", response_model=ApprovalWorkflowResponse)
async def get_approval_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:view"]))
):
    """获取审批工作流详情"""
    workflow = db.query(ApprovalWorkflow).filter(ApprovalWorkflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="审批工作流不存在")
    return workflow

@router.post("/workflows", response_model=ApprovalWorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_workflow(
    workflow_data: ApprovalWorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:manage"]))
):
    """创建审批工作流"""
    workflow = ApprovalWorkflow(**workflow_data.dict())
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

@router.put("/workflows/{workflow_id}", response_model=ApprovalWorkflowResponse)
async def update_approval_workflow(
    workflow_id: int,
    workflow_data: ApprovalWorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:manage"]))
):
    """更新审批工作流"""
    workflow = db.query(ApprovalWorkflow).filter(ApprovalWorkflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="审批工作流不存在")
    
    for field, value in workflow_data.dict(exclude_unset=True).items():
        setattr(workflow, field, value)
    
    db.commit()
    db.refresh(workflow)
    return workflow

@router.delete("/workflows/{workflow_id}", response_model=SuccessResponse)
async def delete_approval_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(["approval:manage"]))
):
    """删除审批工作流"""
    workflow = db.query(ApprovalWorkflow).filter(ApprovalWorkflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="审批工作流不存在")
    
    db.delete(workflow)
    db.commit()
    return SuccessResponse(message="审批工作流删除成功")

# 审批评论相关端点
@router.get("/requests/{request_id}/comments", response_model=List[ApprovalCommentResponse])
async def get_approval_comments(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审批评论列表"""
    comments = db.query(ApprovalComment).filter(
        ApprovalComment.request_id == request_id
    ).order_by(ApprovalComment.created_at.desc()).all()
    return comments

@router.post("/requests/{request_id}/comments", response_model=ApprovalCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_comment(
    request_id: int,
    comment_data: ApprovalCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建审批评论"""
    # 检查审批请求是否存在
    request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="审批请求不存在")
    
    comment = ApprovalComment(
        **comment_data.dict(),
        request_id=request_id,
        user_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# 审批历史相关端点
@router.get("/requests/{request_id}/history", response_model=List[ApprovalHistoryResponse])
async def get_approval_history(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审批历史"""
    history = db.query(ApprovalHistory).filter(
        ApprovalHistory.request_id == request_id
    ).order_by(ApprovalHistory.created_at.desc()).all()
    return history

# 审批委托相关端点
@router.get("/delegates", response_model=List[ApprovalDelegateResponse])
async def get_approval_delegates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的审批委托列表"""
    delegates = db.query(ApprovalDelegate).filter(
        ApprovalDelegate.delegator_id == current_user.id,
        ApprovalDelegate.is_active == True
    ).all()
    return delegates

@router.post("/delegates", response_model=ApprovalDelegateResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_delegate(
    delegate_data: ApprovalDelegateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建审批委托"""
    delegate = ApprovalDelegate(
        **delegate_data.dict(),
        delegator_id=current_user.id
    )
    db.add(delegate)
    db.commit()
    db.refresh(delegate)
    return delegate

@router.delete("/delegates/{delegate_id}", response_model=SuccessResponse)
async def delete_approval_delegate(
    delegate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除审批委托"""
    delegate = db.query(ApprovalDelegate).filter(
        ApprovalDelegate.id == delegate_id,
        ApprovalDelegate.delegator_id == current_user.id
    ).first()
    if not delegate:
        raise HTTPException(status_code=404, detail="审批委托不存在")
    
    db.delete(delegate)
    db.commit()
    return SuccessResponse(message="审批委托删除成功")