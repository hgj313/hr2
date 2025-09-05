from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# 数据库引擎配置
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=20,
    max_overflow=30,
    echo=settings.DEBUG,
)

# 测试数据库引擎（如果配置了测试数据库URL）
test_engine = None
if settings.DATABASE_TEST_URL:
    test_engine = create_engine(
        settings.DATABASE_TEST_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG,
    )

# 会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 测试会话工厂
TestSessionLocal = None
if test_engine:
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

# 数据库元数据
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

# 声明性基类
Base = declarative_base(metadata=metadata)


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话的依赖注入函数"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_test_db() -> Generator[Session, None, None]:
    """获取测试数据库会话的依赖注入函数"""
    if not TestSessionLocal:
        raise RuntimeError("Test database not configured")
    
    db = TestSessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Test database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """数据库管理器类"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_tables(self):
        """创建所有数据库表"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self):
        """删除所有数据库表"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    def health_check(self) -> bool:
        """数据库健康检查"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def get_connection_info(self) -> dict:
        """获取数据库连接信息"""
        return {
            "url": str(self.engine.url).replace(self.engine.url.password or "", "***"),
            "pool_size": self.engine.pool.size(),
            "checked_in": self.engine.pool.checkedin(),
            "checked_out": self.engine.pool.checkedout(),
            "overflow": self.engine.pool.overflow(),
        }


# 全局数据库管理器实例
db_manager = DatabaseManager()


# 数据库事务装饰器
from functools import wraps
from typing import Callable, Any


def transactional(func: Callable) -> Callable:
    """数据库事务装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        db = db_manager.get_session()
        try:
            result = func(db, *args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Transaction failed in {func.__name__}: {e}")
            raise
        finally:
            db.close()
    return wrapper


# 数据库连接池监控
def get_pool_status() -> dict:
    """获取连接池状态"""
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid(),
    }


# 数据库初始化函数
def init_db():
    """初始化数据库"""
    try:
        # 创建所有表
        db_manager.create_tables()
        
        # 执行健康检查
        if not db_manager.health_check():
            raise RuntimeError("Database health check failed after initialization")
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


# 数据库清理函数
def cleanup_db():
    """清理数据库连接"""
    try:
        engine.dispose()
        if test_engine:
            test_engine.dispose()
        logger.info("Database connections cleaned up")
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")