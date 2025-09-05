# 人力资源调度系统后端API接口规范

## 1. API设计原则

### 1.1 RESTful标准
- 使用HTTP动词表示操作类型
- 资源导向的URL设计
- 统一的响应格式
- 合适的HTTP状态码

### 1.2 版本控制
- 基础路径: `/api/v1`
- 版本号在URL中体现
- 向后兼容性保证

### 1.3 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "uuid"
}
```

## 2. 用户认证与权限管理API

### 2.1 用户登录
```http
POST /api/v1/auth/login
```

**请求体:**
```json
{
  "username": "string",
  "password": "string",
  "remember_me": false
}
```

**响应:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "username": "string",
      "email": "string",
      "role": "string",
      "permissions": ["string"]
    }
  }
}
```

### 2.2 刷新令牌
```http
POST /api/v1/auth/refresh
```

**请求体:**
```json
{
  "refresh_token": "string"
}
```

### 2.3 用户登出
```http
POST /api/v1/auth/logout
```

### 2.4 获取当前用户信息
```http
GET /api/v1/auth/me
```

## 3. 组织架构管理API

### 3.1 区域管理

#### 3.1.1 获取区域列表
```http
GET /api/v1/regions
```

**查询参数:**
- `page`: 页码 (默认: 1)
- `size`: 每页数量 (默认: 20)
- `search`: 搜索关键词
- `status`: 状态筛选

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "华北区域",
        "code": "HB001",
        "description": "华北区域描述",
        "status": "active",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "size": 20,
    "pages": 5
  }
}
```

#### 3.1.2 创建区域
```http
POST /api/v1/regions
```

**请求体:**
```json
{
  "name": "华北区域",
  "code": "HB001",
  "description": "华北区域描述",
  "status": "active"
}
```

#### 3.1.3 更新区域信息
```http
PUT /api/v1/regions/{region_id}
```

#### 3.1.4 删除区域
```http
DELETE /api/v1/regions/{region_id}
```

#### 3.1.5 获取区域详情
```http
GET /api/v1/regions/{region_id}
```

### 3.2 部门管理

#### 3.2.1 获取组织架构树
```http
GET /api/v1/departments/tree
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": "uuid",
      "name": "技术部",
      "code": "TECH001",
      "parent_id": null,
      "level": 1,
      "children": [
        {
          "id": "uuid",
          "name": "前端开发组",
          "code": "TECH001-FE",
          "parent_id": "parent_uuid",
          "level": 2,
          "children": []
        }
      ]
    }
  ]
}
```

#### 3.2.2 创建部门
```http
POST /api/v1/departments
```

**请求体:**
```json
{
  "name": "技术部",
  "code": "TECH001",
  "parent_id": "uuid",
  "description": "技术部门",
  "manager_id": "uuid",
  "region_id": "uuid"
}
```

#### 3.2.3 更新部门
```http
PUT /api/v1/departments/{department_id}
```

#### 3.2.4 删除部门
```http
DELETE /api/v1/departments/{department_id}
```

#### 3.2.5 获取部门人员列表
```http
GET /api/v1/departments/{department_id}/personnel
```

## 4. 人员信息管理API

### 4.1 人员档案管理

#### 4.1.1 获取人员档案列表
```http
GET /api/v1/personnel
```

**查询参数:**
- `page`: 页码
- `size`: 每页数量
- `search`: 搜索关键词
- `department_id`: 部门ID
- `region_id`: 区域ID
- `status`: 状态筛选
- `skill`: 技能筛选

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "employee_id": "EMP001",
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "department": {
          "id": "uuid",
          "name": "技术部"
        },
        "position": "高级工程师",
        "status": "active",
        "hire_date": "2023-01-15",
        "skills": [
          {
            "id": "uuid",
            "name": "Python",
            "level": "expert"
          }
        ]
      }
    ],
    "total": 100,
    "page": 1,
    "size": 20,
    "pages": 5
  }
}
```

#### 4.1.2 创建人员档案
```http
POST /api/v1/personnel
```

