# API接口设计文档

## 文档概述

本文档详细描述了人力资源调度系统的API接口设计，包括接口规范、认证机制、核心接口定义和错误处理机制。

## 1. API设计原则

### 1.1 RESTful设计风格
- 使用HTTP动词表示操作类型（GET、POST、PUT、DELETE、PATCH）
- 使用名词表示资源
- 使用HTTP状态码表示操作结果
- 统一的URL结构和命名规范

### 1.2 接口规范
- **基础URL**：`https://api.hrscheduling.com/v1`
- **认证方式**：JWT Token + OAuth 2.0
- **数据格式**：JSON
- **字符编码**：UTF-8
- **版本控制**：URL路径版本控制（/v1、/v2）

## 2. 通用响应格式

### 2.1 成功响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "uuid"
}
```

### 2.2 分页响应格式
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "size": 20,
    "pages": 5
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "uuid"
}
```

### 2.3 错误响应格式
```json
{
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "type": "ValidationError",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      }
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "uuid"
}
```

## 3. 核心API接口

### 3.1 认证授权接口

#### 用户登录
```
POST /api/v1/auth/login
```
**请求体：**
```json
{
  "username": "string",
  "password": "string",
  "remember_me": "boolean"
}
```
**响应：**
```json
{
  "code": 200,
  "data": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "expires_in": 3600,
    "user_info": {
      "id": "string",
      "username": "string",
      "email": "string",
      "roles": ["string"]
    }
  }
}
```

#### Token刷新
```
POST /api/v1/auth/refresh
```

#### 用户登出
```
POST /api/v1/auth/logout
```

### 3.2 人员管理接口

#### 获取人员列表
```
GET /api/v1/personnel?page=1&size=20&search=keyword&department=dept_id
```

#### 创建人员
```
POST /api/v1/personnel
```
**请求体：**
```json
{
  "name": "string",
  "employee_id": "string",
  "email": "string",
  "phone": "string",
  "department_id": "string",
  "position": "string",
  "skills": [
    {
      "skill_type": "string",
      "skill_level": "string",
      "certification": "string"
    }
  ],
  "availability": {
    "work_days": ["monday", "tuesday"],
    "work_hours": {
      "start": "09:00",
      "end": "18:00"
    }
  }
}
```

#### 更新人员信息
```
PUT /api/v1/personnel/{personnel_id}
```

#### 删除人员
```
DELETE /api/v1/personnel/{personnel_id}
```

#### 获取人员技能
```
GET /api/v1/personnel/{personnel_id}/skills
```

### 3.3 项目管理接口

#### 获取项目列表
```
GET /api/v1/projects?page=1&size=20&status=active&search=keyword
```

#### 创建项目
```
POST /api/v1/projects
```
**请求体：**
```json
{
  "name": "string",
  "description": "string",
  "client_id": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "location": "string",
  "requirements": {
    "personnel_count": 10,
    "skill_requirements": [
      {
        "skill_type": "string",
        "skill_level": "string",
        "required_count": 2
      }
    ],
    "work_schedule": {
      "work_days": ["monday", "tuesday"],
      "work_hours": {
        "start": "08:00",
        "end": "17:00"
      }
    }
  }
}
```

#### 更新项目
```
PUT /api/v1/projects/{project_id}
```

#### 获取项目人员
```
GET /api/v1/projects/{project_id}/personnel
```

#### 分配人员到项目
```
POST /api/v1/projects/{project_id}/personnel
```

### 3.4 智能调度接口

#### 获取调度列表
```
GET /api/v1/schedules?page=1&size=20&project_id=id&status=pending
```

#### 创建调度申请
```
POST /api/v1/schedules
```
**请求体：**
```json
{
  "project_id": "string",
  "personnel_id": "string",
  "schedule_date": "2024-01-01",
  "work_hours": {
    "start": "08:00",
    "end": "17:00"
  },
  "role": "string",
  "notes": "string"
}
```

