"""API v1版本主路由文件

本文件整合了人力资源调度系统所有业务模块的API路由。
"""

from fastapi import APIRouter

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

# 创建API路由器
api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"]
)

# 用户管理路由
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"]
)

# 组织架构路由
api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["组织架构"]
)

# 项目管理路由
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["项目管理"]
)

# 调度管理路由
api_router.include_router(
    schedules.router,
    prefix="/schedules",
    tags=["调度管理"]
)

# 审批流程路由
api_router.include_router(
    approvals.router,
    prefix="/approvals",
    tags=["审批流程"]
)

# 风险管控路由
api_router.include_router(
    risks.router,
    prefix="/risks",
    tags=["风险管控"]
)

# 数据分析路由
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["数据分析"]
)