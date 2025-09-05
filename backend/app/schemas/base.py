"""基础Pydantic模式定义

本模块定义了系统中通用的基础模式，包括响应格式、分页等。
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# 泛型类型变量
DataType = TypeVar('DataType')


class BaseSchema(BaseModel):
    """基础模式类
    
    所有Pydantic模式的基类，提供通用配置。
    """
    model_config = ConfigDict(
        # 允许使用ORM模式
        from_attributes=True,
        # 验证赋值
        validate_assignment=True,
        # 使用枚举值
        use_enum_values=True,
        # 序列化时排除未设置的字段
        exclude_unset=True,
        # 序列化时排除None值
        exclude_none=True
    )


class TimestampMixin(BaseSchema):
    """时间戳混入类
    
    为模式添加创建时间和更新时间字段。
    """
    created_at: Optional[datetime] = Field(
        None,
        description="创建时间",
        example="2024-01-01T00:00:00Z"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="更新时间",
        example="2024-01-01T00:00:00Z"
    )


class BaseResponse(BaseSchema):
    """基础响应模式
    
    所有API响应的基础格式。
    """
    success: bool = Field(
        True,
        description="请求是否成功",
        example=True
    )
    message: str = Field(
        "操作成功",
        description="响应消息",
        example="操作成功"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="响应时间戳",
        example="2024-01-01T00:00:00Z"
    )
    request_id: Optional[str] = Field(
        None,
        description="请求ID",
        example="req_123456789"
    )


class SuccessResponse(BaseResponse):
    """成功响应模式"""
    success: bool = Field(
        True,
        description="请求成功",
        example=True
    )


class ErrorResponse(BaseResponse):
    """错误响应模式"""
    success: bool = Field(
        False,
        description="请求失败",
        example=False
    )
    error_code: Optional[str] = Field(
        None,
        description="错误代码",
        example="VALIDATION_ERROR"
    )
    error_details: Optional[Dict[str, Any]] = Field(
        None,
        description="错误详情",
        example={"field": "username", "message": "用户名已存在"}
    )


class MessageResponse(BaseResponse):
    """消息响应模式
    
    用于只返回消息的简单响应。
    """
    pass


class DataResponse(BaseResponse, Generic[DataType]):
    """数据响应模式
    
    用于返回单个数据对象的响应。
    """
    data: DataType = Field(
        ...,
        description="响应数据"
    )


class PaginationInfo(BaseSchema):
    """分页信息模式"""
    page: int = Field(
        1,
        ge=1,
        description="当前页码",
        example=1
    )
    size: int = Field(
        20,
        ge=1,
        le=100,
        description="每页大小",
        example=20
    )
    total: int = Field(
        0,
        ge=0,
        description="总记录数",
        example=100
    )
    pages: int = Field(
        0,
        ge=0,
        description="总页数",
        example=5
    )
    has_next: bool = Field(
        False,
        description="是否有下一页",
        example=True
    )
    has_prev: bool = Field(
        False,
        description="是否有上一页",
        example=False
    )


class PaginatedResponse(BaseResponse, Generic[DataType]):
    """分页响应模式
    
    用于返回分页数据的响应。
    """
    data: List[DataType] = Field(
        default_factory=list,
        description="数据列表"
    )
    pagination: PaginationInfo = Field(
        ...,
        description="分页信息"
    )


class ListResponse(BaseResponse, Generic[DataType]):
    """列表响应模式
    
    用于返回数据列表的响应（不分页）。
    """
    data: List[DataType] = Field(
        default_factory=list,
        description="数据列表"
    )
    count: int = Field(
        0,
        ge=0,
        description="数据总数",
        example=10
    )


class SearchParams(BaseSchema):
    """搜索参数模式"""
    keyword: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="搜索关键词",
        example="张三"
    )
    page: int = Field(
        1,
        ge=1,
        description="页码",
        example=1
    )
    size: int = Field(
        20,
        ge=1,
        le=100,
        description="每页大小",
        example=20
    )
    sort_by: Optional[str] = Field(
        None,
        description="排序字段",
        example="created_at"
    )
    sort_order: Optional[str] = Field(
        "desc",
        regex="^(asc|desc)$",
        description="排序方向",
        example="desc"
    )


class FilterParams(BaseSchema):
    """过滤参数模式"""
    start_date: Optional[datetime] = Field(
        None,
        description="开始日期",
        example="2024-01-01T00:00:00Z"
    )
    end_date: Optional[datetime] = Field(
        None,
        description="结束日期",
        example="2024-12-31T23:59:59Z"
    )
    status: Optional[str] = Field(
        None,
        description="状态过滤",
        example="active"
    )
    category: Optional[str] = Field(
        None,
        description="分类过滤",
        example="category1"
    )


class BulkOperationRequest(BaseSchema):
    """批量操作请求模式"""
    ids: List[int] = Field(
        ...,
        min_items=1,
        description="ID列表",
        example=[1, 2, 3]
    )
    operation: str = Field(
        ...,
        description="操作类型",
        example="delete"
    )
    params: Optional[Dict[str, Any]] = Field(
        None,
        description="操作参数",
        example={"status": "inactive"}
    )


class BulkOperationResponse(BaseResponse):
    """批量操作响应模式"""
    processed: int = Field(
        0,
        ge=0,
        description="处理成功数量",
        example=3
    )
    failed: int = Field(
        0,
        ge=0,
        description="处理失败数量",
        example=0
    )
    errors: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="错误详情列表",
        example=[{"id": 1, "error": "记录不存在"}]
    )


class HealthCheckResponse(BaseResponse):
    """健康检查响应模式"""
    status: str = Field(
        "healthy",
        description="服务状态",
        example="healthy"
    )
    version: str = Field(
        "1.0.0",
        description="服务版本",
        example="1.0.0"
    )
    uptime: int = Field(
        0,
        ge=0,
        description="运行时间（秒）",
        example=3600
    )
    database: str = Field(
        "connected",
        description="数据库状态",
        example="connected"
    )
    redis: str = Field(
        "connected",
        description="Redis状态",
        example="connected"
    )


class FileUploadResponse(BaseResponse):
    """文件上传响应模式"""
    file_id: str = Field(
        ...,
        description="文件ID",
        example="file_123456789"
    )
    filename: str = Field(
        ...,
        description="文件名",
        example="document.pdf"
    )
    file_size: int = Field(
        ...,
        ge=0,
        description="文件大小（字节）",
        example=1024000
    )
    file_type: str = Field(
        ...,
        description="文件类型",
        example="application/pdf"
    )
    file_url: str = Field(
        ...,
        description="文件访问URL",
        example="/api/v1/files/file_123456789"
    )


class ExportRequest(BaseSchema):
    """导出请求模式"""
    format: str = Field(
        "excel",
        regex="^(excel|csv|pdf)$",
        description="导出格式",
        example="excel"
    )
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="过滤条件",
        example={"status": "active"}
    )
    columns: Optional[List[str]] = Field(
        None,
        description="导出列",
        example=["name", "email", "created_at"]
    )


class ExportResponse(BaseResponse):
    """导出响应模式"""
    task_id: str = Field(
        ...,
        description="导出任务ID",
        example="export_123456789"
    )
    status: str = Field(
        "processing",
        description="导出状态",
        example="processing"
    )
    download_url: Optional[str] = Field(
        None,
        description="下载链接",
        example="/api/v1/exports/export_123456789/download"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="链接过期时间",
        example="2024-01-02T00:00:00Z"
    )


class StatisticsResponse(BaseResponse):
    """统计响应模式"""
    data: Dict[str, Any] = Field(
        ...,
        description="统计数据",
        example={
            "total_users": 100,
            "active_users": 80,
            "new_users_today": 5
        }
    )
    period: str = Field(
        "today",
        description="统计周期",
        example="today"
    )
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="统计生成时间",
        example="2024-01-01T00:00:00Z"
    )