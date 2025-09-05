from typing import List, Optional, Set, Dict, Any
from enum import Enum
from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User, Role, Permission
from app.core.security import verify_token, TokenType


class PermissionType(str, Enum):
    """权限类型枚举"""
    # 用户管理权限
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_LIST = "user:list"
    
    # 组织架构权限
    ORG_CREATE = "organization:create"
    ORG_READ = "organization:read"
    ORG_UPDATE = "organization:update"
    ORG_DELETE = "organization:delete"
    ORG_LIST = "organization:list"
    
    # 项目管理权限
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_LIST = "project:list"
    PROJECT_ASSIGN = "project:assign"
    
    # 调度管理权限
    SCHEDULE_CREATE = "schedule:create"
    SCHEDULE_READ = "schedule:read"
    SCHEDULE_UPDATE = "schedule:update"
    SCHEDULE_DELETE = "schedule:delete"
    SCHEDULE_LIST = "schedule:list"
    SCHEDULE_ASSIGN = "schedule:assign"
    
    # 审批流程权限
    APPROVAL_CREATE = "approval:create"
    APPROVAL_READ = "approval:read"
    APPROVAL_UPDATE = "approval:update"
    APPROVAL_DELETE = "approval:delete"
    APPROVAL_LIST = "approval:list"
    APPROVAL_APPROVE = "approval:approve"
    APPROVAL_REJECT = "approval:reject"
    
    # 风险管控权限
    RISK_CREATE = "risk:create"
    RISK_READ = "risk:read"
    RISK_UPDATE = "risk:update"
    RISK_DELETE = "risk:delete"
    RISK_LIST = "risk:list"
    RISK_ASSESS = "risk:assess"
    
    # 数据分析权限
    ANALYTICS_CREATE = "analytics:create"
    ANALYTICS_READ = "analytics:read"
    ANALYTICS_UPDATE = "analytics:update"
    ANALYTICS_DELETE = "analytics:delete"
    ANALYTICS_LIST = "analytics:list"
    ANALYTICS_EXPORT = "analytics:export"
    
    # 系统管理权限
    SYSTEM_CONFIG = "system:config"
    SYSTEM_MONITOR = "system:monitor"
    SYSTEM_BACKUP = "system:backup"
    SYSTEM_RESTORE = "system:restore"
    
    # 超级管理员权限
    ADMIN_ALL = "admin:all"


class RoleType(str, Enum):
    """角色类型枚举"""
    SUPER_ADMIN = "super_admin"  # 超级管理员
    ADMIN = "admin"  # 系统管理员
    HR_MANAGER = "hr_manager"  # 人力资源经理
    PROJECT_MANAGER = "project_manager"  # 项目经理
    TEAM_LEADER = "team_leader"  # 团队负责人
    EMPLOYEE = "employee"  # 普通员工
    GUEST = "guest"  # 访客


