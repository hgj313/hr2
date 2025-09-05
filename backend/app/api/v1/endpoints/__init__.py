"""API端点模块初始化文件

本模块包含了人力资源调度系统所有业务模块的API端点实现。
"""

from app.api.v1.endpoints import (
    auth,
    users,
    organizations,
    projects,
    schedules,
    approvals,
    risks,
    analytics
)

__all__ = [
    "auth",
    "users",
    "organizations",
    "projects",
    "schedules",
    "approvals",
    "risks",
    "analytics"
]