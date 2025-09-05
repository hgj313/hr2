from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# 创建数据库引擎
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite配置
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 20,
        },
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
    )
else:
    # PostgreSQL/MySQL配置
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_recycle=settings.DB_POOL_RECYCLE,
        pool_pre_ping=True,
        echo=settings.DATABASE_ECHO,
    )

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# 创建基类
Base = declarative_base()


def get_db() -> Generator:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_db_and_tables():
    """创建数据库和表"""
    try:
        # 导入所有模型以确保它们被注册
        from app.models import user, department, position, project, task, approval, risk, notification
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_db_and_tables():
    """删除数据库和表（仅用于开发/测试）"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def check_db_connection() -> bool:
    """检查数据库连接"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def get_db_info() -> dict:
    """获取数据库信息"""
    try:
        with engine.connect() as connection:
            if settings.DATABASE_URL.startswith("sqlite"):
                result = connection.execute("SELECT sqlite_version()")
                version = result.fetchone()[0]
                return {
                    "type": "SQLite",
                    "version": version,
                    "url": settings.DATABASE_URL
                }
            elif "postgresql" in settings.DATABASE_URL:
                result = connection.execute("SELECT version()")
                version = result.fetchone()[0]
                return {
                    "type": "PostgreSQL",
                    "version": version,
                    "url": settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL
                }
            elif "mysql" in settings.DATABASE_URL:
                result = connection.execute("SELECT VERSION()")
                version = result.fetchone()[0]
                return {
                    "type": "MySQL",
                    "version": version,
                    "url": settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL
                }
            else:
                return {
                    "type": "Unknown",
                    "version": "Unknown",
                    "url": settings.DATABASE_URL
                }
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        return {
            "type": "Error",
            "version": str(e),
            "url": settings.DATABASE_URL
        }