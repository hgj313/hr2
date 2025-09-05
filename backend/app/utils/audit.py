from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import json
import logging

from app.models.auth import UserActivity
from app.core.config import settings

logger = logging.getLogger(__name__)


class AuditLogger:
    """审计日志记录器"""
    
    def __init__(self):
        self.enabled = settings.AUDIT_LOG_ENABLED
    
    async def log_activity(
        self,
        db: Session,
        user_id: Optional[int],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> Optional[UserActivity]:
        """记录用户活动"""
        if not self.enabled:
            return None
        
        try:
            activity = UserActivity(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details=json.dumps(details) if details else None,
                success=success,
                timestamp=datetime.utcnow()
            )
            
            db.add(activity)
            db.commit()
            db.refresh(activity)
            
            # 记录到应用日志
            log_message = f"用户活动: user_id={user_id}, action={action}, success={success}"
            if details:
                log_message += f", details={details}"
            
            if success:
                logger.info(log_message)
            else:
                logger.warning(log_message)
            
            return activity
            
        except Exception as e:
            logger.error(f"记录用户活动失败: {e}")
            db.rollback()
            return None
    
    async def log_security_event(
        self,
        db: Session,
        event_type: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "medium"
    ) -> Optional[UserActivity]:
        """记录安全事件"""
        security_details = {
            "event_type": event_type,
            "severity": severity,
            **(details or {})
        }
        
        return await self.log_activity(
            db=db,
            user_id=user_id,
            action="security_event",
            resource_type="security",
            ip_address=ip_address,
            user_agent=user_agent,
            details=security_details,
            success=True
        )
    
    async def log_data_access(
        self,
        db: Session,
        user_id: int,
        resource_type: str,
        resource_id: Optional[int],
        action: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[UserActivity]:
        """记录数据访问"""
        return await self.log_activity(
            db=db,
            user_id=user_id,
            action=f"data_{action}",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    async def log_permission_check(
        self,
        db: Session,
        user_id: int,
        permission: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        granted: bool = True,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Optional[UserActivity]:
        """记录权限检查"""
        details = {
            "permission": permission,
            "granted": granted
        }
        
        return await self.log_activity(
            db=db,
            user_id=user_id,
            action="permission_check",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            success=granted
        )
    
    async def log_admin_action(
        self,
        db: Session,
        admin_user_id: int,
        action: str,
        target_user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[UserActivity]:
        """记录管理员操作"""
        admin_details = {
            "admin_action": True,
            "target_user_id": target_user_id,
            **(details or {})
        }
        
        return await self.log_activity(
            db=db,
            user_id=admin_user_id,
            action=f"admin_{action}",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=admin_details
        )
    
    def get_user_activities(
        self,
        db: Session,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        success: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[UserActivity], int]:
        """获取用户活动记录"""
        query = db.query(UserActivity)
        
        if user_id:
            query = query.filter(UserActivity.user_id == user_id)
        if action:
            query = query.filter(UserActivity.action.ilike(f"%{action}%"))
        if resource_type:
            query = query.filter(UserActivity.resource_type == resource_type)
        if start_date:
            query = query.filter(UserActivity.timestamp >= start_date)
        if end_date:
            query = query.filter(UserActivity.timestamp <= end_date)
        if success is not None:
            query = query.filter(UserActivity.success == success)
        
        total = query.count()
        activities = query.order_by(UserActivity.timestamp.desc()).offset(skip).limit(limit).all()
        
        return activities, total
    
    def get_security_events(
        self,
        db: Session,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[UserActivity], int]:
        """获取安全事件记录"""
        query = db.query(UserActivity).filter(UserActivity.action == "security_event")
        
        if event_type:
            query = query.filter(UserActivity.details.ilike(f'%"event_type": "{event_type}"%'))
        if severity:
            query = query.filter(UserActivity.details.ilike(f'%"severity": "{severity}"%'))
        if start_date:
            query = query.filter(UserActivity.timestamp >= start_date)
        if end_date:
            query = query.filter(UserActivity.timestamp <= end_date)
        
        total = query.count()
        events = query.order_by(UserActivity.timestamp.desc()).offset(skip).limit(limit).all()
        
        return events, total
    
    async def cleanup_old_activities(
        self,
        db: Session,
        retention_days: Optional[int] = None
    ) -> int:
        """清理旧的活动记录"""
        if not retention_days:
            retention_days = settings.AUDIT_LOG_RETENTION_DAYS
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        try:
            deleted_count = db.query(UserActivity).filter(
                UserActivity.timestamp < cutoff_date
            ).delete()
            
            db.commit()
            logger.info(f"清理了 {deleted_count} 条旧的活动记录")
            return deleted_count
            
        except Exception as e:
            logger.error(f"清理旧活动记录失败: {e}")
            db.rollback()
            return 0


# 全局审计日志记录器实例
audit_logger = AuditLogger()


# 便捷函数
async def log_user_activity(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    success: bool = True
) -> Optional[UserActivity]:
    """记录用户活动的便捷函数"""
    return await audit_logger.log_activity(
        db=db,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        success=success
    )


async def log_security_event(
    db: Session,
    event_type: str,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "medium"
) -> Optional[UserActivity]:
    """记录安全事件的便捷函数"""
    return await audit_logger.log_security_event(
        db=db,
        event_type=event_type,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        severity=severity
    )


async def log_data_access(
    db: Session,
    user_id: int,
    resource_type: str,
    resource_id: Optional[int],
    action: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Optional[UserActivity]:
    """记录数据访问的便捷函数"""
    return await audit_logger.log_data_access(
        db=db,
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )