"""认证相关Pydantic模式定义

本模块定义了用户认证、角色权限等相关的API请求和响应模式。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator
from app.schemas.base import BaseSchema, TimestampMixin


# ============================================================================
# 用户相关模式
# ============================================================================

class UserBase(BaseSchema):
    """用户基础模式"""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9_-]+$",
        description="用户名",
        example="zhangsan"
    )
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        example="zhangsan@example.com"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="真实姓名",
        example="张三"
    )
    phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="手机号码",
        example="13800138000"
    )
    avatar: Optional[str] = Field(
        None,
        description="头像URL",
        example="/uploads/avatars/user_123.jpg"
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class UserCreate(UserBase):
    """用户创建模式"""
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="密码",
        example="password123"
    )
    confirm_password: str = Field(
        ...,
        description="确认密码",
        example="password123"
    )
    role_ids: Optional[List[int]] = Field(
        None,
        description="角色ID列表",
        example=[1, 2]
    )
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('密码不匹配')
        return v


class UserRegister(BaseSchema):
    """用户注册模式"""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9_-]+$",
        description="用户名",
        example="zhangsan"
    )
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        example="zhangsan@example.com"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="真实姓名",
        example="张三"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="密码",
        example="password123"
    )
    confirm_password: str = Field(
        ...,
        description="确认密码",
        example="password123"
    )
    phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="手机号码",
        example="13800138000"
    )
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('密码不匹配')
        return v


class UserUpdate(BaseSchema):
    """用户更新模式"""
    email: Optional[EmailStr] = Field(
        None,
        description="邮箱地址",
        example="zhangsan@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="真实姓名",
        example="张三"
    )
    phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="手机号码",
        example="13800138000"
    )
    avatar: Optional[str] = Field(
        None,
        description="头像URL",
        example="/uploads/avatars/user_123.jpg"
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )
    role_ids: Optional[List[int]] = Field(
        None,
        description="角色ID列表",
        example=[1, 2]
    )


class UserLogin(BaseSchema):
    """用户登录模式"""
    username: str = Field(
        ...,
        description="用户名或邮箱",
        example="zhangsan"
    )
    password: str = Field(
        ...,
        description="密码",
        example="password123"
    )
    remember_me: bool = Field(
        False,
        description="记住我",
        example=False
    )


class UserResponse(UserBase, TimestampMixin):
    """用户响应模式"""
    id: int = Field(
        ...,
        description="用户ID",
        example=1
    )
    is_superuser: bool = Field(
        False,
        description="是否超级用户",
        example=False
    )
    is_verified: bool = Field(
        False,
        description="是否已验证邮箱",
        example=True
    )
    last_login: Optional[datetime] = Field(
        None,
        description="最后登录时间",
        example="2024-01-01T00:00:00Z"
    )
    roles: Optional[List['RoleResponse']] = Field(
        None,
        description="用户角色列表"
    )


# ============================================================================
# 认证令牌相关模式
# ============================================================================

class TokenResponse(BaseSchema):
    """令牌响应模式"""
    access_token: str = Field(
        ...,
        description="访问令牌",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    refresh_token: str = Field(
        ...,
        description="刷新令牌",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    token_type: str = Field(
        "bearer",
        description="令牌类型",
        example="bearer"
    )
    expires_in: int = Field(
        ...,
        description="访问令牌过期时间（秒）",
        example=3600
    )
    user: UserResponse = Field(
        ...,
        description="用户信息"
    )


class RefreshTokenRequest(BaseSchema):
    """刷新令牌请求模式"""
    refresh_token: str = Field(
        ...,
        description="刷新令牌",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )


class PasswordResetRequest(BaseSchema):
    """密码重置请求模式"""
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        example="zhangsan@example.com"
    )


class PasswordResetConfirm(BaseSchema):
    """密码重置确认模式"""
    token: str = Field(
        ...,
        description="重置令牌",
        example="reset_token_123456"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="新密码",
        example="newpassword123"
    )
    confirm_password: str = Field(
        ...,
        description="确认新密码",
        example="newpassword123"
    )
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('密码不匹配')
        return v


class PasswordChangeRequest(BaseSchema):
    """密码修改请求模式"""
    current_password: str = Field(
        ...,
        description="当前密码",
        example="oldpassword123"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="新密码",
        example="newpassword123"
    )
    confirm_password: str = Field(
        ...,
        description="确认新密码",
        example="newpassword123"
    )
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('密码不匹配')
        return v


class EmailVerificationRequest(BaseSchema):
    """邮箱验证请求模式"""
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        example="zhangsan@example.com"
    )


class EmailVerificationConfirm(BaseSchema):
    """邮箱验证确认模式"""
    token: str = Field(
        ...,
        description="验证令牌",
        example="verify_token_123456"
    )


# ============================================================================
# 角色相关模式
# ============================================================================

class RoleBase(BaseSchema):
    """角色基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="角色名称",
        example="管理员"
    )
    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
        regex="^[A-Z_]+$",
        description="角色代码",
        example="ADMIN"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="角色描述",
        example="系统管理员角色"
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class RoleCreate(RoleBase):
    """角色创建模式"""
    permission_ids: Optional[List[int]] = Field(
        None,
        description="权限ID列表",
        example=[1, 2, 3]
    )


class RoleUpdate(BaseSchema):
    """角色更新模式"""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="角色名称",
        example="管理员"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="角色描述",
        example="系统管理员角色"
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )
    permission_ids: Optional[List[int]] = Field(
        None,
        description="权限ID列表",
        example=[1, 2, 3]
    )


class RoleResponse(RoleBase, TimestampMixin):
    """角色响应模式"""
    id: int = Field(
        ...,
        description="角色ID",
        example=1
    )
    user_count: Optional[int] = Field(
        None,
        description="用户数量",
        example=10
    )
    permissions: Optional[List['PermissionResponse']] = Field(
        None,
        description="权限列表"
    )


# ============================================================================
# 权限相关模式
# ============================================================================

class PermissionBase(BaseSchema):
    """权限基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="权限名称",
        example="用户管理"
    )
    code: str = Field(
        ...,
        min_length=2,
        max_length=100,
        regex="^[a-z_:]+$",
        description="权限代码",
        example="user:manage"
    )
    resource: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="资源名称",
        example="user"
    )
    action: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="操作名称",
        example="manage"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="权限描述",
        example="用户管理权限"
    )


class PermissionResponse(PermissionBase, TimestampMixin):
    """权限响应模式"""
    id: int = Field(
        ...,
        description="权限ID",
        example=1
    )


# ============================================================================
# API密钥相关模式
# ============================================================================

class ApiKeyBase(BaseSchema):
    """API密钥基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="密钥名称",
        example="移动端API密钥"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="密钥描述",
        example="用于移动端应用的API访问"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="过期时间",
        example="2024-12-31T23:59:59Z"
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class ApiKeyCreate(ApiKeyBase):
    """API密钥创建模式"""
    pass


class ApiKeyUpdate(BaseSchema):
    """API密钥更新模式"""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="密钥名称",
        example="移动端API密钥"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="密钥描述",
        example="用于移动端应用的API访问"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="过期时间",
        example="2024-12-31T23:59:59Z"
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )


class ApiKeyResponse(ApiKeyBase, TimestampMixin):
    """API密钥响应模式"""
    id: int = Field(
        ...,
        description="密钥ID",
        example=1
    )
    key: Optional[str] = Field(
        None,
        description="密钥值（仅创建时返回）",
        example="ak_1234567890abcdef"
    )
    key_prefix: str = Field(
        ...,
        description="密钥前缀",
        example="ak_1234"
    )
    last_used: Optional[datetime] = Field(
        None,
        description="最后使用时间",
        example="2024-01-01T00:00:00Z"
    )
    user_id: int = Field(
        ...,
        description="用户ID",
        example=1
    )


# ============================================================================
# 会话相关模式
# ============================================================================

class UserSessionResponse(BaseSchema, TimestampMixin):
    """用户会话响应模式"""
    id: int = Field(
        ...,
        description="会话ID",
        example=1
    )
    session_id: str = Field(
        ...,
        description="会话标识",
        example="session_123456789"
    )
    ip_address: Optional[str] = Field(
        None,
        description="IP地址",
        example="192.168.1.100"
    )
    user_agent: Optional[str] = Field(
        None,
        description="用户代理",
        example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    is_active: bool = Field(
        True,
        description="是否活跃",
        example=True
    )
    expires_at: datetime = Field(
        ...,
        description="过期时间",
        example="2024-01-02T00:00:00Z"
    )
    user_id: int = Field(
        ...,
        description="用户ID",
        example=1
    )


# ============================================================================
# 登录尝试相关模式
# ============================================================================

class LoginAttemptResponse(BaseSchema, TimestampMixin):
    """登录尝试响应模式"""
    id: int = Field(
        ...,
        description="尝试ID",
        example=1
    )
    username: str = Field(
        ...,
        description="用户名",
        example="zhangsan"
    )
    ip_address: Optional[str] = Field(
        None,
        description="IP地址",
        example="192.168.1.100"
    )
    user_agent: Optional[str] = Field(
        None,
        description="用户代理",
        example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    success: bool = Field(
        ...,
        description="是否成功",
        example=True
    )
    failure_reason: Optional[str] = Field(
        None,
        description="失败原因",
        example="密码错误"
    )
    user_id: Optional[int] = Field(
        None,
        description="用户ID",
        example=1
    )


# 更新前向引用
UserResponse.model_rebuild()
RoleResponse.model_rebuild()