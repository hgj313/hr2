from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from typing import List, Optional

from app.core.database import Base


class Department(Base):
    """部门表模型"""
    __tablename__ = "departments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), index=True)
    level = Column(Integer, nullable=False, default=1, index=True)
    path = Column(String(500), nullable=False, index=True)  # 层级路径，如：/root/dept1/subdept1
    sort_order = Column(Integer, default=0)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id"), index=True)
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    address = Column(Text)
    budget = Column(Numeric(15, 2))
    cost_center = Column(String(50), index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    parent = relationship("Department", remote_side=[id], back_populates="children")
    children = relationship("Department", back_populates="parent", cascade="all, delete-orphan")
    manager = relationship("Personnel", foreign_keys=[manager_id], back_populates="managed_departments")
    personnel = relationship("Personnel", back_populates="department", foreign_keys="Personnel.department_id")
    positions = relationship("Position", back_populates="department")
    
    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, code={self.code})>"
    
    @property
    def full_name(self) -> str:
        """获取部门全名（包含层级）"""
        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name
    
    def get_ancestors(self) -> List['Department']:
        """获取所有上级部门"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self) -> List['Department']:
        """获取所有下级部门"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def get_all_personnel(self) -> List['Personnel']:
        """获取部门及其下级部门的所有人员"""
        all_personnel = list(self.personnel)
        for child in self.children:
            all_personnel.extend(child.get_all_personnel())
        return all_personnel
    
    def update_path(self):
        """更新部门路径"""
        if self.parent:
            self.path = f"{self.parent.path}/{self.code}"
            self.level = self.parent.level + 1
        else:
            self.path = f"/{self.code}"
            self.level = 1


class Position(Base):
    """职位表模型"""
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False, index=True)
    level = Column(Integer, nullable=False, default=1, index=True)  # 职级
    category = Column(String(50), nullable=False, index=True)  # 职位类别：管理、技术、业务等
    requirements = Column(JSONB)  # 任职要求
    responsibilities = Column(JSONB)  # 职责描述
    skills_required = Column(JSONB)  # 技能要求
    min_salary = Column(Numeric(10, 2))
    max_salary = Column(Numeric(10, 2))
    is_leadership = Column(Boolean, default=False, index=True)
    max_headcount = Column(Integer, default=1)  # 最大编制数
    current_headcount = Column(Integer, default=0)  # 当前在职人数
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    department = relationship("Department", back_populates="positions")
    personnel = relationship("Personnel", back_populates="position")
    
    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name}, code={self.code})>"
    
    @property
    def is_full(self) -> bool:
        """检查职位是否已满编"""
        return self.current_headcount >= self.max_headcount
    
    @property
    def vacancy_count(self) -> int:
        """获取空缺数量"""
        return max(0, self.max_headcount - self.current_headcount)
    
    def can_assign_personnel(self) -> bool:
        """检查是否可以分配人员"""
        return self.is_active and not self.is_full


class Personnel(Base):
    """人员表模型"""
    __tablename__ = "personnel"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    english_name = Column(String(100))
    gender = Column(String(10), index=True)
    birth_date = Column(DateTime(timezone=True))
    id_card = Column(String(20), unique=True, index=True)
    phone = Column(String(20), index=True)
    email = Column(String(100), index=True)
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    address = Column(Text)
    
    # 职业信息
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False, index=True)
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False, index=True)
    direct_supervisor_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id"), index=True)
    employment_type = Column(String(20), nullable=False, index=True)  # 全职、兼职、实习、外包
    employment_status = Column(String(20), nullable=False, default="active", index=True)  # active, inactive, terminated
    hire_date = Column(DateTime(timezone=True), nullable=False)
    probation_end_date = Column(DateTime(timezone=True))
    contract_start_date = Column(DateTime(timezone=True))
    contract_end_date = Column(DateTime(timezone=True))
    termination_date = Column(DateTime(timezone=True))
    termination_reason = Column(String(200))
    
    # 薪资信息
    base_salary = Column(Numeric(10, 2))
    salary_grade = Column(String(10), index=True)
    
    # 技能和资质
    skills = Column(JSONB)  # 技能列表
    certifications = Column(JSONB)  # 证书列表
    education_background = Column(JSONB)  # 教育背景
    work_experience = Column(JSONB)  # 工作经历
    
    # 工作安排
    work_location = Column(String(100), index=True)
    work_schedule = Column(JSONB)  # 工作时间安排
    availability = Column(JSONB)  # 可用性设置
    
    # 绩效相关
    performance_rating = Column(String(10), index=True)
    last_review_date = Column(DateTime(timezone=True))
    next_review_date = Column(DateTime(timezone=True))
    
    # 系统字段
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="personnel")
    department = relationship("Department", back_populates="personnel", foreign_keys=[department_id])
    position = relationship("Position", back_populates="personnel")
    direct_supervisor = relationship("Personnel", remote_side=[id], back_populates="subordinates")
    subordinates = relationship("Personnel", back_populates="direct_supervisor")
    managed_departments = relationship("Department", back_populates="manager", foreign_keys="Department.manager_id")
    
    # 项目相关关系
    project_assignments = relationship("ProjectAssignment", back_populates="personnel")
    schedule_assignments = relationship("ScheduleAssignment", back_populates="personnel")
    
    def __repr__(self):
        return f"<Personnel(id={self.id}, name={self.name}, employee_id={self.employee_id})>"
    
    @property
    def full_name(self) -> str:
        """获取全名"""
        if self.english_name:
            return f"{self.name} ({self.english_name})"
        return self.name
    
    @property
    def is_manager(self) -> bool:
        """检查是否为管理者"""
        return len(self.subordinates) > 0 or len(self.managed_departments) > 0
    
    @property
    def is_probation(self) -> bool:
        """检查是否在试用期"""
        if self.probation_end_date:
            return datetime.utcnow() < self.probation_end_date.replace(tzinfo=None)
        return False
    
    @property
    def years_of_service(self) -> float:
        """计算工龄（年）"""
        if self.hire_date:
            end_date = self.termination_date or datetime.utcnow()
            delta = end_date - self.hire_date.replace(tzinfo=None)
            return round(delta.days / 365.25, 1)
        return 0
    
    def get_all_subordinates(self) -> List['Personnel']:
        """获取所有下属（包括间接下属）"""
        all_subordinates = []
        for subordinate in self.subordinates:
            all_subordinates.append(subordinate)
            all_subordinates.extend(subordinate.get_all_subordinates())
        return all_subordinates
    
    def get_reporting_chain(self) -> List['Personnel']:
        """获取汇报链（向上）"""
        chain = []
        current = self.direct_supervisor
        while current:
            chain.append(current)
            current = current.direct_supervisor
        return chain
    
    def has_skill(self, skill_name: str) -> bool:
        """检查是否具有指定技能"""
        if self.skills:
            return any(skill.get('name') == skill_name for skill in self.skills)
        return False
    
    def get_skill_level(self, skill_name: str) -> Optional[str]:
        """获取指定技能的等级"""
        if self.skills:
            for skill in self.skills:
                if skill.get('name') == skill_name:
                    return skill.get('level')
        return None
    
    def is_available_for_assignment(self) -> bool:
        """检查是否可用于分配任务"""
        return (
            self.is_active and 
            self.employment_status == 'active' and 
            not self.termination_date
        )


class PersonnelHistory(Base):
    """人员变更历史表模型"""
    __tablename__ = "personnel_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    personnel_id = Column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(String(50), nullable=False, index=True)  # hire, promotion, transfer, termination, etc.
    change_date = Column(DateTime(timezone=True), nullable=False, index=True)
    old_values = Column(JSONB)  # 变更前的值
    new_values = Column(JSONB)  # 变更后的值
    reason = Column(Text)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    effective_date = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    personnel = relationship("Personnel")
    approver = relationship("User")
    
    def __repr__(self):
        return f"<PersonnelHistory(id={self.id}, personnel_id={self.personnel_id}, change_type={self.change_type})>"


class WorkLocation(Base):
    """工作地点表模型"""
    __tablename__ = "work_locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False, index=True)
    province = Column(String(50), nullable=False, index=True)
    country = Column(String(50), nullable=False, index=True)
    postal_code = Column(String(20))
    timezone = Column(String(50), nullable=False)
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    capacity = Column(Integer)  # 容纳人数
    facilities = Column(JSONB)  # 设施信息
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<WorkLocation(id={self.id}, name={self.name}, city={self.city})>"
    
    @property
    def full_address(self) -> str:
        """获取完整地址"""
        return f"{self.address}, {self.city}, {self.province}, {self.country}"