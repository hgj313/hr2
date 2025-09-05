"""API模块初始化文件

本模块包含了人力资源调度系统的所有API端点定义。
"""

from app.api.v1.api import api_router

__all__ = ["api_router"]