#### AI智能匹配
```
POST /api/v1/schedules/ai-match
```
**请求体：**
```json
{
  "project_id": "string",
  "requirements": {
    "skill_types": ["string"],
    "skill_levels": ["string"],
    "personnel_count": 5,
    "work_location": "string",
    "time_range": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-31"
    }
  },
  "preferences": {
    "priority_factors": ["skill_match", "availability", "location"],
    "exclude_personnel": ["string"]
  }
}
```

#### 冲突检测
```
GET /api/v1/schedules/conflicts?personnel_id=id&date_range=2024-01-01,2024-01-31
```

#### 调度优化建议
```
GET /api/v1/schedules/optimization-suggestions?project_id=id
```

### 3.5 风险管控接口

#### 获取风险监控数据
```
GET /api/v1/risk/monitoring?type=all&time_range=7d
```

#### 风险识别分析
```
POST /api/v1/risk/identification
```
**请求体：**
```json
{
  "analysis_type": "schedule_risk",
  "target_id": "string",
  "parameters": {
    "time_range": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-31"
    },
    "risk_factors": ["personnel_shortage", "skill_mismatch"]
  }
}
```

#### 获取风险预警
```
GET /api/v1/risk/alerts?status=active&severity=high
```

#### 应急响应处理
```
POST /api/v1/risk/emergency-response
```

### 3.6 数据分析接口

#### 资源配置评估
```
GET /api/v1/analytics/configuration-assessment?project_id=id&time_range=30d
```

#### 预测分析
```
POST /api/v1/analytics/prediction
```
**请求体：**
```json
{
  "prediction_type": "resource_demand",
  "time_horizon": "30d",
  "parameters": {
    "historical_data_range": "90d",
    "factors": ["seasonal", "project_type", "skill_demand"]
  }
}
```

#### 决策支持数据
```
GET /api/v1/analytics/decision-support?analysis_type=resource_optimization
```

## 4. 认证和授权

### 4.1 JWT Token认证
- **Token类型**：Bearer Token
- **Token有效期**：Access Token 1小时，Refresh Token 7天
- **Token刷新**：自动刷新机制
- **Token存储**：Redis缓存

### 4.2 权限控制
- **权限模型**：RBAC（基于角色的访问控制）
- **权限粒度**：接口级别 + 数据级别
- **权限验证**：装饰器 + 中间件
- **权限缓存**：Redis缓存权限信息

### 4.3 安全机制
- **请求签名**：关键接口使用HMAC签名
- **频率限制**：API调用频率限制
- **IP白名单**：敏感接口IP访问控制
- **审计日志**：所有API调用记录审计日志

## 5. 错误处理

### 5.1 HTTP状态码
- **200 OK**：请求成功
- **201 Created**：资源创建成功
- **400 Bad Request**：请求参数错误
- **401 Unauthorized**：未授权访问
- **403 Forbidden**：权限不足
- **404 Not Found**：资源不存在
- **409 Conflict**：资源冲突
- **422 Unprocessable Entity**：数据验证失败
- **429 Too Many Requests**：请求频率超限
- **500 Internal Server Error**：服务器内部错误

### 5.2 错误码定义
```python
class ErrorCode:
    # 通用错误码
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    
    # 业务错误码
    PERSONNEL_NOT_FOUND = 1001
    PROJECT_NOT_FOUND = 1002
    SCHEDULE_CONFLICT = 1003
    SKILL_MISMATCH = 1004
    AI_SERVICE_ERROR = 1005
    RISK_THRESHOLD_EXCEEDED = 1006
```

## 6. 接口测试

### 6.1 测试环境
- **测试环境URL**：`https://test-api.hrscheduling.com/v1`
- **测试账号**：提供测试用户账号和权限
- **测试数据**：预置测试数据集

### 6.2 API文档
- **Swagger文档**：`/docs`
- **ReDoc文档**：`/redoc`
- **OpenAPI规范**：`/openapi.json`

### 6.3 性能指标
- **响应时间**：95%的请求响应时间 < 200ms
- **并发处理**：支持1000+并发请求
- **可用性**：99.9%服务可用性

---

本文档涵盖了人力资源调度系统的完整API接口设计，为前端开发和第三方系统集成提供了详细的接口规范和使用指南。