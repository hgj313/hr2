"""组织架构相关Pydantic模式定义

本模块定义了部门、职位、人员等组织架构相关的API请求和响应模式。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, validator
from app.schemas.base import BaseSchema, TimestampMixin


# ============================================================================
# 部门相关模式
# ============================================================================

class DepartmentBase(BaseSchema):
    """部门基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="部门名称",
        example="技术部"
    )
    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
        regex="^[A-Z0-9_-]+$",
        description="部门代码",
        example="TECH"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="部门描述",
        example="负责公司技术研发工作"
    )
    manager_id: Optional[int] = Field(
        None,
        description="部门经理ID",
        example=1
    )
    parent_id: Optional[int] = Field(
        None,
        description="上级部门ID",
        example=1
    )
    sort_order: int = Field(
        0,
        ge=0,
        description="排序顺序",
        example=1
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class DepartmentCreate(DepartmentBase):
    """部门创建模式"""
    pass


class DepartmentUpdate(BaseSchema):
    """部门更新模式"""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="部门名称",
        example="技术部"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="部门描述",
        example="负责公司技术研发工作"
    )
    manager_id: Optional[int] = Field(
        None,
        description="部门经理ID",
        example=1
    )
    parent_id: Optional[int] = Field(
        None,
        description="上级部门ID",
        example=1
    )
    sort_order: Optional[int] = Field(
        None,
        ge=0,
        description="排序顺序",
        example=1
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )


class DepartmentResponse(DepartmentBase, TimestampMixin):
    """部门响应模式"""
    id: int = Field(
        ...,
        description="部门ID",
        example=1
    )
    level: int = Field(
        0,
        ge=0,
        description="部门层级",
        example=1
    )
    path: str = Field(
        "",
        description="部门路径",
        example="/1/2/3"
    )
    employee_count: int = Field(
        0,
        ge=0,
        description="员工数量",
        example=10
    )
    manager: Optional['PersonnelResponse'] = Field(
        None,
        description="部门经理信息"
    )
    parent: Optional['DepartmentResponse'] = Field(
        None,
        description="上级部门信息"
    )
    children: Optional[List['DepartmentResponse']] = Field(
        None,
        description="下级部门列表"
    )


# ============================================================================
# 职位相关模式
# ============================================================================

class PositionBase(BaseSchema):
    """职位基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="职位名称",
        example="高级软件工程师"
    )
    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
        regex="^[A-Z0-9_-]+$",
        description="职位代码",
        example="SR_SE"
    )
    level: int = Field(
        1,
        ge=1,
        le=10,
        description="职位等级",
        example=3
    )
    department_id: int = Field(
        ...,
        description="所属部门ID",
        example=1
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="职位描述",
        example="负责软件系统的设计和开发工作"
    )
    requirements: Optional[str] = Field(
        None,
        max_length=2000,
        description="任职要求",
        example="本科以上学历，3年以上开发经验"
    )
    responsibilities: Optional[str] = Field(
        None,
        max_length=2000,
        description="工作职责",
        example="参与系统架构设计，编写高质量代码"
    )
    salary_min: Optional[Decimal] = Field(
        None,
        ge=0,
        description="最低薪资",
        example=10000.00
    )
    salary_max: Optional[Decimal] = Field(
        None,
        ge=0,
        description="最高薪资",
        example=20000.00
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class PositionCreate(PositionBase):
    """职位创建模式"""
    pass


class PositionUpdate(BaseSchema):
    """职位更新模式"""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="职位名称",
        example="高级软件工程师"
    )
    level: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="职位等级",
        example=3
    )
    department_id: Optional[int] = Field(
        None,
        description="所属部门ID",
        example=1
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="职位描述",
        example="负责软件系统的设计和开发工作"
    )
    requirements: Optional[str] = Field(
        None,
        max_length=2000,
        description="任职要求",
        example="本科以上学历，3年以上开发经验"
    )
    responsibilities: Optional[str] = Field(
        None,
        max_length=2000,
        description="工作职责",
        example="参与系统架构设计，编写高质量代码"
    )
    salary_min: Optional[Decimal] = Field(
        None,
        ge=0,
        description="最低薪资",
        example=10000.00
    )
    salary_max: Optional[Decimal] = Field(
        None,
        ge=0,
        description="最高薪资",
        example=20000.00
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )


class PositionResponse(PositionBase, TimestampMixin):
    """职位响应模式"""
    id: int = Field(
        ...,
        description="职位ID",
        example=1
    )
    employee_count: int = Field(
        0,
        ge=0,
        description="在职员工数量",
        example=5
    )
    department: Optional['DepartmentResponse'] = Field(
        None,
        description="所属部门信息"
    )


# ============================================================================
# 工作地点相关模式
# ============================================================================

class WorkLocationBase(BaseSchema):
    """工作地点基础模式"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="地点名称",
        example="北京总部"
    )
    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
        regex="^[A-Z0-9_-]+$",
        description="地点代码",
        example="BJ_HQ"
    )
    address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="详细地址",
        example="北京市朝阳区xxx路xxx号"
    )
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="城市",
        example="北京"
    )
    province: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="省份",
        example="北京市"
    )
    country: str = Field(
        "中国",
        min_length=2,
        max_length=50,
        description="国家",
        example="中国"
    )
    postal_code: Optional[str] = Field(
        None,
        regex="^\d{6}$",
        description="邮政编码",
        example="100000"
    )
    phone: Optional[str] = Field(
        None,
        description="联系电话",
        example="010-12345678"
    )
    is_active: bool = Field(
        True,
        description="是否激活",
        example=True
    )


