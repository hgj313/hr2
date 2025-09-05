from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.config import settings


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户CRUD操作"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_employee_id(self, db: Session, *, employee_id: str) -> Optional[User]:
        """根据员工ID获取用户"""
        return db.query(User).filter(User.employee_id == employee_id).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            employee_id=obj_in.employee_id,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            department_id=obj_in.department_id,
            position_id=obj_in.position_id,
            role=obj_in.role,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """更新用户"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # 如果更新密码，需要加密
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """用户认证"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """检查用户是否活跃"""
        return user.is_active and not user.is_deleted
    
    def is_superuser(self, user: User) -> bool:
        """检查用户是否为超级用户"""
        return user.is_superuser
    
    def activate_user(self, db: Session, *, user: User) -> User:
        """激活用户"""
        user.is_active = True
        user.email_verified = True
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def deactivate_user(self, db: Session, *, user: User) -> User:
        """停用用户"""
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def verify_email(self, db: Session, *, user: User) -> User:
        """验证邮箱"""
        user.email_verified = True
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_last_login(self, db: Session, *, user: User) -> User:
        """更新最后登录时间"""
        user.last_login_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def lock_user(self, db: Session, *, user: User, reason: str = None) -> User:
        """锁定用户"""
        user.is_locked = True
        user.locked_at = datetime.utcnow()
        user.lock_reason = reason
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def unlock_user(self, db: Session, *, user: User) -> User:
        """解锁用户"""
        user.is_locked = False
        user.locked_at = None
        user.lock_reason = None
        user.failed_login_attempts = 0
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def increment_failed_login(self, db: Session, *, user: User) -> User:
        """增加失败登录次数"""
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
        user.last_failed_login_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        
        # 如果失败次数超过限制，锁定用户
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.is_locked = True
            user.locked_at = datetime.utcnow()
            user.lock_reason = f"连续{settings.MAX_LOGIN_ATTEMPTS}次登录失败"
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def reset_failed_login(self, db: Session, *, user: User) -> User:
        """重置失败登录次数"""
        user.failed_login_attempts = 0
        user.last_failed_login_at = None
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def change_password(self, db: Session, *, user: User, new_password: str) -> User:
        """修改密码"""
        user.hashed_password = get_password_hash(new_password)
        user.password_changed_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_users_by_department(
        self, 
        db: Session, 
        *, 
        department_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """根据部门获取用户列表"""
        return db.query(User).filter(
            User.department_id == department_id,
            User.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def get_users_by_position(
        self, 
        db: Session, 
        *, 
        position_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """根据职位获取用户列表"""
        return db.query(User).filter(
            User.position_id == position_id,
            User.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def get_users_by_role(
        self, 
        db: Session, 
        *, 
        role: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """根据角色获取用户列表"""
        return db.query(User).filter(
            User.role == role,
            User.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def search_users(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[User], int]:
        """搜索用户"""
        search_query = db.query(User).filter(
            User.is_deleted == False,
            or_(
                User.full_name.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
                User.employee_id.ilike(f"%{query}%")
            )
        )
        
        total = search_query.count()
        users = search_query.offset(skip).limit(limit).all()
        return users, total
    
    def get_user_statistics(self, db: Session) -> Dict[str, Any]:
        """获取用户统计信息"""
        total_users = db.query(User).filter(User.is_deleted == False).count()
        active_users = db.query(User).filter(
            User.is_deleted == False,
            User.is_active == True
        ).count()
        locked_users = db.query(User).filter(
            User.is_deleted == False,
            User.is_locked == True
        ).count()
        unverified_users = db.query(User).filter(
            User.is_deleted == False,
            User.email_verified == False
        ).count()
        
        # 最近30天新增用户
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        new_users_30d = db.query(User).filter(
            User.is_deleted == False,
            User.created_at >= thirty_days_ago
        ).count()
        
        # 最近7天活跃用户
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users_7d = db.query(User).filter(
            User.is_deleted == False,
            User.last_login_at >= seven_days_ago
        ).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "locked_users": locked_users,
            "unverified_users": unverified_users,
            "new_users_30d": new_users_30d,
            "active_users_7d": active_users_7d,
            "inactive_users": total_users - active_users
        }
    
    def get_users_by_filters(
        self,
        db: Session,
        *,
        department_id: Optional[int] = None,
        position_id: Optional[int] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_locked: Optional[bool] = None,
        email_verified: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> tuple[List[User], int]:
        """根据多个条件过滤用户"""
        query = db.query(User).filter(User.is_deleted == False)
        
        if department_id is not None:
            query = query.filter(User.department_id == department_id)
        if position_id is not None:
            query = query.filter(User.position_id == position_id)
        if role is not None:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        if is_locked is not None:
            query = query.filter(User.is_locked == is_locked)
        if email_verified is not None:
            query = query.filter(User.email_verified == email_verified)
        
        # 排序
        if hasattr(User, order_by):
            column = getattr(User, order_by)
            if order_desc:
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total
    
    def get_password_reset_candidates(self, db: Session) -> List[User]:
        """获取需要重置密码的用户（密码过期）"""
        if not settings.PASSWORD_EXPIRE_DAYS:
            return []
        
        expire_date = datetime.utcnow() - timedelta(days=settings.PASSWORD_EXPIRE_DAYS)
        return db.query(User).filter(
            User.is_deleted == False,
            User.is_active == True,
            or_(
                User.password_changed_at < expire_date,
                User.password_changed_at.is_(None)
            )
        ).all()
    
    def get_inactive_users(self, db: Session, *, days: int = 90) -> List[User]:
        """获取长期未登录的用户"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(User).filter(
            User.is_deleted == False,
            User.is_active == True,
            or_(
                User.last_login_at < cutoff_date,
                User.last_login_at.is_(None)
            )
        ).all()


user = CRUDUser(User)