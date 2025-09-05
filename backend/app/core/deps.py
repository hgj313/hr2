from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import SessionLocal
from app.core.security import verify_token, TokenType
from app.core.permissions import get_current_user_from_token, PermissionType
from app.models.auth import User


# HTTP Bearer 认证方案
security = HTTPBearer()


def get_db() -> Generator:
    """获取数据库会话"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前认证用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 验证令牌
        payload = verify_token(credentials.credentials, TokenType.ACCESS)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # 从数据库获取用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """获取当前超级用户"""
    from app.core.permissions import permission_manager
    
    if not permission_manager.has_permission(current_user, PermissionType.ADMIN_ALL.value, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（用于可选认证的端点）"""
    if not authorization:
        return None
    
    try:
        # 提取Bearer令牌
        if not authorization.startswith("Bearer "):
            return None
        
        token = authorization.split(" ")[1]
        
        # 验证令牌
        payload = verify_token(token, TokenType.ACCESS)
        if payload is None:
            return None
        
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        # 从数据库获取用户
        user = db.query(User).filter(User.id == user_id).first()
        if user is None or not user.is_active:
            return None
        
        return user
        
    except Exception:
        return None


def get_api_key_user(
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """通过API密钥获取用户"""
    if not x_api_key:
        return None
    
    try:
        # 这里需要实现API密钥验证逻辑
        # 从数据库查找对应的用户
        # 实际实现中需要有API密钥表
        
        # 占位符实现
        return None
        
    except Exception:
        return None


def require_permission(permission: str):
    """权限依赖工厂函数"""
    def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        from app.core.permissions import permission_manager
        
        if not permission_manager.has_permission(current_user, permission, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    
    return permission_dependency


def require_any_permission(*permissions: str):
    """任意权限依赖工厂函数"""
    def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        from app.core.permissions import permission_manager
        
        if not permission_manager.has_any_permission(current_user, list(permissions), db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of permissions {permissions} required"
            )
        return current_user
    
    return permission_dependency


def require_role(role: str):
    """角色依赖工厂函数"""
    def role_dependency(
        current_user: User = Depends(get_current_user)
    ) -> User:
        user_roles = {role.name for role in current_user.roles}
        if role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required"
            )
        return current_user
    
    return role_dependency


def require_any_role(*roles: str):
    """任意角色依赖工厂函数"""
    def role_dependency(
        current_user: User = Depends(get_current_user)
    ) -> User:
        user_roles = {role.name for role in current_user.roles}
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of roles {roles} required"
            )
        return current_user
    
    return role_dependency


def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> dict:
    """分页参数依赖"""
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 1000:
        limit = 100
    
    return {"skip": skip, "limit": limit}


def get_search_params(
    q: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> dict:
    """搜索参数依赖"""
    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"
    
    return {
        "q": q,
        "sort_by": sort_by,
        "sort_order": sort_order
    }


def get_filter_params(
    status: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> dict:
    """过滤参数依赖"""
    return {
        "status": status,
        "category": category,
        "date_from": date_from,
        "date_to": date_to
    }


class RateLimitDependency:
    """速率限制依赖类"""
    
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
    
    def __call__(
        self,
        request,  # Request对象
        current_user: Optional[User] = Depends(get_optional_current_user)
    ):
        # 这里可以实现基于用户或IP的速率限制
        # 实际实现中需要使用Redis或内存存储来跟踪请求频率
        
        # 获取客户端标识
        client_id = None
        if current_user:
            client_id = f"user:{current_user.id}"
        else:
            client_id = f"ip:{request.client.host}"
        
        # 检查速率限制（占位符实现）
        # 实际实现中需要使用Redis的滑动窗口或令牌桶算法
        
        return True


# 常用的速率限制实例
rate_limit_strict = RateLimitDependency(calls=10, period=60)  # 每分钟10次
rate_limit_normal = RateLimitDependency(calls=100, period=60)  # 每分钟100次
rate_limit_loose = RateLimitDependency(calls=1000, period=60)  # 每分钟1000次


# 常用权限依赖实例
require_user_read = require_permission(PermissionType.USER_READ.value)
require_user_write = require_any_permission(
    PermissionType.USER_CREATE.value,
    PermissionType.USER_UPDATE.value
)
require_admin = require_permission(PermissionType.ADMIN_ALL.value)

require_project_access = require_any_permission(
    PermissionType.PROJECT_READ.value,
    PermissionType.PROJECT_CREATE.value,
    PermissionType.PROJECT_UPDATE.value
)

require_schedule_access = require_any_permission(
    PermissionType.SCHEDULE_READ.value,
    PermissionType.SCHEDULE_CREATE.value,
    PermissionType.SCHEDULE_UPDATE.value
)

require_approval_access = require_any_permission(
    PermissionType.APPROVAL_READ.value,
    PermissionType.APPROVAL_CREATE.value,
    PermissionType.APPROVAL_APPROVE.value
)

require_analytics_access = require_any_permission(
    PermissionType.ANALYTICS_READ.value,
    PermissionType.ANALYTICS_CREATE.value
)