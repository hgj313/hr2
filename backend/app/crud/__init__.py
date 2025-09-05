"""CRUD操作包初始化文件

本模块包含了人力资源调度系统的所有数据库CRUD操作。
"""

from app.crud.base import CRUDBase
from app.crud.crud_user import crud_user

__all__ = [
    "CRUDBase",
    "crud_user"
]