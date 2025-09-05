import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import User


@pytest.mark.api
class TestUsers:
    """用户管理API测试"""
    
    def test_get_users_success(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试获取用户列表成功"""
        response = client.get("/api/v1/users/", headers=superuser_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert len(data["items"]) >= 1
    
    def test_get_users_with_pagination(self, client: TestClient, superuser_token_headers):
        """测试分页获取用户列表"""
        response = client.get("/api/v1/users/?page=1&size=10", headers=superuser_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 10
    
    def test_get_users_with_filters(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试过滤获取用户列表"""
        response = client.get(
            f"/api/v1/users/?department_id={test_user.department_id}&is_active=true",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        # 验证过滤结果
        for user in data["items"]:
            assert user["department_id"] == test_user.department_id
            assert user["is_active"] is True
    
    def test_get_users_with_search(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试搜索用户"""
        response = client.get(
            f"/api/v1/users/?search={test_user.full_name}",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
        # 验证搜索结果包含目标用户
        user_found = any(user["id"] == test_user.id for user in data["items"])
        assert user_found
    
    def test_get_users_unauthorized(self, client: TestClient, user_token_headers):
        """测试普通用户无权限获取用户列表"""
        response = client.get("/api/v1/users/", headers=user_token_headers)
        
        assert response.status_code == 403
    
    def test_get_user_by_id_success(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试根据ID获取用户成功"""
        response = client.get(f"/api/v1/users/{test_user.id}", headers=superuser_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
    
    def test_get_user_by_id_not_found(self, client: TestClient, superuser_token_headers):
        """测试获取不存在的用户"""
        response = client.get("/api/v1/users/99999", headers=superuser_token_headers)
        
        assert response.status_code == 404
        assert "用户不存在" in response.json()["detail"]
    
    def test_get_user_by_id_unauthorized(self, client: TestClient, user_token_headers, test_user: User):
        """测试普通用户无权限获取其他用户信息"""
        # 创建另一个用户
        other_user_id = test_user.id + 1000  # 假设的其他用户ID
        response = client.get(f"/api/v1/users/{other_user_id}", headers=user_token_headers)
        
        assert response.status_code == 403
    
    def test_create_user_success(self, client: TestClient, superuser_token_headers, test_department, test_position):
        """测试创建用户成功"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "phone": "13800138000",
            "department_id": test_department.id,
            "position_id": test_position.id,
            "role": "employee",
            "is_active": True,
            "is_superuser": False
        }
        response = client.post("/api/v1/users/", json=user_data, headers=superuser_token_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "id" in data
        assert "hashed_password" not in data  # 确保密码不返回
    
    def test_create_user_duplicate_email(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试创建用户时邮箱重复"""
        user_data = {
            "email": test_user.email,  # 重复邮箱
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "phone": "13800138000",
            "role": "employee"
        }
        response = client.post("/api/v1/users/", json=user_data, headers=superuser_token_headers)
        
        assert response.status_code == 400
        assert "邮箱已被注册" in response.json()["detail"]
    
    def test_create_user_unauthorized(self, client: TestClient, user_token_headers):
        """测试普通用户无权限创建用户"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "employee_id": "NEW001",
            "password": "newpassword123",
            "full_name": "新用户",
            "role": "employee"
        }
        response = client.post("/api/v1/users/", json=user_data, headers=user_token_headers)
        
        assert response.status_code == 403
    
    def test_update_user_success(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试更新用户成功"""
        update_data = {
            "full_name": "更新后的姓名",
            "phone": "13900139000",
            "is_active": False
        }
        response = client.put(
            f"/api/v1/users/{test_user.id}",
            json=update_data,
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone"] == update_data["phone"]
        assert data["is_active"] == update_data["is_active"]
    
    def test_update_user_not_found(self, client: TestClient, superuser_token_headers):
        """测试更新不存在的用户"""
        update_data = {"full_name": "更新后的姓名"}
        response = client.put(
            "/api/v1/users/99999",
            json=update_data,
            headers=superuser_token_headers
        )
        
        assert response.status_code == 404
        assert "用户不存在" in response.json()["detail"]
    
    def test_update_user_unauthorized(self, client: TestClient, user_token_headers, test_user: User):
        """测试普通用户无权限更新其他用户"""
        update_data = {"full_name": "更新后的姓名"}
        other_user_id = test_user.id + 1000  # 假设的其他用户ID
        response = client.put(
            f"/api/v1/users/{other_user_id}",
            json=update_data,
            headers=user_token_headers
        )
        
        assert response.status_code == 403
    
    def test_delete_user_success(self, client: TestClient, superuser_token_headers, db_session: Session, test_department, test_position):
        """测试删除用户成功"""
        # 创建一个用于删除的用户
        user_in = UserCreate(
            email="todelete@example.com",
            username="todelete",
            employee_id
            ="DEL001",
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
        
        response = client.delete(
            f"/api/v1/users/{user_to_delete.id}",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "用户删除成功"
        
        # 验证用户已被软删除
        db_session.refresh(user_to_delete)
        assert user_to_delete.is_deleted is True
    
    def test_delete_user_not_found(self, client: TestClient, superuser_token_headers):
        """测试删除不存在的用户"""
        response = client.delete("/api/v1/users/99999", headers=superuser_token_headers)
        
        assert response.status_code == 404
        assert "用户不存在" in response.json()["detail"]
    
    def test_delete_user_unauthorized(self, client: TestClient, user_token_headers, test_user: User):
        """测试普通用户无权限删除用户"""
        response = client.delete(f"/api/v1/users/{test_user.id}", headers=user_token_headers)
        
        assert response.status_code == 403
    
    def test_activate_user_success(self, client: TestClient, superuser_token_headers, db_session: Session, test_department, test_position):
        """测试激活用户成功"""
        # 创建一个非活跃用户
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
        
        response = client.post(
            f"/api/v1/users/{inactive_user.id}/activate",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "用户激活成功"
        
        # 验证用户已被激活
        db_session.refresh(inactive_user)
        assert inactive_user.is_active is True
    
    def test_deactivate_user_success(self, client: TestClient, superuser_token_headers, test_user: User, db_session: Session):
        """测试停用用户成功"""
        response = client.post(
            f"/api/v1/users/{test_user.id}/deactivate",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "用户停用成功"
        
        # 验证用户已被停用
        db_session.refresh(test_user)
        assert test_user.is_active is False
    
    def test_reset_user_password_success(self, client: TestClient, superuser_token_headers, test_user: User, db_session: Session):
        """测试管理员重置用户密码成功"""
        reset_data = {"new_password": "resetpassword123"}
        response = client.post(
            f"/api/v1/users/{test_user.id}/reset-password",
            json=reset_data,
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "密码重置成功"
        
        # 验证新密码
        from app.core.security import verify_password
        db_session.refresh(test_user)
        assert verify_password("resetpassword123", test_user.hashed_password)
    
    def test_get_user_statistics_success(self, client: TestClient, superuser_token_headers):
        """测试获取用户统计信息成功"""
        response = client.get("/api/v1/users/statistics", headers=superuser_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "active_users" in data
        assert "locked_users" in data
        assert "unverified_users" in data
        assert "new_users_30d" in data
        assert "active_users_7d" in data
        assert "inactive_users" in data
        
        # 验证数据类型
        for key in data:
            assert isinstance(data[key], int)
    
    def test_get_user_statistics_unauthorized(self, client: TestClient, user_token_headers):
        """测试普通用户无权限获取用户统计信息"""
        response = client.get("/api/v1/users/statistics", headers=user_token_headers)
        
        assert response.status_code == 403
    
    def test_get_user_activity_success(self, client: TestClient, superuser_token_headers, test_user: User):
        """测试获取用户活动记录成功"""
        response = client.get(
            f"/api/v1/users/{test_user.id}/activity",
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    def test_get_user_activity_unauthorized(self, client: TestClient, user_token_headers, test_user: User):
        """测试普通用户无权限获取其他用户活动记录"""
        other_user_id = test_user.id + 1000  # 假设的其他用户ID
        response = client.get(
            f"/api/v1/users/{other_user_id}/activity",
            headers=user_token_headers
        )
        
        assert response.status_code == 403
    
    def test_bulk_operations_success(self, client: TestClient, superuser_token_headers, db_session: Session, test_department, test_position):
        """测试批量操作成功"""
        # 创建多个测试用户
        test_users = []
        for i in range(3):
            user_in = UserCreate(
                email=f"bulk{i}@example.com",
                username=f"bulk{i}",
                employee_id=f"BULK00{i}",
                password="password123",
                full_name=f"批量用户{i}",
                phone=f"1380013800{i}",
                department_id=test_department.id,
                position_id=test_position.id,
                role="employee",
                is_active=True,
                is_superuser=False
            )
            user = crud_user.create(db_session, obj_in=user_in)
            test_users.append(user)
        
        # 测试批量停用
        user_ids = [user.id for user in test_users]
        bulk_data = {"user_ids": user_ids, "action": "deactivate"}
        response = client.post(
            "/api/v1/users/bulk-action",
            json=bulk_data,
            headers=superuser_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success_count"] == 3
        assert data["failed_count"] == 0
        
        # 验证用户已被停用
        for user in test_users:
            db_session.refresh(user)
            assert user.is_active is False