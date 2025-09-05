"""API v1版本模块初始化文件

本模块包含了人力资源调度系统API v1版本的所有端点定义。
"""

from app.api.v1.api import api_router

__all__ = ["api_router"]