**请求体:**
```json
{
  "employee_id": "EMP001",
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "department_id": "uuid",
  "position": "高级工程师",
  "hire_date": "2023-01-15",
  "status": "active",
  "personal_info": {
    "gender": "male",
    "birth_date": "1990-01-01",
    "education": "本科",
    "address": "北京市朝阳区"
  }
}
```

#### 4.1.3 更新人员档案
```http
PUT /api/v1/personnel/{personnel_id}
```

#### 4.1.4 获取人员详情
```http
GET /api/v1/personnel/{personnel_id}
```

#### 4.1.5 删除人员档案
```http
DELETE /api/v1/personnel/{personnel_id}
```

### 4.2 技能管理

#### 4.2.1 获取人员技能
```http
GET /api/v1/personnel/{personnel_id}/skills
```

#### 4.2.2 添加人员技能
```http
POST /api/v1/personnel/{personnel_id}/skills
```

**请求体:**
```json
{
  "skill_name": "Python",
  "level": "expert",
  "years_experience": 5,
  "certification": "Python认证",
  "description": "精通Python开发"
}
```

#### 4.2.3 更新人员技能
```http
PUT /api/v1/personnel/{personnel_id}/skills/{skill_id}
```

#### 4.2.4 删除人员技能
```http
DELETE /api/v1/personnel/{personnel_id}/skills/{skill_id}
```

### 4.3 人员状态管理

#### 4.3.1 获取人员状态
```http
GET /api/v1/personnel/{personnel_id}/status
```

#### 4.3.2 更新人员状态
```http
PUT /api/v1/personnel/{personnel_id}/status
```

**请求体:**
```json
{
  "status": "active",
  "availability": "available",
  "current_project_id": "uuid",
  "notes": "状态备注"
}
```

## 5. 项目管理API

### 5.1 项目基础管理

#### 5.1.1 获取项目列表
```http
GET /api/v1/projects
```