class PermissionManager:
    """权限管理器"""
    
    def __init__(self):
        # 预定义角色权限映射
        self.role_permissions = {
            RoleType.SUPER_ADMIN: [PermissionType.ADMIN_ALL],
            RoleType.ADMIN: [
                PermissionType.USER_CREATE, PermissionType.USER_READ, 
                PermissionType.USER_UPDATE, PermissionType.USER_DELETE, PermissionType.USER_LIST,
                PermissionType.ORG_CREATE, PermissionType.ORG_READ, 
                PermissionType.ORG_UPDATE, PermissionType.ORG_DELETE, PermissionType.ORG_LIST,
                PermissionType.SYSTEM_CONFIG, PermissionType.SYSTEM_MONITOR,
                PermissionType.ANALYTICS_READ, PermissionType.ANALYTICS_LIST, PermissionType.ANALYTICS_EXPORT,
            ],
            RoleType.HR_MANAGER: [
                PermissionType.USER_CREATE, PermissionType.USER_READ, 
                PermissionType.USER_UPDATE, PermissionType.USER_LIST,
                PermissionType.ORG_READ, PermissionType.ORG_UPDATE, PermissionType.ORG_LIST,
                PermissionType.SCHEDULE_CREATE, PermissionType.SCHEDULE_READ, 
                PermissionType.SCHEDULE_UPDATE, PermissionType.SCHEDULE_LIST, PermissionType.SCHEDULE_ASSIGN,
                PermissionType.APPROVAL_READ, PermissionType.APPROVAL_LIST, 
                PermissionType.APPROVAL_APPROVE, PermissionType.APPROVAL_REJECT,
                PermissionType.ANALYTICS_READ, PermissionType.ANALYTICS_LIST,
            ],
            RoleType.PROJECT_MANAGER: [
                PermissionType.USER_READ, PermissionType.USER_LIST,
                PermissionType.PROJECT_CREATE, PermissionType.PROJECT_READ, 
                PermissionType.PROJECT_UPDATE, PermissionType.PROJECT_LIST, PermissionType.PROJECT_ASSIGN,
                PermissionType.SCHEDULE_CREATE, PermissionType.SCHEDULE_READ, 
                PermissionType.SCHEDULE_UPDATE, PermissionType.SCHEDULE_LIST,
                PermissionType.APPROVAL_CREATE, PermissionType.APPROVAL_READ, PermissionType.APPROVAL_LIST,
                PermissionType.RISK_CREATE, PermissionType.RISK_READ, 
                PermissionType.RISK_UPDATE, PermissionType.RISK_LIST, PermissionType.RISK_ASSESS,
                PermissionType.ANALYTICS_READ, PermissionType.ANALYTICS_LIST,
            ],
            RoleType.TEAM_LEADER: [
                PermissionType.USER_READ, PermissionType.USER_LIST,
                PermissionType.PROJECT_READ, PermissionType.PROJECT_LIST,
                PermissionType.SCHEDULE_READ, PermissionType.SCHEDULE_LIST,
                PermissionType.APPROVAL_CREATE, PermissionType.APPROVAL_READ, PermissionType.APPROVAL_LIST,
                PermissionType.RISK_READ, PermissionType.RISK_LIST,
            ],
            RoleType.EMPLOYEE: [
                PermissionType.USER_READ,
                PermissionType.PROJECT_READ, PermissionType.PROJECT_LIST,
                PermissionType.SCHEDULE_READ, PermissionType.SCHEDULE_LIST,
                PermissionType.APPROVAL_CREATE, PermissionType.APPROVAL_READ,
                PermissionType.RISK_READ,
            ],
            RoleType.GUEST: [
                PermissionType.USER_READ,
                PermissionType.PROJECT_READ,
                PermissionType.SCHEDULE_READ,
            ],
        }
    
    def get_user_permissions(self, user: User, db: Session) -> Set[str]:
        """获取用户权限集合"""
        permissions = set()
        
        # 超级管理员拥有所有权限
        if any(role.name == RoleType.SUPER_ADMIN for role in user.roles):
            return {perm.value for perm in PermissionType}
        
        # 从角色获取权限
        for role in user.roles:
            role_perms = self.role_permissions.get(role.name, [])
            permissions.update(perm.value for perm in role_perms)
            
            # 从数据库获取角色的额外权限
            for permission in role.permissions:
                permissions.add(permission.name)
        
        # 用户的直接权限
        for permission in user.permissions:
            permissions.add(permission.name)
        
        return permissions
    
    def has_permission(self, user: User, permission: str, db: Session) -> bool:
        """检查用户是否有指定权限"""
        user_permissions = self.get_user_permissions(user, db)
        
        # 检查是否有超级管理员权限
        if PermissionType.ADMIN_ALL.value in user_permissions:
            return True
        
        return permission in user_permissions
    
    def has_any_permission(self, user: User, permissions: List[str], db: Session) -> bool:
        """检查用户是否有任意一个指定权限"""
        user_permissions = self.get_user_permissions(user, db)
        
        # 检查是否有超级管理员权限
        if PermissionType.ADMIN_ALL.value in user_permissions:
            return True
        
        return any(perm in user_permissions for perm in permissions)
    
    def has_all_permissions(self, user: User, permissions: List[str], db: Session) -> bool:
        """检查用户是否有所有指定权限"""
        user_permissions = self.get_user_permissions(user, db)
        
        # 检查是否有超级管理员权限
        if PermissionType.ADMIN_ALL.value in user_permissions:
            return True
        
        return all(perm in user_permissions for perm in permissions)
    
    def check_resource_access(self, user: User, resource_type: str, resource_id: str, 
                            action: str, db: Session) -> bool:
        """检查用户对特定资源的访问权限"""
        # 构建权限字符串
        permission = f"{resource_type}:{action}"
        
        # 基础权限检查
        if not self.has_permission(user, permission, db):
            return False
        
        # 资源级别的权限检查（可以根据业务需求扩展）
        # 例如：检查用户是否属于资源的组织、项目等
        
        return True
    
    def filter_accessible_resources(self, user: User, resources: List[Dict[str, Any]], 
                                  resource_type: str, action: str, db: Session) -> List[Dict[str, Any]]:
        """过滤用户可访问的资源列表"""
        accessible_resources = []
        
        for resource in resources:
            resource_id = str(resource.get('id', ''))
            if self.check_resource_access(user, resource_type, resource_id, action, db):
                accessible_resources.append(resource)
        
        return accessible_resources


# 全局权限管理器实例
permission_manager = PermissionManager()


def get_current_user_from_token(token: str, db: Session) -> Optional[User]:
    """从令牌获取当前用户"""
    try:
        payload = verify_token(token, TokenType.ACCESS)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
        
    except Exception:
        return None


def require_permissions(*required_permissions: str):
    """权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取数据库会话和用户
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            
            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查权限
            if not permission_manager.has_all_permissions(current_user, list(required_permissions), db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(*required_permissions: str):
    """任意权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取数据库会话和用户
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            
            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查权限
            if not permission_manager.has_any_permission(current_user, list(required_permissions), db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(*required_roles: str):
    """角色检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取数据库会话和用户
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            
            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查角色
            user_roles = {role.name for role in current_user.roles}
            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient role permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_resource_ownership(resource_type: str, user_field: str = "user_id"):
    """资源所有权检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取数据库会话、用户和资源ID
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            resource_id = kwargs.get('id') or kwargs.get('resource_id')
            
            if not db or not current_user or not resource_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 超级管理员跳过所有权检查
            if permission_manager.has_permission(current_user, PermissionType.ADMIN_ALL.value, db):
                return await func(*args, **kwargs)
            
            # 这里需要根据具体的资源类型进行所有权检查
            # 实际实现中需要查询对应的资源表
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# 便捷函数
def has_permission(user: User, permission: str, db: Session) -> bool:
    """检查用户权限的便捷函数"""
    return permission_manager.has_permission(user, permission, db)


def get_user_permissions(user: User, db: Session) -> Set[str]:
    """获取用户权限的便捷函数"""
    return permission_manager.get_user_permissions(user, db)


def check_resource_access(user: User, resource_type: str, resource_id: str, 
                         action: str, db: Session) -> bool:
    """检查资源访问权限的便捷函数"""
    return permission_manager.check_resource_access(user, resource_type, resource_id, action, db)