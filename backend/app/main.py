"""FastAPI应用程序主文件

本文件是人力资源调度系统后端API的入口点，配置了应用程序的基础设置、中间件和路由。
"""

import time
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.database import database_manager
from app.core.security import SecurityManager
from app.api import api_router
from app.schemas.base import ErrorResponse

# 获取配置
settings = get_settings()

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log") if settings.LOG_TO_FILE else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"Request: {request.method} {request.url} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序生命周期管理"""
    # 启动时执行
    logger.info("Starting up Human Resource Scheduling System...")
    
    try:
        # 初始化数据库
        await database_manager.initialize()
        logger.info("Database initialized successfully")
        
        # 创建数据库表
        await database_manager.create_tables()
        logger.info("Database tables created successfully")
        
        # 初始化安全管理器
        security_manager = SecurityManager()
        logger.info("Security manager initialized")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    finally:
        # 关闭时执行
        logger.info("Shutting down Human Resource Scheduling System...")
        
        try:
            # 清理数据库连接
            await database_manager.cleanup()
            logger.info("Database connections cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="人力资源调度系统后端API",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=f"{settings.API_V1_STR}/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
    debug=settings.DEBUG
)

# 配置CORS中间件
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time", "X-Request-ID"]
    )

# 配置受信任主机中间件
if settings.ALLOWED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# 配置Gzip压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 添加自定义中间件
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)


# 全局异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail} - "
        f"Path: {request.url.path} - Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            request_id=getattr(request.state, "request_id", None)
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """请求验证异常处理器"""
    logger.warning(
        f"Validation Error: {exc.errors()} - "
        f"Path: {request.url.path} - Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            message="请求参数验证失败",
            error_code="VALIDATION_ERROR",
            error_details={
                "errors": exc.errors(),
                "body": exc.body
            },
            request_id=getattr(request.state, "request_id", None)
        ).model_dump()
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Starlette HTTP异常处理器"""
    logger.error(
        f"Starlette Exception: {exc.status_code} - {exc.detail} - "
        f"Path: {request.url.path} - Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message=str(exc.detail),
            error_code=f"STARLETTE_{exc.status_code}",
            request_id=getattr(request.state, "request_id", None)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(
        f"Unexpected Error: {type(exc).__name__}: {str(exc)} - "
        f"Path: {request.url.path} - Method: {request.method}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            message="服务器内部错误" if settings.ENVIRONMENT == "production" else str(exc),
            error_code="INTERNAL_SERVER_ERROR",
            error_details=None if settings.ENVIRONMENT == "production" else {
                "type": type(exc).__name__,
                "details": str(exc)
            },
            request_id=getattr(request.state, "request_id", None)
        ).model_dump()
    )


# 健康检查端点
@app.get("/health", tags=["健康检查"])
async def health_check() -> Dict[str, Any]:
    """健康检查端点"""
    try:
        # 检查数据库连接
        db_status = await database_manager.health_check()
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "database": "connected" if db_status else "disconnected",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )


# 根路径重定向
@app.get("/", include_in_schema=False)
async def root():
    """根路径重定向到API文档"""
    return {
        "message": "Human Resource Scheduling System API",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "redoc_url": f"{settings.API_V1_STR}/redoc"
    }


# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    
    # 开发环境运行配置
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )