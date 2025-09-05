from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from datetime import datetime

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD基类"""
    
    def __init__(self, model: Type[ModelType]):
        """
        CRUD对象，包含默认的增删改查操作
        
        **参数**
        * `model`: SQLAlchemy模型类
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """根据ID获取单个记录"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """获取多个记录"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_multi_with_total(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[List[ModelType], int]:
        """获取多个记录及总数"""
        query = db.query(self.model)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def get_multi_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> tuple[List[ModelType], int]:
        """根据过滤条件获取多个记录"""
        query = db.query(self.model)
        
        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        query = query.filter(column.in_(value))
                    elif isinstance(value, str) and key.endswith('_search'):
                        # 模糊搜索
                        actual_key = key.replace('_search', '')
                        if hasattr(self.model, actual_key):
                            actual_column = getattr(self.model, actual_key)
                            query = query.filter(actual_column.ilike(f"%{value}%"))
                    else:
                        query = query.filter(column == value)
        
        # 应用排序
        if order_by and hasattr(self.model, order_by):
            column = getattr(self.model, order_by)
            if order_desc:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """创建新记录"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        
        # 设置创建时间
        if hasattr(db_obj, 'created_at'):
            db_obj.created_at = datetime.utcnow()
        if hasattr(db_obj, 'updated_at'):
            db_obj.updated_at = datetime.utcnow()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """更新记录"""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        # 设置更新时间
        if hasattr(db_obj, 'updated_at'):
            db_obj.updated_at = datetime.utcnow()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """删除记录（软删除或硬删除）"""
        obj = db.query(self.model).get(id)
        if obj:
            if hasattr(obj, 'is_deleted'):
                # 软删除
                obj.is_deleted = True
                if hasattr(obj, 'deleted_at'):
                    obj.deleted_at = datetime.utcnow()
                if hasattr(obj, 'updated_at'):
                    obj.updated_at = datetime.utcnow()
                db.add(obj)
            else:
                # 硬删除
                db.delete(obj)
            db.commit()
        return obj
    
    def count(self, db: Session, *, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计记录数量"""
        query = db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        query = query.filter(column.in_(value))
                    else:
                        query = query.filter(column == value)
        
        return query.count()
    
    def exists(self, db: Session, *, id: int) -> bool:
        """检查记录是否存在"""
        return db.query(self.model).filter(self.model.id == id).first() is not None
    
    def get_by_field(
        self, 
        db: Session, 
        field_name: str, 
        field_value: Any
    ) -> Optional[ModelType]:
        """根据指定字段获取记录"""
        if hasattr(self.model, field_name):
            column = getattr(self.model, field_name)
            return db.query(self.model).filter(column == field_value).first()
        return None
    
    def get_multi_by_field(
        self, 
        db: Session, 
        field_name: str, 
        field_value: Any,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """根据指定字段获取多个记录"""
        if hasattr(self.model, field_name):
            column = getattr(self.model, field_name)
            return db.query(self.model).filter(
                column == field_value
            ).offset(skip).limit(limit).all()
        return []
    
    def search(
        self,
        db: Session,
        *,
        query_str: str,
        search_fields: List[str],
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[ModelType], int]:
        """全文搜索"""
        query = db.query(self.model)
        
        if query_str and search_fields:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    search_conditions.append(
                        column.ilike(f"%{query_str}%")
                    )
            
            if search_conditions:
                query = query.filter(or_(*search_conditions))
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def bulk_create(
        self, 
        db: Session, 
        *, 
        objs_in: List[CreateSchemaType]
    ) -> List[ModelType]:
        """批量创建记录"""
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            
            # 设置创建时间
            if hasattr(db_obj, 'created_at'):
                db_obj.created_at = datetime.utcnow()
            if hasattr(db_obj, 'updated_at'):
                db_obj.updated_at = datetime.utcnow()
            
            db_objs.append(db_obj)
        
        db.add_all(db_objs)
        db.commit()
        
        for db_obj in db_objs:
            db.refresh(db_obj)
        
        return db_objs
    
    def bulk_update(
        self,
        db: Session,
        *,
        updates: List[Dict[str, Any]]
    ) -> List[ModelType]:
        """批量更新记录"""
        updated_objs = []
        
        for update_data in updates:
            if 'id' not in update_data:
                continue
            
            obj_id = update_data.pop('id')
            db_obj = self.get(db, id=obj_id)
            
            if db_obj:
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                
                # 设置更新时间
                if hasattr(db_obj, 'updated_at'):
                    db_obj.updated_at = datetime.utcnow()
                
                updated_objs.append(db_obj)
        
        if updated_objs:
            db.add_all(updated_objs)
            db.commit()
            
            for db_obj in updated_objs:
                db.refresh(db_obj)
        
        return updated_objs
    
    def bulk_delete(
        self, 
        db: Session, 
        *, 
        ids: List[int]
    ) -> int:
        """批量删除记录"""
        deleted_count = 0
        
        for obj_id in ids:
            if self.remove(db, id=obj_id):
                deleted_count += 1
        
        return deleted_count
    
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取活跃记录（如果模型有is_active字段）"""
        query = db.query(self.model)
        
        if hasattr(self.model, 'is_active'):
            query = query.filter(self.model.is_active == True)
        
        if hasattr(self.model, 'is_deleted'):
            query = query.filter(self.model.is_deleted == False)
        
        return query.offset(skip).limit(limit).all()
    
    def get_recent(
        self, 
        db: Session, 
        *, 
        days: int = 7, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """获取最近创建的记录"""
        query = db.query(self.model)
        
        if hasattr(self.model, 'created_at'):
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(self.model.created_at >= cutoff_date)
            query = query.order_by(desc(self.model.created_at))
        
        return query.offset(skip).limit(limit).all()