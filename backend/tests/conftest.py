import pytest
import asyncio
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import tempfile
import os

from app.main import app
from app.db.session import get_db, Base
from app.core.config import settings
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate
from app.core.security import create_access_token
from app.models.user import User
from app.models.department import Department
from app.models.position import Position


# 创建测试数据库
@pytest.fixture(scope="session")
def test_db_file():
    """创建临时测试数据库文件"""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    yield db_path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="session")
def test_engine(test_db_file):
    """创建测试数据库引擎"""
    engine = create_engine(
        f"sqlite:///{test_db_file}",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """创建测试会话工厂"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session(TestingSessionLocal) -> Generator[Session, None, None]:
    """创建测试数据库会话"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_department(db_session) -> Department:
    """创建测试部门"""
    department = Department(
        name="测试部门",
        code="TEST_DEPT",
        description="测试用部门",
        is_active=True
    )
    db_session.add(department)
    db_session.commit()
    db_session.refresh(department)
    return department


@pytest.fixture
def test_position(db_session, test_department) -> Position:
    """创建测试职位"""
    position = Position(
        name="测试职位",
        code="TEST_POS",
        description="测试用职位",
        level=5,
        department_id=test_department.id,
        is_active=True
    )
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)
    return position


@pytest.fixture
def test_user(db_session, test_department, test_position) -> User:
    """创建测试用户"""
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
    return crud_user.create(db_session, obj_in=user_in)


@pytest.fixture
def test_superuser(db_session, test_department, test_position) -> User:
    """创建测试超级用户"""
    user_in = UserCreate(
        email="admin@example.com",
        username="admin",
        employee_id="ADMIN001",
        password="adminpassword123",
        full_name="管理员",
        phone="13800138001",
        department_id=test_department.id,
        position_id=test_position.id,
        role="admin",
        is_active=True,
        is_superuser=True
    )
    return crud_user.create(db_session, obj_in=user_in)


@pytest.fixture
def test_manager(db_session, test_department, test_position) -> User:
    """创建测试管理员"""
    user_in = UserCreate(
        email="manager@example.com",
        username="manager",
        employee_id="MGR001",
        password="managerpassword123",
        full_name="部门经理",
        phone="13800138002",
        department_id=test_department.id,
        position_id=test_position.id,
        role="manager",
        is_active=True,
        is_superuser=False
    )
    return crud_user.create(db_session, obj_in=user_in)


@pytest.fixture
def user_token_headers(test_user) -> Dict[str, str]:
    """创建普通用户认证头"""
    access_token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def superuser_token_headers(test_superuser) -> Dict[str, str]:
    """创建超级用户认证头"""
    access_token = create_access_token(subject=test_superuser.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def manager_token_headers(test_manager) -> Dict[str, str]:
    """创建管理员认证头"""
    access_token = create_access_token(subject=test_manager.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """测试用户数据"""
    return {
        "email": "newuser@example.com",
        "username": "newuser",
        "employee_id": "NEW001",
        "password": "newpassword123",
        "full_name": "新用户",
        "phone": "13800138003",
        "role": "employee",
        "is_active": True,
        "is_superuser": False
    }


@pytest.fixture
def test_department_data() -> Dict[str, Any]:
    """测试部门数据"""
    return {
        "name": "新部门",
        "code": "NEW_DEPT",
        "description": "新创建的部门",
        "is_active": True
    }


@pytest.fixture
def test_position_data() -> Dict[str, Any]:
    """测试职位数据"""
    return {
        "name": "新职位",
        "code": "NEW_POS",
        "description": "新创建的职位",
        "level": 6,
        "is_active": True
    }


# 异步测试支持
@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# 测试配置
@pytest.fixture(autouse=True)
def test_settings():
    """设置测试环境配置"""
    original_env = settings.ENVIRONMENT
    original_testing = settings.TESTING
    
    settings.ENVIRONMENT = "testing"
    settings.TESTING = True
    
    yield
    
    settings.ENVIRONMENT = original_env
    settings.TESTING = original_testing


# 清理数据库
@pytest.fixture(autouse=True)
def cleanup_db(db_session):
    """每个测试后清理数据库"""
    yield
    # 清理所有表数据
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


# Mock外部服务
@pytest.fixture
def mock_email_service(monkeypatch):
    """模拟邮件服务"""
    def mock_send_email(*args, **kwargs):
        return True
    
    monkeypatch.setattr("app.utils.email.send_email", mock_send_email)
    monkeypatch.setattr("app.utils.email.send_template_email", mock_send_email)


@pytest.fixture
def mock_redis_service(monkeypatch):
    """模拟Redis服务"""
    class MockRedis:
        def __init__(self):
            self.data = {}
        
        def get(self, key):
            return self.data.get(key)
        
        def set(self, key, value, ex=None):
            self.data[key] = value
            return True
        
        def delete(self, key):
            return self.data.pop(key, None) is not None
        
        def exists(self, key):
            return key in self.data
        
        def incr(self, key):
            self.data[key] = self.data.get(key, 0) + 1
            return self.data[key]
        
        def expire(self, key, seconds):
            return True
    
    mock_redis = MockRedis()
    monkeypatch.setattr("app.core.cache.redis_client", mock_redis)
    return mock_redis


# 性能测试标记
pytest_plugins = ["pytest_benchmark"]


# 测试标记
def pytest_configure(config):
    """配置pytest标记"""
    config.addinivalue_line(
        "markers", "unit: 单元测试"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试"
    )
    config.addinivalue_line(
        "markers", "api: API测试"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试"
    )
    config.addinivalue_line(
        "markers", "security: 安全测试"
    )
    config.addinivalue_line(
        "markers", "performance: 性能测试"
    )