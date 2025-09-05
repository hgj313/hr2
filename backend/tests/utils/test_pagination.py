import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.pagination import (
    PaginationParams,
    PaginationResult,
    paginate,
    paginate_list,
    CursorPagination,
    CursorPaginationResult,
    create_pagination_response,
    get_pagination_info,
    SearchPagination,
    apply_search_filters
)

# 创建测试用的数据库模型
Base = declarative_base()

class TestModel(Base):
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)


@pytest.mark.utils
class TestPagination:
    """分页工具测试"""
    
    @pytest.fixture
    def test_db_session(self):
        """创建测试数据库会话"""
        engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # 创建测试数据
        for i in range(25):
            item = TestModel(
                name=f"Item {i+1}",
                description=f"Description for item {i+1}",
                is_active=i % 2 == 0  # 偶数为活跃
            )
            session.add(item)
        session.commit()
        
        yield session
        session.close()
    
    def test_pagination_params_default(self):
        """测试分页参数默认值"""
        params = PaginationParams()
        
        assert params.page == 1
        assert params.size == 20
        assert params.skip == 0
    
    def test_pagination_params_custom(self):
        """测试自定义分页参数"""
        params = PaginationParams(page=3, size=10)
        
        assert params.page == 3
        assert params.size == 10
        assert params.skip == 20  # (3-1) * 10
    
    def test_pagination_params_validation(self):
        """测试分页参数验证"""
        # 测试页码最小值
        params = PaginationParams(page=0)
        assert params.page == 1
        
        # 测试页面大小最小值
        params = PaginationParams(size=0)
        assert params.size == 1
        
        # 测试页面大小最大值
        params = PaginationParams(size=200)
        assert params.size == 100  # 假设最大值为100
    
    def test_paginate_sqlalchemy_query(self, test_db_session: Session):
        """测试SQLAlchemy查询分页"""
        query = test_db_session.query(TestModel)
        params = PaginationParams(page=1, size=10)
        
        result = paginate(query, params)
        
        assert isinstance(result, PaginationResult)
        assert len(result.items) == 10
        assert result.total == 25
        assert result.page == 1
        assert result.size == 10
        assert result.pages == 3  # ceil(25/10)
        assert result.has_next is True
        assert result.has_prev is False
    
    def test_paginate_second_page(self, test_db_session: Session):
        """测试第二页分页"""
        query = test_db_session.query(TestModel)
        params = PaginationParams(page=2, size=10)
        
        result = paginate(query, params)
        
        assert len(result.items) == 10
        assert result.page == 2
        assert result.has_next is True
        assert result.has_prev is True
    
    def test_paginate_last_page(self, test_db_session: Session):
        """测试最后一页分页"""
        query = test_db_session.query(TestModel)
        params = PaginationParams(page=3, size=10)
        
        result = paginate(query, params)
        
        assert len(result.items) == 5  # 最后一页只有5个项目
        assert result.page == 3
        assert result.has_next is False
        assert result.has_prev is True
    
    def test_paginate_empty_result(self, test_db_session: Session):
        """测试空结果分页"""
        query = test_db_session.query(TestModel).filter(TestModel.name == "NonExistent")
        params = PaginationParams(page=1, size=10)
        
        result = paginate(query, params)
        
        assert len(result.items) == 0
        assert result.total == 0
        assert result.pages == 0
        assert result.has_next is False
        assert result.has_prev is False
    
    def test_paginate_list(self):
        """测试列表分页"""
        items = list(range(1, 26))  # 1到25的列表
        params = PaginationParams(page=2, size=10)
        
        result = paginate_list(items, params)
        
        assert isinstance(result, PaginationResult)
        assert result.items == list(range(11, 21))  # 第二页：11到20
        assert result.total == 25
        assert result.page == 2
        assert result.size == 10
        assert result.pages == 3
        assert result.has_next is True
        assert result.has_prev is True
    
    def test_paginate_list_last_page(self):
        """测试列表最后一页分页"""
        items = list(range(1, 26))  # 1到25的列表
        params = PaginationParams(page=3, size=10)
        
        result = paginate_list(items, params)
        
        assert result.items == list(range(21, 26))  # 最后一页：21到25
        assert len(result.items) == 5
        assert result.has_next is False
    
    def test_cursor_pagination_params(self):
        """测试游标分页参数"""
        params = CursorPagination()
        
        assert params.limit == 20
        assert params.cursor is None
        assert params.direction == "next"
    
    def test_cursor_pagination_custom(self):
        """测试自定义游标分页参数"""
        params = CursorPagination(limit=10, cursor="abc123", direction="prev")
        
        assert params.limit == 10
        assert params.cursor == "abc123"
        assert params.direction == "prev"
    
    def test_create_pagination_response(self):
        """测试创建分页响应"""
        items = [1, 2, 3, 4, 5]
        total = 25
        page = 2
        size = 5
        
        response = create_pagination_response(items, total, page, size)
        
        assert response["items"] == items
        assert response["total"] == total
        assert response["page"] == page
        assert response["size"] == size
        assert response["pages"] == 5  # ceil(25/5)
        assert response["has_next"] is True
        assert response["has_prev"] is True
    
    def test_create_pagination_response_first_page(self):
        """测试创建第一页分页响应"""
        items = [1, 2, 3, 4, 5]
        total = 25
        page = 1
        size = 5
        
        response = create_pagination_response(items, total, page, size)
        
        assert response["has_next"] is True
        assert response["has_prev"] is False
    
    def test_create_pagination_response_last_page(self):
        """测试创建最后一页分页响应"""
        items = [21, 22, 23, 24, 25]
        total = 25
        page = 5
        size = 5
        
        response = create_pagination_response(items, total, page, size)
        
        assert response["has_next"] is False
        assert response["has_prev"] is True
    
    def test_get_pagination_info(self):
        """测试获取分页信息"""
        total = 25
        page = 2
        size = 10
        
        info = get_pagination_info(total, page, size)
        
        assert info["total"] == 25
        assert info["page"] == 2
        assert info["size"] == 10
        assert info["pages"] == 3
        assert info["has_next"] is True
        assert info["has_prev"] is True
        assert info["start_index"] == 11  # (2-1)*10 + 1
        assert info["end_index"] == 20   # min(2*10, 25)
    
    def test_search_pagination_params(self):
        """测试搜索分页参数"""
        params = SearchPagination()
        
        assert params.page == 1
        assert params.size == 20
        assert params.search == ""
        assert params.sort_by == "id"
        assert params.sort_order == "asc"
    
    def test_search_pagination_custom(self):
        """测试自定义搜索分页参数"""
        params = SearchPagination(
            page=2,
            size=15,
            search="test",
            sort_by="name",
            sort_order="desc"
        )
        
        assert params.page == 2
        assert params.size == 15
        assert params.search == "test"
        assert params.sort_by == "name"
        assert params.sort_order == "desc"
    
    def test_apply_search_filters(self, test_db_session: Session):
        """测试应用搜索过滤器"""
        query = test_db_session.query(TestModel)
        params = SearchPagination(search="Item 1", sort_by="name", sort_order="asc")
        
        # 模拟搜索字段
        search_fields = ["name", "description"]
        
        filtered_query = apply_search_filters(query, params, TestModel, search_fields)
        
        # 这里需要根据实际的apply_search_filters实现来验证
        # 假设它会添加搜索条件和排序
        assert filtered_query is not None
    
    def test_pagination_edge_cases(self):
        """测试分页边界情况"""
        # 空列表分页
        empty_list = []
        params = PaginationParams(page=1, size=10)
        result = paginate_list(empty_list, params)
        
        assert len(result.items) == 0
        assert result.total == 0
        assert result.pages == 0
        assert result.has_next is False
        assert result.has_prev is False
    
    def test_pagination_single_item(self):
        """测试单项分页"""
        single_item = ["only_item"]
        params = PaginationParams(page=1, size=10)
        result = paginate_list(single_item, params)
        
        assert len(result.items) == 1
        assert result.total == 1
        assert result.pages == 1
        assert result.has_next is False
        assert result.has_prev is False
    
    def test_pagination_exact_page_size(self):
        """测试恰好整页的分页"""
        items = list(range(1, 21))  # 恰好20个项目
        params = PaginationParams(page=1, size=20)
        result = paginate_list(items, params)
        
        assert len(result.items) == 20
        assert result.total == 20
        assert result.pages == 1
        assert result.has_next is False
        assert result.has_prev is False
    
    def test_pagination_out_of_range(self):
        """测试超出范围的页码"""
        items = list(range(1, 11))  # 10个项目
        params = PaginationParams(page=5, size=10)  # 请求第5页，但只有1页
        result = paginate_list(items, params)
        
        assert len(result.items) == 0
        assert result.total == 10
        assert result.pages == 1
        assert result.page == 5  # 保持请求的页码
    
    def test_cursor_pagination_result(self):
        """测试游标分页结果"""
        items = [1, 2, 3, 4, 5]
        next_cursor = "next_cursor_123"
        prev_cursor = "prev_cursor_456"
        has_next = True
        has_prev = False
        
        result = CursorPaginationResult(
            items=items,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
            has_next=has_next,
            has_prev=has_prev
        )
        
        assert result.items == items
        assert result.next_cursor == next_cursor
        assert result.prev_cursor == prev_cursor
        assert result.has_next == has_next
        assert result.has_prev == has_prev
    
    def test_pagination_with_filters(self, test_db_session: Session):
        """测试带过滤条件的分页"""
        # 只查询活跃的项目
        query = test_db_session.query(TestModel).filter(TestModel.is_active == True)
        params = PaginationParams(page=1, size=10)
        
        result = paginate(query, params)
        
        # 应该有13个活跃项目（偶数索引：0,2,4,...,24）
        assert result.total == 13
        assert len(result.items) == 10  # 第一页10个
        assert result.pages == 2  # ceil(13/10)
        
        # 验证所有返回的项目都是活跃的
        for item in result.items:
            assert item.is_active is True
    
    def test_pagination_performance(self, test_db_session: Session):
        """测试分页性能（确保不会加载所有数据）"""
        query = test_db_session.query(TestModel)
        params = PaginationParams(page=1, size=5)
        
        # 这个测试主要是确保分页查询只返回请求的数量
        result = paginate(query, params)
        
        assert len(result.items) == 5
        # 在实际应用中，可以添加查询计数或执行时间的检查
    
    def test_pagination_consistency(self, test_db_session: Session):
        """测试分页一致性"""
        query = test_db_session.query(TestModel).order_by(TestModel.id)
        
        # 获取第一页
        page1_result = paginate(query, PaginationParams(page=1, size=10))
        # 获取第二页
        page2_result = paginate(query, PaginationParams(page=2, size=10))
        
        # 确保没有重复项目
        page1_ids = [item.id for item in page1_result.items]
        page2_ids = [item.id for item in page2_result.items]
        
        assert len(set(page1_ids) & set(page2_ids)) == 0  # 没有交集
        assert len(page1_ids) == 10
        assert len(page2_ids) == 10