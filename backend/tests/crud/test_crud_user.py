import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import verify_password


@pytest.mark.crud
class TestCRUDUser:
    """用户CRUD操作测试"""
    
    def test_create_user(self, db_session: Session, test_department, test_position):
        """测试创建用户"""
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            employee_id="TEST001",
            password="testpassword123",
            full_name="测试用户",
            phone="13800138000",
            department_id=test_department.id,
            position_id=test_position.id,
            role="employee",
            is_active=True,
            is_superuser=False
        )
        user = crud_user.create(db_session, obj_in=user_in)
        
        assert user.email == user_in.email
        assert user.username == user_in.username
        assert user.employee_id == user_in.employee_id
        assert user.full_name == user_in.full_name
        assert user.phone == user_in.phone
        assert user.department_id == user_in.department_id
        assert user.position_id == user_in.position_id
        assert user.role == user_in.role
        assert user.is_active == user_in.is_active
        assert user.is_superuser == user_in.is_superuser
        assert verify_password(user_in.password, user.hashed_password)
        assert user.id is not None
        assert user.created_at is not None
    
    def test_get_user_by_id(self, db_session: Session, test_user: User):
        """测试根据ID获取用户"""
        user = crud_user.get(db_session, id=test_user.id)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    def test_get_user_by_email(self, db_session: Session, test_user: User):
        """测试根据邮箱获取用户"""
        user = crud_user.get_by_email(db_session, email=test_user.email)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    def test_get_user_by_username(self, db_session: Session, test_user: User):
        """测试根据用户名获取用户"""
        user = crud_user.get_by_username(db_session, username=test_user.username)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username
    
    def test_get_user_by_employee_id(self, db_session: Session, test_user: User):
        """测试根据员工ID获取用户"""
        user = crud_user.get_by_employee_id(db_session, employee_id=test_user.employee_id)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.employee_id == test_user.employee_id
    
    def test_get_nonexistent_user(self, db_session: Session):
        """测试获取不存在的用户"""
        user = crud_user.get(db_session, id=99999)
        assert user is None
        
        user = crud_user.get_by_email(db_session, email="nonexistent@example.com")
        assert user is None
        
        user = crud_user.get_by_username(db_session, username="nonexistent")
        assert user is None
        
        user = crud_user.get_by_employee_id(db_session, employee_id="NONEXISTENT")
        assert user is None
    
    def test_update_user(self, db_session: Session, test_user: User):
        """测试更新用户"""
        user_update = UserUpdate(
            full_name="更新后的姓名",
            phone="13900139000",
            is_active=False
        )
        updated_user = crud_user.update(db_session, db_obj=test_user, obj_in=user_update)
        
        assert updated_user.id == test_user.id
        assert updated_user.full_name == "更新后的姓名"
        assert updated_user.phone == "13900139000"
        assert updated_user.is_active is False
        assert updated_user.updated_at is not None
    
    def test_update_user_with_dict(self, db_session: Session, test_user: User):
        """测试使用字典更新用户"""
        update_data = {
            "full_name": "字典更新姓名",
            "phone": "13800138001"
        }
        updated_user = crud_user.update(db_session, db_obj=test_user, obj_in=update_data)
        
        assert updated_user.full_name == "字典更新姓名"
        assert updated_user.phone == "13800138001"
    
    def test_authenticate_user_success(self, db_session: Session, test_user: User):
        """测试用户认证成功"""
        # 假设测试用户的密码是 "testpassword123"
        authenticated_user = crud_user.authenticate(
            db_session, 
            email=test_user.email, 
            password="testpassword123"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
    
    def test_authenticate_user_wrong_password(self, db_session: Session, test_user: User):
        """测试用户认证密码错误"""
        authenticated_user = crud_user.authenticate(
            db_session, 
            email=test_user.email, 
            password="wrongpassword"
        )
        
        assert authenticated_user is None
    
    def test_authenticate_user_nonexistent(self, db_session: Session):
        """测试认证不存在的用户"""
        authenticated_user = crud_user.authenticate(
            db_session, 
            email="nonexistent@example.com", 
            password="password"
        )
        
        assert authenticated_user is None
    
    def test_is_active(self, db_session: Session, test_user: User):
        """测试检查用户是否活跃"""
        # 测试活跃用户
        assert crud_user.is_active(test_user) is True
        
        # 测试非活跃用户
        test_user.is_active = False
        db_session.commit()
        assert crud_user.is_active(test_user) is False
    
    def test_is_superuser(self, db_session: Session, test_superuser: User, test_user: User):
        """测试检查用户是否为超级用户"""
        assert crud_user.is_superuser(test_superuser) is True
        assert crud_user.is_superuser(test_user) is False
    
    def test_activate_user(self, db_session: Session, test_user: User):
        """测试激活用户"""
        # 先停用用户
        test_user.is_active = False
        db_session.commit()
        
        # 激活用户
        activated_user = crud_user.activate(db_session, user=test_user)
        
        assert activated_user.is_active is True
    
    def test_deactivate_user(self, db_session: Session, test_user: User):
        """测试停用用户"""
        deactivated_user = crud_user.deactivate(db_session, user=test_user)
        
        assert deactivated_user.is_active is False
    
    def test_verify_email(self, db_session: Session, test_user: User):
        """测试验证邮箱"""
        # 先设置邮箱未验证
        test_user.email_verified = False
        db_session.commit()
        
        # 验证邮箱
        verified_user = crud_user.verify_email(db_session, user=test_user)
        
        assert verified_user.email_verified is True
        assert verified_user.email_verified_at is not None
    
    def test_update_last_login(self, db_session: Session, test_user: User):
        """测试更新最后登录时间"""
        original_last_login = test_user.last_login_at
        
        updated_user = crud_user.update_last_login(db_session, user=test_user)
        
        assert updated_user.last_login_at is not None
        assert updated_user.last_login_at != original_last_login
    
    def test_lock_user(self, db_session: Session, test_user: User):
        """测试锁定用户"""
        locked_user = crud_user.lock_user(db_session, user=test_user, reason="测试锁定")
        
        assert locked_user.is_locked is True
        assert locked_user.locked_at is not None
        assert locked_user.lock_reason == "测试锁定"
    
    def test_unlock_user(self, db_session: Session, test_user: User):
        """测试解锁用户"""
        # 先锁定用户
        crud_user.lock_user(db_session, user=test_user, reason="测试锁定")
        
        # 解锁用户
        unlocked_user = crud_user.unlock_user(db_session, user=test_user)
        
        assert unlocked_user.is_locked is False
        assert unlocked_user.locked_at is None
        assert unlocked_user.lock_reason is None
    
    def test_increment_failed_login_attempts(self, db_session: Session, test_user: User):
        """测试增加失败登录次数"""
        original_attempts = test_user.failed_login_attempts
        
        updated_user = crud_user.increment_failed_login_attempts(db_session, user=test_user)
        
        assert updated_user.failed_login_attempts == original_attempts + 1
    
    def test_reset_failed_login_attempts(self, db_session: Session, test_user: User):
        """测试重置失败登录次数"""
        # 先增加失败次数
        test_user.failed_login_attempts = 3
        db_session.commit()
        
        # 重置失败次数
        updated_user = crud_user.reset_failed_login_attempts(db_session, user=test_user)
        
        assert updated_user.failed_login_attempts == 0
    
    def test_change_password(self, db_session: Session, test_user: User):
        """测试修改密码"""
        new_password = "newpassword123"
        updated_user = crud_user.change_password(db_session, user=test_user, new_password=new_password)
        
        assert verify_password(new_password, updated_user.hashed_password)
        assert updated_user.password_changed_at is not None
    
    def test_get_users_by_department(self, db_session: Session, test_user: User, test_department):
        """测试根据部门获取用户列表"""
        users = crud_user.get_by_department(db_session, department_id=test_department.id)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
        for user in users:
            assert user.department_id == test_department.id
    
    def test_get_users_by_position(self, db_session: Session, test_user: User, test_position):
        """测试根据职位获取用户列表"""
        users = crud_user.get_by_position(db_session, position_id=test_position.id)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
        for user in users:
            assert user.position_id == test_position.id
    
    def test_get_users_by_role(self, db_session: Session, test_user: User):
        """测试根据角色获取用户列表"""
        users = crud_user.get_by_role(db_session, role=test_user.role)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
        for user in users:
            assert user.role == test_user.role
    
    def test_search_users(self, db_session: Session, test_user: User):
        """测试搜索用户"""
        # 使用用户姓名搜索
        users = crud_user.search(db_session, query=test_user.full_name)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
    
    def test_get_user_statistics(self, db_session: Session, test_user: User, test_superuser: User):
        """测试获取用户统计信息"""
        stats = crud_user.get_statistics(db_session)
        
        assert "total_users" in stats
        assert "active_users" in stats
        assert "locked_users" in stats
        assert "unverified_users" in stats
        assert "new_users_30d" in stats
        assert "active_users_7d" in stats
        assert "inactive_users" in stats
        
        # 验证数据类型和基本逻辑
        assert isinstance(stats["total_users"], int)
        assert stats["total_users"] >= 2  # 至少有测试用户和超级用户
        assert stats["active_users"] <= stats["total_users"]
    
    def test_filter_users(self, db_session: Session, test_user: User, test_department, test_position):
        """测试过滤用户"""
        filters = {
            "department_id": test_department.id,
            "position_id": test_position.id,
            "role": test_user.role,
            "is_active": True
        }
        
        users = crud_user.filter_users(db_session, **filters)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
        
        for user in users:
            assert user.department_id == test_department.id
            assert user.position_id == test_position.id
            assert user.role == test_user.role
            assert user.is_active is True
    
    def test_get_users_need_password_reset(self, db_session: Session, test_user: User):
        """测试获取需要重置密码的用户"""
        # 设置用户需要重置密码
        test_user.password_reset_required = True
        db_session.commit()
        
        users = crud_user.get_users_need_password_reset(db_session)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
        for user in users:
            assert user.password_reset_required is True
    
    def test_get_inactive_users(self, db_session: Session, test_user: User):
        """测试获取长期未登录的用户"""
        from datetime import datetime, timedelta
        
        # 设置用户很久没有登录
        test_user.last_login_at = datetime.utcnow() - timedelta(days=100)
        db_session.commit()
        
        users = crud_user.get_inactive_users(db_session, days=90)
        
        assert len(users) >= 1
        assert any(user.id == test_user.id for user in users)
    
    def test_delete_user(self, db_session: Session, test_department, test_position):
        """测试删除用户（软删除）"""
        # 创建一个用于删除的用户
        user_in = UserCreate(
            email="todelete@example.com",
            username="todelete",
            employee_id="DEL001",
            password="password123",
            full_name="待删除用户",
            phone="13800138000",
            department_id=test_department.id,
            position_id=test_position.id,
            role="employee",
            is_active=True,
            is_superuser=False
        )
        user_to_delete = crud_user.create(db_session, obj_in=user_in)
        
        # 删除用户
        deleted_user = crud_user.remove(db_session, id=user_to_delete.id)
        
        assert deleted_user.is_deleted is True
        assert deleted_user.deleted_at is not None
        
        # 验证软删除后无法通过常规方法获取
        user = crud_user.get(db_session, id=user_to_delete.id)
        assert user is None  # 因为基类的get方法会过滤已删除的记录
    
    def test_get_multi_users(self, db_session: Session, test_user: User, test_superuser: User):
        """测试获取多个用户"""
        users = crud_user.get_multi(db_session, skip=0, limit=10)
        
        assert len(users) >= 2  # 至少有测试用户和超级用户
        user_ids = [user.id for user in users]
        assert test_user.id in user_ids
        assert test_superuser.id in user_ids
    
    def test_count_users(self, db_session: Session):
        """测试统计用户数量"""
        count = crud_user.count(db_session)
        
        assert isinstance(count, int)
        assert count >= 2  # 至少有测试用户和超级用户