**查询参数:**
- `page`: 页码
- `size`: 每页数量
- `search`: 搜索关键词
- `status`: 状态筛选
- `region_id`: 区域ID
- `start_date`: 开始日期
- `end_date`: 结束日期

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "项目A",
        "code": "PROJ001",
        "description": "项目描述",
        "status": "active",
        "priority": "high",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "budget": 1000000,
        "region": {
          "id": "uuid",
          "name": "华北区域"
        },
        "manager": {
          "id": "uuid",
          "name": "项目经理"
        },
        "team_size": 10,
        "progress": 65.5
      }
    ],
    "total": 50,
    "page": 1,
    "size": 20,
    "pages": 3
  }
}
```

#### 5.1.2 创建项目
```http
POST /api/v1/projects
```

**请求体:**
```json
{
  "name": "项目A",
  "code": "PROJ001",
  "description": "项目描述",
  "priority": "high",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "budget": 1000000,
  "region_id": "uuid",
  "manager_id": "uuid",
  "requirements": {
    "skills_required": ["Python", "React"],
    "team_size": 10,
    "duration_months": 12
  }
}
```

#### 5.1.3 更新项目
```http
PUT /api/v1/projects/{project_id}
```

#### 5.1.4 获取项目详情
```http
GET /api/v1/projects/{project_id}
```

#### 5.1.5 删除项目
```http
DELETE /api/v1/projects/{project_id}
```

### 5.2 项目人员配置

#### 5.2.1 获取项目人员列表
```http
GET /api/v1/projects/{project_id}/personnel
```

#### 5.2.2 添加项目人员
```http
POST /api/v1/projects/{project_id}/personnel
```

**请求体:**
```json
{
  "personnel_id": "uuid",
  "role": "开发工程师",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "allocation_percentage": 100,
  "hourly_rate": 200
}
```

#### 5.2.3 移除项目人员
```http
DELETE /api/v1/projects/{project_id}/personnel/{personnel_id}
```

## 6. 智能调度管理API

### 6.1 智能匹配

#### 6.1.1 人员匹配推荐
```http
POST /api/v1/scheduling/match-personnel
```

**请求体:**
```json
{
  "project_id": "uuid",
  "requirements": {
    "skills": ["Python", "React"],
    "experience_years": 3,
    "availability_start": "2024-01-01",
    "availability_end": "2024-12-31",
    "region_id": "uuid",
    "budget_range": {
      "min": 150,
      "max": 300
    }
  },
  "preferences": {
    "prioritize_experience": true,
    "prioritize_availability": false,
    "prioritize_cost": false
  }
}
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "matches": [
      {
        "personnel": {
          "id": "uuid",
          "name": "张三",
          "position": "高级工程师"
        },
        "match_score": 95.5,
        "match_details": {
          "skill_match": 90,
          "experience_match": 95,
          "availability_match": 100,
          "cost_match": 85
        },
        "availability": {
          "start_date": "2024-01-01",
          "end_date": "2024-12-31",
          "allocation_percentage": 80
        },
        "estimated_cost": 200
      }
    ],
    "total_matches": 15,
    "search_criteria": {}
  }
}
```

### 6.2 调度计划管理

#### 6.2.1 创建调度计划
```http
POST /api/v1/scheduling/plans
```

**请求体:**
```json
{
  "name": "Q1调度计划",
  "description": "第一季度人员调度计划",
  "start_date": "2024-01-01",
  "end_date": "2024-03-31",
  "assignments": [
    {
      "personnel_id": "uuid",
      "project_id": "uuid",
      "role": "开发工程师",
      "start_date": "2024-01-01",
      "end_date": "2024-03-31",
      "allocation_percentage": 100
    }
  ]
}
```

#### 6.2.2 获取调度计划列表
```http
GET /api/v1/scheduling/plans
```

#### 6.2.3 更新调度计划
```http
PUT /api/v1/scheduling/plans/{plan_id}
```

#### 6.2.4 执行调度计划
```http
POST /api/v1/scheduling/plans/{plan_id}/execute
```

### 6.3 冲突检测

#### 6.3.1 检测调度冲突
```http
POST /api/v1/scheduling/conflict-detection
```

**请求体:**
```json
{
  "assignments": [
    {
      "personnel_id": "uuid",
      "project_id": "uuid",
      "start_date": "2024-01-01",
      "end_date": "2024-03-31",
      "allocation_percentage": 100
    }
  ]
}
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "has_conflicts": true,
    "conflicts": [
      {
        "type": "time_overlap",
        "severity": "high",
        "description": "人员张三在同一时间段被分配到多个项目",
        "affected_assignments": [
          {
            "personnel_id": "uuid",
            "project_id": "uuid",
            "conflict_period": {
              "start": "2024-01-01",
              "end": "2024-02-15"
            }
          }
        ],
        "suggestions": [
          "调整项目时间安排",
          "降低人员分配比例",
          "寻找替代人员"
        ]
      }
    ]
  }
}
```

## 7. 审批流程API

### 7.1 审批流程管理

#### 7.1.1 创建审批申请
```http
POST /api/v1/approvals
```

**请求体:**
```json
{
  "type": "scheduling_approval",
  "title": "Q1人员调度申请",
  "description": "申请调度张三到项目A",
  "data": {
    "personnel_id": "uuid",
    "project_id": "uuid",
    "start_date": "2024-01-01",
    "end_date": "2024-03-31"
  },
  "approvers": ["uuid1", "uuid2"],
  "priority": "normal"
}
```

#### 7.1.2 获取审批列表
```http
GET /api/v1/approvals
```

**查询参数:**
- `status`: 审批状态 (pending, approved, rejected)
- `type`: 审批类型
- `applicant_id`: 申请人ID
- `approver_id`: 审批人ID

#### 7.1.3 审批处理
```http
POST /api/v1/approvals/{approval_id}/process
```

**请求体:**
```json
{
  "action": "approve",
  "comment": "审批通过",
  "conditions": {
    "budget_limit": 50000,
    "duration_limit": "3 months"
  }
}
```

## 8. 风险管控与预警API

### 8.1 风险识别

#### 8.1.1 风险模式识别
```http
POST /api/v1/risk/pattern-recognition
```

**请求体:**
```json
{
  "analysis_period": {
    "start_date": "2024-01-01",
    "end_date": "2024-03-31"
  },
  "scope": {
    "regions": ["uuid1", "uuid2"],
    "departments": ["uuid1", "uuid2"],
    "projects": ["uuid1", "uuid2"]
  },
  "risk_types": ["resource_shortage", "skill_mismatch", "budget_overrun"]
}
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "identified_risks": [
      {
        "id": "uuid",
        "type": "resource_shortage",
        "severity": "high",
        "probability": 0.85,
        "impact_score": 8.5,
        "description": "项目A在Q2可能面临Python开发人员短缺",
        "affected_entities": {
          "projects": ["uuid1"],
          "departments": ["uuid1"],
          "personnel": ["uuid1", "uuid2"]
        },
        "predicted_timeline": {
          "earliest_occurrence": "2024-04-01",
          "peak_impact": "2024-05-15"
        },
        "mitigation_suggestions": [
          "提前招聘Python开发人员",
          "安排现有人员技能培训",
          "考虑外包部分开发工作"
        ]
      }
    ],
    "risk_summary": {
      "total_risks": 5,
      "high_severity": 2,
      "medium_severity": 2,
      "low_severity": 1
    }
  }
}
```

### 8.2 实时监控

#### 8.2.1 风险监控仪表板
```http
GET /api/v1/risk/dashboard
```

**查询参数:**
- `region_id`: 区域ID
- `department_id`: 部门ID
- `time_range`: 时间范围 (1d, 7d, 30d, 90d)

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "overview": {
      "total_active_risks": 12,
      "high_priority_risks": 3,
      "new_risks_today": 2,
      "resolved_risks_today": 1
    },
    "risk_trends": [
      {
        "date": "2024-01-15",
        "total_risks": 10,
        "high_severity": 2,
        "medium_severity": 5,
        "low_severity": 3
      }
    ],
    "top_risks": [
      {
        "id": "uuid",
        "type": "resource_shortage",
        "severity": "high",
        "description": "关键技能人员短缺",
        "impact_score": 9.2
      }
    ],
    "risk_distribution": {
      "by_type": {
        "resource_shortage": 5,
        "skill_mismatch": 3,
        "budget_overrun": 2,
        "timeline_delay": 2
      },
      "by_region": {
        "华北区域": 6,
        "华南区域": 4,
        "华东区域": 2
      }
    }
  }
}
```

