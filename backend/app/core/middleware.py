import time
import uuid
import logging
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
import redis
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import verify_token, TokenType
from app.models.auth import User


# 配置日志
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"Request started - ID: {request_id}, "
            f"Method: {request.method}, "
            f"URL: {request.url}, "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录响应信息
            logger.info(
                f"Request completed - ID: {request_id}, "
                f"Status: {response.status_code}, "
                f"Time: {process_time:.4f}s"
            )
            
            # 添加响应头
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录错误信息
            logger.error(
                f"Request failed - ID: {request_id}, "
                f"Error: {str(e)}, "
                f"Time: {process_time:.4f}s"
            )
            
            # 重新抛出异常
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # 在生产环境中添加HSTS头
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # 内容安全策略
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """速率限制中间件"""
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.redis_client = None
        
        # 尝试连接Redis
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()
        except Exception as e:
            logger.warning(f"Redis connection failed, rate limiting disabled: {e}")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.redis_client:
            return await call_next(request)
        
        # 获取客户端标识
        client_id = self._get_client_id(request)
        
        # 检查速率限制
        if not await self._check_rate_limit(client_id):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded"}
            )
        
        return await call_next(request)
    
    def _get_client_id(self, request: Request) -> str:
        """获取客户端标识"""
        # 优先使用用户ID（如果已认证）
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                token = auth_header.split(" ")[1]
                payload = verify_token(token, TokenType.ACCESS)
                if payload:
                    user_id = payload.get("sub")
                    if user_id:
                        return f"user:{user_id}"
            except Exception:
                pass
        
        # 使用IP地址
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    async def _check_rate_limit(self, client_id: str) -> bool:
        """检查速率限制"""
        try:
            key = f"rate_limit:{client_id}"
            current = self.redis_client.get(key)
            
            if current is None:
                # 首次请求
                self.redis_client.setex(key, self.period, 1)
                return True
            
            current_count = int(current)
            if current_count >= self.calls:
                return False
            
            # 增加计数
            self.redis_client.incr(key)
            return True
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # 出错时允许请求


class DatabaseMiddleware(BaseHTTPMiddleware):
    """数据库中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 为请求创建数据库会话
        db = SessionLocal()
        request.state.db = db
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # 回滚事务
            db.rollback()
            raise
        finally:
            # 关闭数据库会话
            db.close()


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """错误处理中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except HTTPException:
            # FastAPI的HTTP异常直接传递
            raise
        except Exception as e:
            # 记录未处理的异常
            request_id = getattr(request.state, 'request_id', 'unknown')
            logger.error(
                f"Unhandled exception - Request ID: {request_id}, "
                f"Error: {str(e)}", 
                exc_info=True
            )
            
            # 返回通用错误响应
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id
                }
            )


class MaintenanceMiddleware(BaseHTTPMiddleware):
    """维护模式中间件"""
    
    def __init__(self, app, maintenance_mode: bool = False):
        super().__init__(app)
        self.maintenance_mode = maintenance_mode
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if self.maintenance_mode:
            # 允许健康检查端点
            if request.url.path in ["/health", "/health/"]:
                return await call_next(request)
            
            # 返回维护模式响应
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "detail": "Service temporarily unavailable for maintenance",
                    "retry_after": 3600  # 1小时后重试
                }
            )
        
        return await call_next(request)


class UserActivityMiddleware(BaseHTTPMiddleware):
    """用户活动跟踪中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 获取用户信息
        user = await self._get_current_user(request)
        
        if user:
            # 更新用户最后活动时间
            await self._update_user_activity(user)
        
        return await call_next(request)
    
    async def _get_current_user(self, request: Request) -> Optional[User]:
        """从请求中获取当前用户"""
        try:
            auth_header = request.headers.get("authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.split(" ")[1]
            payload = verify_token(token, TokenType.ACCESS)
            if not payload:
                return None
            
            user_id = payload.get("sub")
            if not user_id:
                return None
            
            # 从数据库获取用户
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                return user
            finally:
                db.close()
                
        except Exception:
            return None
    
    async def _update_user_activity(self, user: User):
        """更新用户活动时间"""
        try:
            db = SessionLocal()
            try:
                # 更新最后活动时间
                user.last_activity = time.time()
                db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Failed to update user activity: {e}")


def setup_middleware(app):
    """设置应用中间件"""
    
    # 错误处理中间件（最外层）
    app.add_middleware(ErrorHandlingMiddleware)
    
    # 维护模式中间件
    app.add_middleware(
        MaintenanceMiddleware,
        maintenance_mode=settings.MAINTENANCE_MODE
    )
    
    # 请求日志中间件
    app.add_middleware(RequestLoggingMiddleware)
    
    # 安全头中间件
    app.add_middleware(SecurityHeadersMiddleware)
    
    # 速率限制中间件
    if settings.ENABLE_RATE_LIMITING:
        app.add_middleware(
            RateLimitMiddleware,
            calls=settings.RATE_LIMIT_CALLS,
            period=settings.RATE_LIMIT_PERIOD
        )
    
    # 用户活动跟踪中间件
    app.add_middleware(UserActivityMiddleware)
    
    # GZIP压缩中间件
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 会话中间件
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        max_age=settings.SESSION_MAX_AGE
    )
    
    # CORS中间件
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # 受信任主机中间件
    if settings.ALLOWED_HOSTS:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )


# 中间件配置类
class MiddlewareConfig:
    """中间件配置类"""
    
    def __init__(self):
        self.request_logging = True
        self.security_headers = True
        self.rate_limiting = settings.ENABLE_RATE_LIMITING
        self.user_activity_tracking = True
        self.error_handling = True
        self.maintenance_mode = settings.MAINTENANCE_MODE
        self.gzip_compression = True
        self.cors_enabled = bool(settings.BACKEND_CORS_ORIGINS)
        self.trusted_hosts = bool(settings.ALLOWED_HOSTS)
    
    def apply_to_app(self, app):
        """将中间件配置应用到应用"""
        if self.error_handling:
            app.add_middleware(ErrorHandlingMiddleware)
        
        if self.maintenance_mode:
            app.add_middleware(
                MaintenanceMiddleware,
                maintenance_mode=True
            )
        
        if self.request_logging:
            app.add_middleware(RequestLoggingMiddleware)
        
        if self.security_headers:
            app.add_middleware(SecurityHeadersMiddleware)
        
        if self.rate_limiting:
            app.add_middleware(
                RateLimitMiddleware,
                calls=settings.RATE_LIMIT_CALLS,
                period=settings.RATE_LIMIT_PERIOD
            )
        
        if self.user_activity_tracking:
            app.add_middleware(UserActivityMiddleware)
        
        if self.gzip_compression:
            app.add_middleware(GZipMiddleware, minimum_size=1000)
        
        app.add_middleware(
            SessionMiddleware,
            secret_key=settings.SECRET_KEY,
            max_age=settings.SESSION_MAX_AGE
        )
        
        if self.cors_enabled:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        
        if self.trusted_hosts:
            app.add_middleware(
                TrustedHostMiddleware,
                allowed_hosts=settings.ALLOWED_HOSTS
            )