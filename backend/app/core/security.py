from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from passlib.hash import bcrypt
import secrets
import hashlib
import hmac
from enum import Enum

from app.core.config import settings


class TokenType(str, Enum):
    """令牌类型枚举"""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"


class SecurityManager:
    """安全管理器类"""
    
    def __init__(self):
        # 密码上下文配置
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12
        )
        
        # JWT配置
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_password_hash(self, password: str) -> str:
        """创建密码哈希"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def generate_salt(self, length: int = 32) -> str:
        """生成随机盐值"""
        return secrets.token_hex(length)
    
    def create_access_token(
        self, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[dict] = None
    ) -> str:
        """创建访问令牌"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": TokenType.ACCESS,
            "iat": datetime.utcnow(),
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def create_refresh_token(
        self, 
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建刷新令牌"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=self.refresh_token_expire_days
            )
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": TokenType.REFRESH,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def create_reset_password_token(self, email: str) -> str:
        """创建重置密码令牌"""
        expire = datetime.utcnow() + timedelta(hours=1)  # 1小时有效期
        
        to_encode = {
            "exp": expire,
            "sub": email,
            "type": TokenType.RESET_PASSWORD,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def create_email_verification_token(self, email: str) -> str:
        """创建邮箱验证令牌"""
        expire = datetime.utcnow() + timedelta(days=1)  # 1天有效期
        
        to_encode = {
            "exp": expire,
            "sub": email,
            "type": TokenType.EMAIL_VERIFICATION,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def verify_token(
        self, 
        token: str, 
        expected_type: Optional[TokenType] = None
    ) -> Optional[dict]:
        """验证令牌"""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # 检查令牌类型
            if expected_type and payload.get("type") != expected_type:
                return None
            
            # 检查过期时间
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None
            
            return payload
            
        except JWTError:
            return None
    
    def get_token_subject(self, token: str) -> Optional[str]:
        """获取令牌主题"""
        payload = self.verify_token(token)
        if payload:
            return payload.get("sub")
        return None
    
    def is_token_expired(self, token: str) -> bool:
        """检查令牌是否过期"""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={"verify_exp": False}  # 不验证过期时间
            )
            
            exp = payload.get("exp")
            if exp:
                return datetime.fromtimestamp(exp) < datetime.utcnow()
            return True
            
        except JWTError:
            return True
    
    def generate_api_key(self, user_id: str, length: int = 32) -> str:
        """生成API密钥"""
        # 使用用户ID和当前时间戳生成唯一的API密钥
        timestamp = str(int(datetime.utcnow().timestamp()))
        data = f"{user_id}:{timestamp}:{secrets.token_hex(16)}"
        
        # 使用HMAC生成安全的API密钥
        api_key = hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()[:length]
        
        return api_key
    
    def verify_api_key(self, api_key: str, user_id: str) -> bool:
        """验证API密钥"""
        # 这里应该从数据库中获取存储的API密钥进行比较
        # 实际实现中需要结合数据库操作
        return True  # 占位符实现
    
    def create_secure_hash(self, data: str, salt: Optional[str] = None) -> tuple[str, str]:
        """创建安全哈希"""
        if not salt:
            salt = self.generate_salt()
        
        # 使用PBKDF2进行哈希
        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            data.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 迭代次数
        ).hex()
        
        return hash_value, salt
    
    def verify_secure_hash(self, data: str, hash_value: str, salt: str) -> bool:
        """验证安全哈希"""
        computed_hash, _ = self.create_secure_hash(data, salt)
        return hmac.compare_digest(computed_hash, hash_value)
    
    def validate_password_strength(self, password: str) -> dict:
        """验证密码强度"""
        result = {
            "is_valid": True,
            "errors": [],
            "score": 0
        }
        
        # 长度检查
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            result["is_valid"] = False
            result["errors"].append(
                f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
            )
        else:
            result["score"] += 1
        
        # 包含大写字母
        if any(c.isupper() for c in password):
            result["score"] += 1
        else:
            result["errors"].append("Password must contain at least one uppercase letter")
        
        # 包含小写字母
        if any(c.islower() for c in password):
            result["score"] += 1
        else:
            result["errors"].append("Password must contain at least one lowercase letter")
        
        # 包含数字
        if any(c.isdigit() for c in password):
            result["score"] += 1
        else:
            result["errors"].append("Password must contain at least one digit")
        
        # 包含特殊字符
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            result["score"] += 1
        else:
            result["errors"].append("Password must contain at least one special character")
        
        # 如果有错误，则密码无效
        if result["errors"]:
            result["is_valid"] = False
        
        return result
    
    def generate_csrf_token(self, session_id: str) -> str:
        """生成CSRF令牌"""
        timestamp = str(int(datetime.utcnow().timestamp()))
        data = f"{session_id}:{timestamp}"
        
        csrf_token = hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return csrf_token
    
    def verify_csrf_token(self, token: str, session_id: str, max_age: int = 3600) -> bool:
        """验证CSRF令牌"""
        try:
            # 从令牌中提取时间戳（这需要在生成时包含时间戳信息）
            # 这里是简化实现，实际应用中需要更复杂的验证逻辑
            current_time = int(datetime.utcnow().timestamp())
            expected_token = self.generate_csrf_token(session_id)
            
            return hmac.compare_digest(token, expected_token)
            
        except Exception:
            return False


# 全局安全管理器实例
security_manager = SecurityManager()


# 便捷函数
def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌的便捷函数"""
    return security_manager.create_access_token(subject, expires_delta)


def create_refresh_token(subject: Union[str, Any]) -> str:
    """创建刷新令牌的便捷函数"""
    return security_manager.create_refresh_token(subject)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码的便捷函数"""
    return security_manager.verify_password(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希的便捷函数"""
    return security_manager.create_password_hash(password)


def verify_token(token: str, expected_type: Optional[TokenType] = None) -> Optional[dict]:
    """验证令牌的便捷函数"""
    return security_manager.verify_token(token, expected_type)