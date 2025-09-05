import logging
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.models.department import Department
from app.models.position import Position
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate
from app.core.config import settings
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """初始化数据库数据"""
    try:
        # 检查是否已经有超级用户
        superuser = crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not superuser:
            # 创建默认超级用户
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER_USERNAME,
                employee_id="ADMIN001",
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name="系统管理员",
                phone="",
                department_id=None,
                position_id=None,
                role="admin",
                is_active=True,
                is_superuser=True
            )
            superuser = crud_user.create(db, obj_in=user_in)
            logger.info(f"Superuser created: {superuser.email}")
        else:
            logger.info(f"Superuser already exists: {superuser.email}")
        
        # 创建默认部门
        create_default_departments(db)
        
        # 创建默认职位
        create_default_positions(db)
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def create_default_departments(db: Session) -> None:
    """创建默认部门"""
    default_departments = [
        {
            "name": "人力资源部",
            "code": "HR",
            "description": "负责人力资源管理、招聘、培训等工作",
            "parent_id": None,
            "manager_id": None,
            "is_active": True
        },
        {
            "name": "技术部",
            "code": "TECH",
            "description": "负责技术开发、系统维护等工作",
            "parent_id": None,
            "manager_id": None,
            "is_active": True
        },
        {
            "name": "财务部",
            "code": "FINANCE",
            "description": "负责财务管理、会计核算等工作",
            "parent_id": None,
            "manager_id": None,
            "is_active": True
        },
        {
            "name": "市场部",
            "code": "MARKETING",
            "description": "负责市场推广、销售支持等工作",
            "parent_id": None,
            "manager_id": None,
            "is_active": True
        },
        {
            "name": "运营部",
            "code": "OPERATIONS",
            "description": "负责日常运营、流程管理等工作",
            "parent_id": None,
            "manager_id": None,
            "is_active": True
        }
    ]
    
    for dept_data in default_departments:
        existing_dept = db.query(Department).filter(
            Department.code == dept_data["code"]
        ).first()
        
        if not existing_dept:
            department = Department(
                name=dept_data["name"],
                code=dept_data["code"],
                description=dept_data["description"],
                parent_id=dept_data["parent_id"],
                manager_id=dept_data["manager_id"],
                is_active=dept_data["is_active"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(department)
            logger.info(f"Created department: {dept_data['name']}")
    
    db.commit()


def create_default_positions(db: Session) -> None:
    """创建默认职位"""
    default_positions = [
        {
            "name": "总经理",
            "code": "GM",
            "description": "公司总经理",
            "level": 1,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "部门经理",
            "code": "DEPT_MGR",
            "description": "部门经理",
            "level": 2,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "项目经理",
            "code": "PROJ_MGR",
            "description": "项目经理",
            "level": 3,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "高级工程师",
            "code": "SR_ENG",
            "description": "高级工程师",
            "level": 4,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "工程师",
            "code": "ENG",
            "description": "工程师",
            "level": 5,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "初级工程师",
            "code": "JR_ENG",
            "description": "初级工程师",
            "level": 6,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "专员",
            "code": "SPECIALIST",
            "description": "专员",
            "level": 7,
            "department_id": None,
            "is_active": True
        },
        {
            "name": "助理",
            "code": "ASSISTANT",
            "description": "助理",
            "level": 8,
            "department_id": None,
            "is_active": True
        }
    ]
    
    for pos_data in default_positions:
        existing_pos = db.query(Position).filter(
            Position.code == pos_data["code"]
        ).first()
        
        if not existing_pos:
            position = Position(
                name=pos_data["name"],
                code=pos_data["code"],
                description=pos_data["description"],
                level=pos_data["level"],
                department_id=pos_data["department_id"],
                is_active=pos_data["is_active"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(position)
            logger.info(f"Created position: {pos_data['name']}")
    
    db.commit()


def create_test_data(db: Session) -> None:
    """创建测试数据（仅用于开发环境）"""
    if not settings.ENVIRONMENT == "development":
        return
    
    try:
        # 获取部门和职位
        hr_dept = db.query(Department).filter(Department.code == "HR").first()
        tech_dept = db.query(Department).filter(Department.code == "TECH").first()
        
        manager_pos = db.query(Position).filter(Position.code == "DEPT_MGR").first()
        engineer_pos = db.query(Position).filter(Position.code == "ENG").first()
        
        # 创建测试用户
        test_users = [
            {
                "email": "hr.manager@company.com",
                "username": "hr_manager",
                "employee_id": "HR001",
                "password": "password123",
                "full_name": "张三",
                "phone": "13800138001",
                "department_id": hr_dept.id if hr_dept else None,
                "position_id": manager_pos.id if manager_pos else None,
                "role": "manager",
                "is_active": True,
                "is_superuser": False
            },
            {
                "email": "tech.lead@company.com",
                "username": "tech_lead",
                "employee_id": "TECH001",
                "password": "password123",
                "full_name": "李四",
                "phone": "13800138002",
                "department_id": tech_dept.id if tech_dept else None,
                "position_id": manager_pos.id if manager_pos else None,
                "role": "manager",
                "is_active": True,
                "is_superuser": False
            },
            {
                "email": "developer@company.com",
                "username": "developer",
                "employee_id": "TECH002",
                "password": "password123",
                "full_name": "王五",
                "phone": "13800138003",
                "department_id": tech_dept.id if tech_dept else None,
                "position_id": engineer_pos.id if engineer_pos else None,
                "role": "employee",
                "is_active": True,
                "is_superuser": False
            }
        ]
        
        for user_data in test_users:
            existing_user = crud_user.get_by_email(db, email=user_data["email"])
            if not existing_user:
                user_in = UserCreate(**user_data)
                test_user = crud_user.create(db, obj_in=user_in)
                logger.info(f"Created test user: {test_user.email}")
        
        logger.info("Test data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating test data: {e}")
        raise


def main() -> None:
    """主函数"""
    logger.info("Initializing database...")
    db = SessionLocal()
    try:
        init_db(db)
        if settings.ENVIRONMENT == "development":
            create_test_data(db)
    finally:
        db.close()
    logger.info("Database initialization completed")


if __name__ == "__main__":
    main()