class WorkLocationCreate(WorkLocationBase):
    """工作地点创建模式"""
    pass


class WorkLocationUpdate(BaseSchema):
    """工作地点更新模式"""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="地点名称",
        example="北京总部"
    )
    address: Optional[str] = Field(
        None,
        min_length=5,
        max_length=200,
        description="详细地址",
        example="北京市朝阳区xxx路xxx号"
    )
    city: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="城市",
        example="北京"
    )
    province: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="省份",
        example="北京市"
    )
    country: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="国家",
        example="中国"
    )
    postal_code: Optional[str] = Field(
        None,
        regex="^\d{6}$",
        description="邮政编码",
        example="100000"
    )
    phone: Optional[str] = Field(
        None,
        description="联系电话",
        example="010-12345678"
    )
    is_active: Optional[bool] = Field(
        None,
        description="是否激活",
        example=True
    )


class WorkLocationResponse(WorkLocationBase, TimestampMixin):
    """工作地点响应模式"""
    id: int = Field(
        ...,
        description="地点ID",
        example=1
    )
    employee_count: int = Field(
        0,
        ge=0,
        description="员工数量",
        example=50
    )


# ============================================================================
# 人员相关模式
# ============================================================================

class PersonnelBase(BaseSchema):
    """人员基础模式"""
    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        regex="^[A-Z0-9_-]+$",
        description="员工编号",
        example="EMP001"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="姓名",
        example="张三"
    )
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        example="zhangsan@example.com"
    )
    phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="手机号码",
        example="13800138000"
    )
    gender: Optional[str] = Field(
        None,
        regex="^(male|female|other)$",
        description="性别",
        example="male"
    )
    birth_date: Optional[date] = Field(
        None,
        description="出生日期",
        example="1990-01-01"
    )
    id_card: Optional[str] = Field(
        None,
        regex="^\d{17}[\dX]$",
        description="身份证号",
        example="110101199001011234"
    )
    department_id: int = Field(
        ...,
        description="所属部门ID",
        example=1
    )
    position_id: int = Field(
        ...,
        description="职位ID",
        example=1
    )
    work_location_id: Optional[int] = Field(
        None,
        description="工作地点ID",
        example=1
    )
    hire_date: date = Field(
        ...,
        description="入职日期",
        example="2024-01-01"
    )
    employment_type: str = Field(
        "full_time",
        regex="^(full_time|part_time|contract|intern)$",
        description="雇佣类型",
        example="full_time"
    )
    status: str = Field(
        "active",
        regex="^(active|inactive|terminated|on_leave)$",
        description="员工状态",
        example="active"
    )
    salary: Optional[Decimal] = Field(
        None,
        ge=0,
        description="薪资",
        example=15000.00
    )
    manager_id: Optional[int] = Field(
        None,
        description="直属上级ID",
        example=1
    )
    avatar: Optional[str] = Field(
        None,
        description="头像URL",
        example="/uploads/avatars/emp_001.jpg"
    )
    emergency_contact: Optional[str] = Field(
        None,
        description="紧急联系人",
        example="李四"
    )
    emergency_phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="紧急联系电话",
        example="13900139000"
    )
    skills: Optional[List[str]] = Field(
        None,
        description="技能列表",
        example=["Python", "JavaScript", "SQL"]
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="备注",
        example="优秀员工，工作认真负责"
    )


class PersonnelCreate(PersonnelBase):
    """人员创建模式"""
    user_id: Optional[int] = Field(
        None,
        description="关联用户ID",
        example=1
    )


class PersonnelUpdate(BaseSchema):
    """人员更新模式"""
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="姓名",
        example="张三"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="邮箱地址",
        example="zhangsan@example.com"
    )
    phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="手机号码",
        example="13800138000"
    )
    gender: Optional[str] = Field(
        None,
        regex="^(male|female|other)$",
        description="性别",
        example="male"
    )
    birth_date: Optional[date] = Field(
        None,
        description="出生日期",
        example="1990-01-01"
    )
    department_id: Optional[int] = Field(
        None,
        description="所属部门ID",
        example=1
    )
    position_id: Optional[int] = Field(
        None,
        description="职位ID",
        example=1
    )
    work_location_id: Optional[int] = Field(
        None,
        description="工作地点ID",
        example=1
    )
    employment_type: Optional[str] = Field(
        None,
        regex="^(full_time|part_time|contract|intern)$",
        description="雇佣类型",
        example="full_time"
    )
    status: Optional[str] = Field(
        None,
        regex="^(active|inactive|terminated|on_leave)$",
        description="员工状态",
        example="active"
    )
    salary: Optional[Decimal] = Field(
        None,
        ge=0,
        description="薪资",
        example=15000.00
    )
    manager_id: Optional[int] = Field(
        None,
        description="直属上级ID",
        example=1
    )
    avatar: Optional[str] = Field(
        None,
        description="头像URL",
        example="/uploads/avatars/emp_001.jpg"
    )
    emergency_contact: Optional[str] = Field(
        None,
        description="紧急联系人",
        example="李四"
    )
    emergency_phone: Optional[str] = Field(
        None,
        regex="^1[3-9]\d{9}$",
        description="紧急联系电话",
        example="13900139000"
    )
    skills: Optional[List[str]] = Field(
        None,
        description="技能列表",
        example=["Python", "JavaScript", "SQL"]
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="备注",
        example="优秀员工，工作认真负责"
    )


class PersonnelResponse(PersonnelBase, TimestampMixin):
    """人员响应模式"""
    id: int = Field(
        ...,
        description="人员ID",
        example=1
    )
    user_id: Optional[int] = Field(
        None,
        description="关联用户ID",
        example=1
    )
    age: Optional[int] = Field(
        None,
        ge=0,
        description="年龄",
        example=30
    )
    work_years: Optional[int] = Field(
        None,
        ge=0,
        description="工作年限",
        example=5
    )
    department: Optional[DepartmentResponse] = Field(
        None,
        description="所属部门信息"
    )
    position: Optional[PositionResponse] = Field(
        None,
        description="职位信息"
    )
    work_location: Optional[WorkLocationResponse] = Field(
        None,
        description="工作地点信息"
    )
    manager: Optional['PersonnelResponse'] = Field(
        None,
        description="直属上级信息"
    )


class PersonnelDetailResponse(PersonnelResponse):
    """人员详细响应模式"""
    subordinates: Optional[List[PersonnelResponse]] = Field(
        None,
        description="下属列表"
    )
    project_count: int = Field(
        0,
        ge=0,
        description="参与项目数量",
        example=3
    )
    current_workload: Optional[Decimal] = Field(
        None,
        ge=0,
        le=100,
        description="当前工作负荷百分比",
        example=75.5
    )
    performance_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=100,
        description="绩效评分",
        example=85.0
    )
    last_promotion_date: Optional[date] = Field(
        None,
        description="最后晋升日期",
        example="2023-06-01"
    )
    contract_end_date: Optional[date] = Field(
        None,
        description="合同到期日期",
        example="2025-12-31"
    )


# ============================================================================
# 人员变更历史相关模式
# ============================================================================

class PersonnelHistoryResponse(BaseSchema, TimestampMixin):
    """人员变更历史响应模式"""
    id: int = Field(
        ...,
        description="历史记录ID",
        example=1
    )
    personnel_id: int = Field(
        ...,
        description="人员ID",
        example=1
    )
    change_type: str = Field(
        ...,
        description="变更类型",
        example="department_change"
    )
    old_value: Optional[str] = Field(
        None,
        description="原值",
        example="技术部"
    )
    new_value: Optional[str] = Field(
        None,
        description="新值",
        example="产品部"
    )
    reason: Optional[str] = Field(
        None,
        description="变更原因",
        example="工作调动"
    )
    effective_date: date = Field(
        ...,
        description="生效日期",
        example="2024-01-01"
    )
    operator_id: int = Field(
        ...,
        description="操作人ID",
        example=1
    )
    personnel: Optional[PersonnelResponse] = Field(
        None,
        description="人员信息"
    )


# 更新前向引用
DepartmentResponse.model_rebuild()
PersonnelResponse.model_rebuild()