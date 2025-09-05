from typing import Any, Dict, List, Optional, TypeVar, Generic
from math import ceil
from sqlalchemy.orm import Query
from pydantic import BaseModel

T = TypeVar('T')


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = 1
    size: int = 20
    
    @property
    def skip(self) -> int:
        """计算跳过的记录数"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """获取限制数量"""
        return self.size


class PaginationResult(BaseModel, Generic[T]):
    """分页结果"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> 'PaginationResult[T]':
        """创建分页结果"""
        pages = ceil(total / size) if size > 0 else 0
        
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


def paginate(
    query: Query,
    page: int = 1,
    size: int = 20,
    max_size: int = 100
) -> PaginationResult:
    """对SQLAlchemy查询进行分页"""
    # 限制分页大小
    if size > max_size:
        size = max_size
    if size < 1:
        size = 1
    if page < 1:
        page = 1
    
    # 计算总数
    total = query.count()
    
    # 计算跳过的记录数
    skip = (page - 1) * size
    
    # 获取分页数据
    items = query.offset(skip).limit(size).all()
    
    return PaginationResult.create(
        items=items,
        total=total,
        page=page,
        size=size
    )


def paginate_list(
    items: List[T],
    page: int = 1,
    size: int = 20,
    max_size: int = 100
) -> PaginationResult[T]:
    """对列表进行分页"""
    # 限制分页大小
    if size > max_size:
        size = max_size
    if size < 1:
        size = 1
    if page < 1:
        page = 1
    
    total = len(items)
    
    # 计算跳过的记录数
    skip = (page - 1) * size
    
    # 获取分页数据
    paginated_items = items[skip:skip + size]
    
    return PaginationResult.create(
        items=paginated_items,
        total=total,
        page=page,
        size=size
    )


class CursorPagination(BaseModel):
    """游标分页参数"""
    cursor: Optional[str] = None
    size: int = 20
    direction: str = "next"  # next 或 prev


class CursorPaginationResult(BaseModel, Generic[T]):
    """游标分页结果"""
    items: List[T]
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None
    has_next: bool = False
    has_prev: bool = False
    size: int
    
    @classmethod
    def create(
        cls,
        items: List[T],
        next_cursor: Optional[str] = None,
        prev_cursor: Optional[str] = None,
        has_next: bool = False,
        has_prev: bool = False,
        size: int = 20
    ) -> 'CursorPaginationResult[T]':
        """创建游标分页结果"""
        return cls(
            items=items,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
            has_next=has_next,
            has_prev=has_prev,
            size=size
        )


def create_pagination_response(
    items: List[Any],
    total: int,
    page: int,
    size: int,
    additional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """创建标准分页响应"""
    pages = ceil(total / size) if size > 0 else 0
    
    response = {
        "items": items,
        "pagination": {
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1
        }
    }
    
    if additional_data:
        response.update(additional_data)
    
    return response


def get_pagination_info(
    total: int,
    page: int,
    size: int
) -> Dict[str, Any]:
    """获取分页信息"""
    pages = ceil(total / size) if size > 0 else 0
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
        "start_index": (page - 1) * size + 1 if total > 0 else 0,
        "end_index": min(page * size, total)
    }


class SearchPagination(BaseModel):
    """搜索分页参数"""
    query: Optional[str] = None
    page: int = 1
    size: int = 20
    sort_by: Optional[str] = None
    sort_order: str = "asc"  # asc 或 desc
    filters: Optional[Dict[str, Any]] = None
    
    @property
    def skip(self) -> int:
        """计算跳过的记录数"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """获取限制数量"""
        return self.size
    
    def get_order_by_clause(self, model_class):
        """获取排序子句"""
        if not self.sort_by:
            return None
        
        if not hasattr(model_class, self.sort_by):
            return None
        
        column = getattr(model_class, self.sort_by)
        
        if self.sort_order.lower() == "desc":
            return column.desc()
        else:
            return column.asc()


def apply_search_filters(
    query: Query,
    search_params: SearchPagination,
    model_class,
    searchable_fields: List[str] = None
) -> Query:
    """应用搜索过滤器"""
    # 应用搜索查询
    if search_params.query and searchable_fields:
        search_conditions = []
        for field in searchable_fields:
            if hasattr(model_class, field):
                column = getattr(model_class, field)
                search_conditions.append(
                    column.ilike(f"%{search_params.query}%")
                )
        
        if search_conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*search_conditions))
    
    # 应用过滤器
    if search_params.filters:
        for field, value in search_params.filters.items():
            if hasattr(model_class, field) and value is not None:
                column = getattr(model_class, field)
                if isinstance(value, list):
                    query = query.filter(column.in_(value))
                else:
                    query = query.filter(column == value)
    
    # 应用排序
    order_by = search_params.get_order_by_clause(model_class)
    if order_by is not None:
        query = query.order_by(order_by)
    
    return query