### 8.3 预警管理

#### 8.3.1 创建预警规则
```http
POST /api/v1/risk/alert-rules
```

**请求体:**
```json
{
  "name": "人员利用率预警",
  "description": "当人员利用率超过90%时触发预警",
  "conditions": {
    "metric": "personnel_utilization",
    "operator": "greater_than",
    "threshold": 0.9,
    "duration": "1h"
  },
  "scope": {
    "regions": ["uuid1"],
    "departments": ["uuid1"]
  },
  "notification": {
    "channels": ["email", "sms"],
    "recipients": ["uuid1", "uuid2"],
    "template": "high_utilization_alert"
  },
  "severity": "medium",
  "enabled": true
}
```

#### 8.3.2 触发应急响应
```http
POST /api/v1/risk/emergency-response
```

**请求体:**
```json
{
  "risk_id": "uuid",
  "response_type": "immediate",
  "actions": [
    {
      "type": "resource_reallocation",
      "description": "紧急调配人员",
      "parameters": {
        "source_project": "uuid1",
        "target_project": "uuid2",
        "personnel_ids": ["uuid1", "uuid2"]
      }
    }
  ],
  "notification": {
    "notify_stakeholders": true,
    "escalation_level": "high"
  }
}
```

## 9. 数据分析与报表API

### 9.1 调度分析

#### 9.1.1 资源利用率分析
```http
GET /api/v1/analytics/resource-utilization
```

