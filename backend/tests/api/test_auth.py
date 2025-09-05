import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.core.config import settings
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate
from app.core.security import verify_password, create_access_token
from app.models.user import User


@pytest.mark.api
class TestAuth:
    """认证API测试"""
    
    def test_login_success(self, client: TestClient, test_user: User):
        """测试登录成功"""
        login_data = {
            "username": test_user.email,
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user.email
    
    def test_login_invalid_email(self, client: TestClient):
        """测试无效邮箱登录"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 400
        assert "用户名或密码错误" in response.json()["detail"]
    
    def test_login_invalid_password(self, client: TestClient, test_user: User):
        """测试无效密码登录"""
        login_data = {
            "username": test_user.email,
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 400
        assert "用户名或密码错误" in response.json()["detail"]
    
    def test_login_inactive_user(self, client: TestClient, db_session: Session, test_department, test_position):
        """测试非活跃用户登录"""
        # 创建非活跃用户
        user_in = UserCreate(
            email="inactive@example.com",
            username="inactive",
            employee_id="INACTIVE001",
            password="password123",
            full_name="非活跃用户",
            phone="13800138000",
            department_id=test_department.id,
            position_id=test_position.id,
            role="employee",
            is_active=False,
            is_superuser=False
        )
        inactive_user = crud_user.create(db_session, obj_in=user_in)
        
        login_data = {
            "username": inactive_user.email,
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 400
        assert "用户账户已被禁用" in response.json()["detail"]
    
    def test_register_success(self, client: TestClient, test_department, test_position):
        """测试注册成功"""
        register_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "phone": "13800138000",
            "department_id": test_department.id,
            "position_id": test_position.id,
            "role": "employee"
        }
        response = client.post("/api/v1/auth/register", json=register_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == register_data["email"]
        assert data["username"] == register_data["username"]
        assert "id" in data
    
    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """测试重复邮箱注册"""
        register_data = {
            "email": test_user.email,
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "phone": "13800138000",
            "role": "employee"
        }
        response = client.post("/api/v1/auth/register", json=register_data)
        
        assert response.status_code == 400
        assert "邮箱已被注册" in response.json()["detail"]
    
    def test_register_duplicate_username(self, client: TestClient, test_user: User):
        """测试重复用户名注册"""
        register_data = {
            "email": "newuser@example.com",
            "username": test_user.username,
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "phone": "13800138000",
            "role": "employee"
        }
        response = client.post("/api/v1/auth/register", json=register_data)
        
        assert response.status_code == 400
        assert "用户名已被使用" in response.json()["detail"]
    
    def test_register_weak_password(self, client: TestClient):
        """测试弱密码注册"""
        register_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "123",  # 弱密码
            "full_name": "新用户",
            "phone": "13800138000",
            "role": "employee"
        }
        response = client.post("/api/v1/auth/register", json=register_data)
        
        assert response.status_code == 400
        assert "密码强度不足" in response.json()["detail"]
    
    def test_refresh_token_success(self, client: TestClient, test_user: User):
        """测试刷新令牌成功"""
        # 先登录获取刷新令牌
        login_data = {
            "username": test_user.email,
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", data=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # 使用刷新令牌获取新的访问令牌
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self, client: TestClient):
        """测试无效刷新令牌"""
        refresh_data = {"refresh_token": "invalid_token"}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        assert "无效的刷新令牌" in response.json()["detail"]
    
    def test_logout_success(self, client: TestClient, user_token_headers):
        """测试登出成功"""
        response = client.post("/api/v1/auth/logout", headers=user_token_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "登出成功"
    
    def test_logout_without_token(self, client: TestClient):
        """测试未认证登出"""
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == 401
    
    def test_get_current_user_success(self, client: TestClient, user_token_headers, test_user: User):
        """测试获取当前用户信息成功"""
        response = client.get("/api/v1/auth/me", headers=user_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert data["id"] == test_user.id
    
    def test_get_current_user_without_token(self, client: TestClient):
        """测试未认证获取当前用户信息"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_update_current_user_success(self, client: TestClient, user_token_headers, test_user: User):
        """测试更新当前用户信息成功"""
        update_data = {
            "full_name": "更新后的姓名",
            "phone": "13900139000"
        }
        response = client.put("/api/v1/auth/me", json=update_data, headers=user_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone"] == update_data["phone"]
    
    def test_change_password_success(self, client: TestClient, user_token_headers, test_user: User, db_session: Session):
        """测试修改密码成功"""
        change_data = {
            "current_password": "testpassword123",
            "new_password": "newpassword123"
        }
        response = client.post("/api/v1/auth/change-password", json=change_data, headers=user_token_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "密码修改成功"
        
        # 验证新密码
        db_session.refresh(test_user)
        assert verify_password("newpassword123", test_user.hashed_password)
    
    def test_change_password_wrong_current(self, client: TestClient, user_token_headers):
        """测试修改密码时当前密码错误"""
        change_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        response = client.post("/api/v1/auth/change-password", json=change_data, headers=user_token_headers)
        
        assert response.status_code == 400
        assert "当前密码错误" in response.json()["detail"]
    
    def test_change_password_weak_new(self, client: TestClient, user_token_headers):
        """测试修改密码时新密码强度不足"""
        change_data = {
            "current_password": "testpassword123",
            "new_password": "123"  # 弱密码
        }
        response = client.post("/api/v1/auth/change-password", json=change_data, headers=user_token_headers)
        
        assert response.status_code == 400
        assert "密码强度不足" in response.json()["detail"]
    
    @patch('app.utils.email.send_password_reset_email')
    def test_request_password_reset_success(self, mock_send_email, client: TestClient, test_user: User):
        """测试请求密码重置成功"""
        mock_send_email.return_value = True
        
        reset_data = {"email": test_user.email}
        response = client.post("/api/v1/auth/password-reset", json=reset_data)
        
        assert response.status_code == 200
        assert "密码重置邮件已发送" in response.json()["message"]
        mock_send_email.assert_called_once()
    
    def test_request_password_reset_nonexistent_email(self, client: TestClient):
        """测试请求密码重置时邮箱不存在"""
        reset_data = {"email": "nonexistent@example.com"}
        response = client.post("/api/v1/auth/password-reset", json=reset_data)
        
        # 为了安全，即使邮箱不存在也返回成功
        assert response.status_code == 200
        assert "密码重置邮件已发送" in response.json()["message"]
    
    def test_reset_password_success(self, client: TestClient, test_user: User, db_session: Session):
        """测试重置密码成功"""
        # 创建重置令牌
        from app.core.security import create_reset_password_token
        reset_token = create_reset_password_token(test_user.email)
        
        reset_data = {
            "token": reset_token,
            "new_password": "resetpassword123"
        }
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        
        assert response.status_code == 200
        assert response.json()["message"] == "密码重置成功"
        
        # 验证新密码
        db_session.refresh(test_user)
        assert verify_password("resetpassword123", test_user.hashed_password)
    
    def test_reset_password_invalid_token(self, client: TestClient):
        """测试重置密码时令牌无效"""
        reset_data = {
            "token": "invalid_token",
            "new_password": "resetpassword123"
        }
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        
        assert response.status_code == 400
        assert "无效或过期的重置令牌" in response.json()["detail"]
    
    @patch('app.utils.email.send_email_verification')
    def test_verify_email_success(self, mock_send_email, client: TestClient, test_user: User, db_session: Session):
        """测试邮箱验证成功"""
        # 创建验证令牌
        from app.core.security import create_email_verification_token
        verification_token = create_email_verification_token(test_user.email)
        
        verify_data = {"token": verification_token}
        response = client.post("/api/v1/auth/verify-email", json=verify_data)
        
        assert response.status_code == 200
        assert response.json()["message"] == "邮箱验证成功"
        
        # 验证用户邮箱已验证
        db_session.refresh(test_user)
        assert test_user.email_verified is True
    
    def test_verify_email_invalid_token(self, client: TestClient):
        """测试邮箱验证时令牌无效"""
        verify_data = {"token": "invalid_token"}
        response = client.post("/api/v1/auth/verify-email", json=verify_data)
        
        assert response.status_code == 400
        assert "无效或过期的验证令牌" in response.json()["detail"]
    
    def test_get_csrf_token(self, client: TestClient):
        """测试获取CSRF令牌"""
        response = client.get("/api/v1/auth/csrf-token")
        
        assert response.status_code == 200
        data = response.json()
        assert "csrf_token" in data
        assert len(data["csrf_token"]) > 0
    
    def test_get_user_permissions(self, client: TestClient, user_token_headers):
        """测试获取用户权限"""
        response = client.get("/api/v1/auth/permissions", headers=user_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "permissions" in data
        assert "role" in data
        assert isinstance(data["permissions"], list)