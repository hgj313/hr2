from typing import List, Optional, Union
from pydantic import BaseSettings, validator, AnyHttpUrl
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    """应用程序配置设置"""
    
    # 应用程序基础配置
    APP_NAME: str = "HR Scheduling System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Human Resource Scheduling and Management System"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # JWT配置
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS配置
    CORS_ORIGINS: List[AnyHttpUrl] = []
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # 安全配置
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 30
    
    # 令牌配置
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    API_KEY_EXPIRE_DAYS: int = 365
    
    # 会话配置
    SESSION_TIMEOUT_MINUTES: int = 60
    REMEMBER_ME_DAYS: int = 30
    
    # 安全头配置
    SECURITY_HEADERS_ENABLED: bool = True
    HSTS_MAX_AGE: int = 31536000  # 1 year
    CONTENT_SECURITY_POLICY: str = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    # CSRF配置
    CSRF_PROTECTION_ENABLED: bool = True
    CSRF_TOKEN_EXPIRE_MINUTES: int = 60
    
    # IP白名单配置
    IP_WHITELIST_ENABLED: bool = False
    IP_WHITELIST: List[str] = []
    
    # 审计日志配置
    AUDIT_LOG_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 90
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # 邮件配置
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    EMAIL_FROM: Optional[str] = None
    
    # 文件上传配置
    UPLOAD_MAX_SIZE: int = 10485760  # 10MB
    UPLOAD_ALLOWED_EXTENSIONS: List[str] = [
        "jpg", "jpeg", "png", "pdf", "doc", "docx", "xls", "xlsx"
    ]
    UPLOAD_PATH: str = "./uploads"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    LOG_MAX_SIZE: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # 监控配置
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 8001
    HEALTH_CHECK_ENABLED: bool = True
    HEALTH_CHECK_PATH: str = "/health"
    
    # 中间件配置
    REQUEST_LOGGING_ENABLED: bool = True
    REQUEST_ID_HEADER: str = "X-Request-ID"
    CORRELATION_ID_HEADER: str = "X-Correlation-ID"
    
    # 维护模式配置
    MAINTENANCE_MODE: bool = False
    MAINTENANCE_MESSAGE: str = "System is under maintenance. Please try again later."
    
    # 用户活动跟踪配置
    USER_ACTIVITY_TRACKING_ENABLED: bool = True
    USER_ACTIVITY_RETENTION_DAYS: int = 30
    
    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # 缓存配置
    CACHE_ENABLED: bool = True
    CACHE_DEFAULT_TTL: int = 300  # 5 minutes
    
    # 备份配置
    BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    BACKUP_RETENTION_DAYS: int = 30
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL")
        return v
    
    @validator("SECRET_KEY", pre=True)
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("PASSWORD_MIN_LENGTH")
    def validate_password_min_length(cls, v: int) -> int:
        if v < 6:
            raise ValueError("PASSWORD_MIN_LENGTH must be at least 6")
        return v
    
    @validator("DEFAULT_PAGE_SIZE")
    def validate_default_page_size(cls, v: int) -> int:
        if v < 1 or v > 100:
            raise ValueError("DEFAULT_PAGE_SIZE must be between 1 and 100")
        return v
    
    @validator("MAX_PAGE_SIZE")
    def validate_max_page_size(cls, v: int) -> int:
        if v < 1 or v > 1000:
            raise ValueError("MAX_PAGE_SIZE must be between 1 and 1000")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取应用程序设置的单例实例"""
    return Settings()


# 全局设置实例
settings = get_settings()