**查询参数:**
- `start_date`: 开始日期
- `end_date`: 结束日期
- `region_id`: 区域ID
- `department_id`: 部门ID
- `granularity`: 粒度 (daily, weekly, monthly)

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "summary": {
      "average_utilization": 78.5,
      "peak_utilization": 95.2,
      "low_utilization": 45.3,
      "total_personnel": 150,
      "active_personnel": 142
    },
    "trends": [
      {
        "date": "2024-01-15",
        "utilization_rate": 78.5,
        "available_hours": 1200,
        "allocated_hours": 942
      }
    ],
    "by_department": [
      {
        "department_id": "uuid",
        "department_name": "技术部",
        "utilization_rate": 85.2,
        "personnel_count": 50
      }
    ],
    "by_skill": [
      {
        "skill_name": "Python",
        "utilization_rate": 92.1,
        "demand_hours": 800,
        "supply_hours": 870
      }
    ]
  }
}
```

### 9.2 项目分析

#### 9.2.1 项目调度效率分析
```http
GET /api/v1/analytics/project-efficiency
```

### 9.3 自定义报表

#### 9.3.1 生成自定义报表
```http
POST /api/v1/reports/generate
```

**请求体:**
```json
{
  "name": "月度调度报表",
  "type": "scheduling_summary",
  "parameters": {
    "period": "monthly",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "regions": ["uuid1", "uuid2"],
    "include_charts": true,
    "format": "pdf"
  },
  "schedule": {
    "frequency": "monthly",
    "day_of_month": 1,
    "recipients": ["uuid1", "uuid2"]
  }
}
```

## 10. 系统管理API

### 10.1 系统配置

#### 10.1.1 获取系统配置
```http
GET /api/v1/system/config
```

#### 10.1.2 更新系统配置
```http
PUT /api/v1/system/config
```

### 10.2 数据管理

#### 10.2.1 数据备份
```http
POST /api/v1/system/backup
```

#### 10.2.2 数据恢复
```http
POST /api/v1/system/restore
```

### 10.3 系统监控

#### 10.3.1 系统健康检查
```http
GET /api/v1/system/health
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "services": {
      "database": {
        "status": "healthy",
        "response_time": 15,
        "connections": 25
      },
      "redis": {
        "status": "healthy",
        "response_time": 2,
        "memory_usage": "45%"
      },
      "external_apis": {
        "status": "healthy",
        "response_time": 120
      }
    },
    "metrics": {
      "cpu_usage": "35%",
      "memory_usage": "68%",
      "disk_usage": "42%",
      "active_connections": 156
    }
  }
}
```

## 11. 错误码规范

### 11.1 HTTP状态码
- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权
- `403`: 禁止访问
- `404`: 资源不存在
- `409`: 资源冲突
- `422`: 数据验证失败
- `500`: 服务器内部错误

### 11.2 业务错误码
- `10001`: 用户名或密码错误
- `10002`: 用户已被禁用
- `10003`: 令牌已过期
- `20001`: 人员不存在
- `20002`: 人员已被分配
- `30001`: 项目不存在
- `30002`: 项目已结束
- `40001`: 调度冲突
- `40002`: 资源不足
- `50001`: 审批流程错误
- `60001`: 权限不足

## 12. 接口安全规范

### 12.1 认证机制
- JWT Bearer Token认证
- Token过期时间: 1小时
- 刷新Token有效期: 7天
- 支持Token黑名单机制

### 12.2 权限控制
- 基于角色的访问控制(RBAC)
- 细粒度权限管理
- 资源级别权限控制
- 操作审计日志

### 12.3 数据安全
- 敏感数据加密传输
- 请求参数验证
- SQL注入防护
- XSS攻击防护

### 12.4 接口限流
- 基于用户的请求频率限制
- 基于IP的请求频率限制
- 重要接口特殊限制
- 超限处理机制

---

**注意事项:**
1. 所有接口都需要进行身份验证(除登录接口外)
2. 请求和响应数据都使用JSON格式
3. 时间格式统一使用ISO 8601标准
4. 分页参数统一使用page和size
5. 所有接口都需要记录操作日志
6. 敏感操作需要二次确认
7. 批量操作需要限制数量
8. 长时间操作需要异步处理

**开发优先级:**
1. 用户认证与权限管理 (高)
2. 组织架构管理 (高)
3. 人员信息管理 (高)
4. 项目管理 (高)
5. 智能调度管理 (高)
6. 审批流程 (中)
7. 风险管控与预警 (中)
8. 数据分析与报表 (中)
9. 系统管理 (低)