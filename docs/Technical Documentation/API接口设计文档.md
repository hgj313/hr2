# 人力资源调度系统API接口设计文档

## 文档概述

本文档详细定义了人力资源调度系统的RESTful API接口规范，包括接口路径、请求方法、参数定义、响应格式等完整的API设计。

## 系统概述

**API版本**：v1.0  
**基础URL**：`https://api.hrscheduling.com/v1`  
**认证方式**：JWT Token + OAuth 2.0  
**数据格式**：JSON  
**字符编码**：UTF-8  
**系统特色**：
- 专注智能化资源调度，不包含考勤功能
- 预留ERP系统集成接口
- 支持现代化可视化交互
- 模块化架构设计，支持系统扩展

## 系统功能边界

### 核心功能范围
本系统专注于人力资源调度管理的核心功能：
- **调度时长设置**：为调度决策提供时间规划依据
- **时间规划**：合理安排人员在项目中的时间分配
- **冲突解决**：识别和解决时间冲突、资源冲突
- **资源优化**：基于调度需求进行人员配置优化

### 明确排除的功能
以下功能明确不在本系统范围内：
- **绩效管理**：员工绩效考核、评价、奖惩等
- **考勤打卡**：上下班打卡、考勤统计等
- **工时统计**：实际工作时间记录和统计
- **薪资计算**：工资核算、奖金分配等

**重要说明**：系统中所有时间相关数据（调度时长、时间规划等）仅服务于调度系统的核心功能，不用于考勤、工时统计或薪资计算等用途。

## API设计原则

### 1. RESTful设计风格
- 使用HTTP动词表示操作类型（GET、POST、PUT、DELETE、PATCH）
- 使用名词表示资源
- 使用HTTP状态码表示操作结果
- 统一的URL结构和命名规范

### 2. FastAPI框架特性
- 自动生成OpenAPI文档
- 数据验证和序列化
- 异步支持
- 依赖注入系统
- 类型提示支持

### 3. 通用响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "uuid"
}
```

### 4. 分页响应格式
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

## 1. 智能化资源调度管理API

### 1.1 AI智能匹配引擎

#### 智能人员匹配
```
POST /api/v1/scheduling/ai-match
```
**请求体**：
```json
{
  "project_id": "string",
  "requirements": {
    "skill_types": ["string"],
    "skill_levels": ["string"],
    "personnel_count": "number",
    "work_location": "string",
    "time_range": {
      "start_date": "string",
      "end_date": "string"
    },
    "budget_limit": "number",
    "priority": "high|medium|low"
  },
  "preferences": {
    "cost_weight": "number",
    "skill_weight": "number",
    "location_weight": "number",
    "experience_weight": "number"
  }
}
```
**响应**：
```json
{
  "code": 200,
  "message": "AI匹配完成",
  "data": {
    "match_id": "string",
    "recommendations": [
      {
        "personnel_id": "string",
        "match_score": "number",
        "match_details": {
          "skill_match": "number",
          "experience_match": "number",
          "location_match": "number",
          "cost_efficiency": "number"
        },
        "advantages": ["string"],
        "risks": ["string"]
      }
    ],
    "optimal_solution": {
      "total_cost": "number",
      "expected_roi": "number",
      "risk_level": "low|medium|high",
      "implementation_plan": ["string"]
    }
  }
}
```

#### 可视化调度界面数据
```
GET /api/v1/scheduling/visualization-data
```
**查询参数**：
- `view_type`: 视图类型（gantt|kanban|timeline）
- `date_range`: 日期范围
- `filters`: 过滤条件（department,project,skill）

**响应**：
```json
{
  "code": 200,
  "message": "可视化数据获取成功",
  "data": {
    "view_type": "gantt",
    "time_range": {
      "start_date": "string",
      "end_date": "string"
    },
    "personnel": [
      {
        "personnel_id": "string",
        "name": "string",
        "status": "available|busy|leave",
        "current_project": "string",
        "utilization": "number",
        "location": {
          "lat": "number",
          "lng": "number",
          "address": "string"
        }
      }
    ],
    "projects": [
      {
        "project_id": "string",
        "name": "string",
        "progress": "number",
        "milestones": [
          {
            "date": "string",
            "description": "string",
            "status": "completed|pending|delayed"
          }
        ]
      }
    ],
    "resource_flow": [
      {
        "from_project": "string",
        "to_project": "string",
        "personnel_count": "number",
        "transfer_date": "string",
        "reason": "string"
      }
    ]
  }
}
```

#### 拖拽式调度操作
```
POST /api/v1/scheduling/drag-assign
```
**请求体**：
```json
{
  "operation": "assign|reassign|remove",
  "personnel_id": "string",
  "source_project": "string",
  "target_project": "string",
  "time_slot": {
    "start_date": "string",
    "end_date": "string"
  },
  "conflict_resolution": "auto|manual",
  "reason": "string"
}
```
**响应**：
```json
{
  "code": 200,
  "message": "调度操作成功",
  "data": {
    "operation_id": "string",
    "result": "success|conflict|failed",
    "conflicts": [
      {
        "type": "time|skill|location",
        "description": "string",
        "suggestions": ["string"]
      }
    ],
    "impact_analysis": {
      "affected_projects": ["string"],
      "cost_impact": "number",
      "timeline_impact": "string"
    },
    "rollback_info": {
      "can_rollback": "boolean",
      "rollback_deadline": "string"
    }
  }
}
```

### 1.2 风险管控与预警

#### 风险评估
```
POST /api/v1/scheduling/risk-assessment
```
**请求体**：
```json
{
  "assessment_type": "project|personnel|resource",
  "target_id": "string",
  "time_horizon": "1w|1m|3m|6m",
  "risk_factors": ["cost|schedule|quality|resource"]
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "overall_risk_level": "low|medium|high|critical",
    "risk_details": [
      {
        "risk_type": "string",
        "probability": "number",
        "impact": "number",
        "risk_score": "number",
        "description": "string",
        "mitigation_strategies": ["string"]
      }
    ],
    "early_warnings": [
      {
        "warning_type": "string",
        "severity": "low|medium|high",
        "trigger_date": "string",
        "recommended_actions": ["string"]
      }
    ]
  }
}
```

## 2. 全流程资源风险管控 API

### 2.1 智能风险识别

#### 风险模式识别
```
POST /api/v1/risk/pattern-recognition
```
**请求体**：
```json
{
  "analysis_scope": "project|personnel|department|global",
  "target_ids": ["string"],
  "time_range": {
    "start_date": "string",
    "end_date": "string"
  },
  "risk_categories": ["cost|schedule|quality|resource|safety"],
  "ai_model_version": "string"
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "analysis_id": "string",
    "identified_patterns": [
      {
        "pattern_id": "string",
        "pattern_type": "string",
        "confidence_level": "number",
        "description": "string",
        "historical_occurrences": "number",
        "potential_impact": "low|medium|high|critical"
      }
    ],
    "risk_predictions": [
      {
        "risk_type": "string",
        "probability": "number",
        "expected_impact": "number",
        "timeline": "string",
        "prevention_strategies": ["string"]
      }
    ]
  }
}
```

### 2.2 实时风险监控

#### 风险监控仪表板
```
GET /api/v1/risk/dashboard
```
**查询参数**：
- `scope`: 监控范围（global|region|department|project）
- `risk_level`: 风险等级过滤（low|medium|high|critical）
- `real_time`: 是否实时数据（true|false）

**响应**：
```json
{
  "code": 200,
  "data": {
    "overall_risk_status": "green|yellow|orange|red",
    "active_alerts": [
      {
        "alert_id": "string",
        "alert_type": "cost_overrun|schedule_delay|resource_shortage",
        "severity": "low|medium|high|critical",
        "affected_projects": ["string"],
        "trigger_time": "string",
        "current_status": "new|acknowledged|in_progress|resolved",
        "recommended_actions": ["string"]
      }
    ],
    "risk_trends": {
      "cost_risk_trend": ["number"],
      "schedule_risk_trend": ["number"],
      "resource_risk_trend": ["number"],
      "quality_risk_trend": ["number"]
    },
    "key_metrics": {
      "total_projects_at_risk": "number",
      "average_risk_score": "number",
      "risk_mitigation_success_rate": "number"
    }
  }
}
```

### 2.3 风险预警与响应

#### 创建风险预警规则
```
POST /api/v1/risk/alert-rules
```
**请求体**：
```json
{
  "rule_name": "string",
  "rule_type": "threshold|pattern|anomaly",
  "scope": {
    "target_type": "project|personnel|department",
    "target_ids": ["string"]
  },
  "conditions": {
    "metric_type": "cost|schedule|resource|quality",
    "threshold_value": "number",
    "comparison_operator": "gt|lt|eq|gte|lte",
    "time_window": "1h|1d|1w|1m"
  },
  "alert_settings": {
    "severity": "low|medium|high|critical",
    "notification_channels": ["email|sms|push|webhook"],
    "recipients": ["string"],
    "escalation_rules": [
      {
        "delay_minutes": "number",
        "escalate_to": ["string"]
      }
    ]
  }
}
```

#### 触发应急响应
```
POST /api/v1/risk/emergency-response
```
**请求体**：
```json
{
  "incident_type": "critical_resource_shortage|major_schedule_delay|safety_incident",
  "affected_scope": {
    "projects": ["string"],
    "personnel": ["string"],
    "departments": ["string"]
  },
  "severity_level": "1|2|3|4|5",
  "description": "string",
  "immediate_actions_taken": ["string"],
  "response_team": ["string"],
  "estimated_resolution_time": "string"
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "response_id": "string",
    "response_plan": {
      "immediate_actions": ["string"],
      "short_term_actions": ["string"],
      "long_term_actions": ["string"]
    },
    "resource_allocation": {
      "emergency_team": ["string"],
      "backup_resources": ["string"],
      "budget_authorization": "number"
    },
    "communication_plan": {
      "stakeholders_to_notify": ["string"],
      "communication_channels": ["string"],
      "update_frequency": "string"
    }
  }
}
```

## 3. 组织架构管理API

### 3.1 区域管理

#### 获取区域列表
```
GET /api/v1/regions
```
**查询参数**：
- `page`: 页码（默认1）
- `size`: 每页数量（默认20）
- `keyword`: 搜索关键词

#### 创建区域
```
POST /api/v1/regions
```
**请求体**：
```json
{
  "region_name": "string",
  "region_code": "string",
  "manager_id": "string",
  "description": "string",
  "location": {
    "province": "string",
    "city": "string",
    "address": "string"
  }
}
```

#### 更新区域信息
```
PUT /api/v1/regions/{region_id}
```

#### 删除区域
```
DELETE /api/v1/regions/{region_id}
```

#### 获取区域详情
```
GET /api/v1/regions/{region_id}
```

### 3.2 部门管理

#### 获取组织架构树
```
GET /api/v1/departments/tree
```
**查询参数**：
- `region_id`: 区域ID（可选）
- `level`: 层级深度（可选）

#### 创建部门
```
POST /api/v1/departments
```
**请求体**：
```json
{
  "department_name": "string",
  "parent_id": "string",
  "manager_id": "string",
  "department_type": "string",
  "description": "string",
  "region_id": "string"
}
```

#### 更新部门信息
```
PUT /api/v1/departments/{department_id}
```

#### 删除部门
```
DELETE /api/v1/departments/{department_id}
```

#### 获取部门人员列表
```
GET /api/v1/departments/{department_id}/members
```

## 4. 人员信息管理API

### 3.1 人员档案管理

#### 获取人员列表
```
GET /api/v1/personnel
```
**查询参数**：
- `page`: 页码
- `size`: 每页数量
- `keyword`: 搜索关键词
- `region_id`: 区域ID
- `department_id`: 部门ID
- `status`: 人员状态
- `skill_type`: 技能类型

#### 创建人员档案
```
POST /api/v1/personnel
```
**请求体**：
```json
{
  "basic_info": {
    "real_name": "string",
    "gender": "male|female",
    "birth_date": "2000-01-01",
    "id_card": "string",
    "phone": "string",
    "email": "string",
    "address": "string"
  },
  "work_info": {
    "employee_id": "string",
    "join_date": "2024-01-01",
    "department_id": "string",
    "position": "string",
    "employment_type": "full_time|part_time|contract"
  },
  "emergency_contact": {
    "name": "string",
    "relationship": "string",
    "phone": "string"
  }
}
```

#### 更新人员信息
```
PUT /api/v1/personnel/{personnel_id}
```

#### 获取人员详情
```
GET /api/v1/personnel/{personnel_id}
```

#### 删除人员档案
```
DELETE /api/v1/personnel/{personnel_id}
```

### 3.2 技能管理

#### 获取人员技能列表
```
GET /api/v1/personnel/{personnel_id}/skills
```

#### 添加人员技能
```
POST /api/v1/personnel/{personnel_id}/skills
```
**请求体**：
```json
{
  "skill_type": "string",
  "skill_level": "beginner|intermediate|advanced|expert",
  "certificate_info": {
    "certificate_name": "string",
    "certificate_number": "string",
    "issue_date": "2024-01-01",
    "expire_date": "2025-01-01",
    "issuing_authority": "string"
  },
  "assessment_score": 85,
  "notes": "string"
}
```

#### 更新技能信息
```
PUT /api/v1/personnel/{personnel_id}/skills/{skill_id}
```

#### 删除技能记录
```
DELETE /api/v1/personnel/{personnel_id}/skills/{skill_id}
```

### 3.3 人员状态管理

#### 获取人员状态
```
GET /api/v1/personnel/{personnel_id}/status
```

#### 更新人员状态
```
PUT /api/v1/personnel/{personnel_id}/status
```
**请求体**：
```json
{
  "status": "available|busy|on_leave|transferred",
  "current_project_id": "string",
  "available_date": "2024-01-01",
  "notes": "string"
}
```

## 5. 项目管理API

### 4.1 项目基础管理

#### 获取项目列表
```
GET /api/v1/projects
```
**查询参数**：
- `page`: 页码
- `size`: 每页数量
- `keyword`: 搜索关键词
- `region_id`: 区域ID
- `project_type`: 项目类型
- `status`: 项目状态
- `manager_id`: 项目经理ID

#### 创建项目
```
POST /api/v1/projects
```
**请求体**：
```json
{
  "project_name": "string",
  "project_code": "string",
  "project_type": "construction|landscaping|comprehensive",
  "client_info": {
    "client_name": "string",
    "contact_person": "string",
    "contact_phone": "string"
  },
  "contract_info": {
    "contract_amount": 1000000,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "contract_number": "string"
  },
  "location": {
    "province": "string",
    "city": "string",
    "address": "string",
    "coordinates": {
      "latitude": 39.9042,
      "longitude": 116.4074
    }
  },
  "manager_id": "string",
  "region_id": "string"
}
```

#### 更新项目信息
```
PUT /api/v1/projects/{project_id}
```

#### 获取项目详情
```
GET /api/v1/projects/{project_id}
```

#### 删除项目
```
DELETE /api/v1/projects/{project_id}
```

### 4.2 人力需求管理

#### 获取项目人力需求
```
GET /api/v1/projects/{project_id}/requirements
```

#### 创建人力需求
```
POST /api/v1/projects/{project_id}/requirements
```
**请求体**：
```json
{
  "phase_name": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-03-31",
  "requirements": [{
    "position_type": "string",
    "skill_requirements": ["string"],
    "required_count": 5,
    "priority": "high|medium|low",
    "notes": "string"
  }]
}
```

#### 更新人力需求
```
PUT /api/v1/projects/{project_id}/requirements/{requirement_id}
```

### 4.3 项目团队管理

#### 获取项目团队
```
GET /api/v1/projects/{project_id}/team
```

#### 添加团队成员
```
POST /api/v1/projects/{project_id}/team
```
**请求体**：
```json
{
  "personnel_id": "string",
  "role": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "allocation_ratio": 100
}
```

#### 移除团队成员
```
DELETE /api/v1/projects/{project_id}/team/{personnel_id}
```

## 6. 调度管理核心API

### 5.1 智能匹配

#### 人员匹配查询
```
POST /api/v1/scheduling/match
```
**请求体**：
```json
{
  "project_id": "string",
  "requirements": [{
    "skill_type": "string",
    "skill_level": "string",
    "required_count": 3,
    "start_date": "2024-01-01",
    "end_date": "2024-03-31"
  }],
  "constraints": {
    "max_distance": 50,
    "max_cost": 10000,
    "preferred_regions": ["string"]
  }
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "matches": [{
      "personnel_id": "string",
      "personnel_name": "string",
      "match_score": 95,
      "skill_match": 90,
      "location_score": 85,
      "availability_score": 100,
      "cost_estimate": 5000,
      "distance_km": 25
    }],
    "alternatives": [],
    "summary": {
      "total_matches": 10,
      "perfect_matches": 3,
      "good_matches": 5,
      "acceptable_matches": 2
    }
  }
}
```

### 5.2 调度执行

#### 创建调度方案
```
POST /api/v1/scheduling/plans
```
**请求体**：
```json
{
  "plan_name": "string",
  "project_id": "string",
  "scheduling_type": "normal|emergency|cross_region",
  "assignments": [{
    "personnel_id": "string",
    "role": "string",
    "start_date": "2024-01-01",
    "end_date": "2024-03-31",
    "allocation_ratio": 100
  }],
  "reason": "string",
  "priority": "high|medium|low"
}
```

#### 执行调度方案
```
POST /api/v1/scheduling/plans/{plan_id}/execute
```

#### 获取调度方案列表
```
GET /api/v1/scheduling/plans
```

#### 获取调度方案详情
```
GET /api/v1/scheduling/plans/{plan_id}
```

### 5.3 调度冲突管理

#### 检测调度冲突
```
POST /api/v1/scheduling/conflicts/check
```
**请求体**：
```json
{
  "personnel_ids": ["string"],
  "start_date": "2024-01-01",
  "end_date": "2024-03-31"
}
```

#### 获取冲突解决方案
```
POST /api/v1/scheduling/conflicts/resolve
```

## 7. 审批流程API

### 6.1 审批流程管理

#### 提交审批申请
```
POST /api/v1/approvals
```
**请求体**：
```json
{
  "approval_type": "scheduling|recruitment|cost",
  "title": "string",
  "content": {},
  "urgency": "high|medium|low",
  "reason": "string",
  "attachments": ["string"]
}
```

#### 获取待审批列表
```
GET /api/v1/approvals/pending
```

#### 处理审批
```
POST /api/v1/approvals/{approval_id}/process
```
**请求体**：
```json
{
  "action": "approve|reject|transfer",
  "comment": "string",
  "transfer_to": "string"
}
```

#### 获取审批历史
```
GET /api/v1/approvals/{approval_id}/history
```

### 6.2 审批流程配置

#### 获取流程模板
```
GET /api/v1/approval-templates
```

#### 创建流程模板
```
POST /api/v1/approval-templates
```

## 8. 日历与时间管理API

### 7.1 日历管理

#### 获取日历数据
```
GET /api/v1/calendar
```
**查询参数**：
- `type`: 日历类型（personal|project|region|team）
- `target_id`: 目标ID
- `start_date`: 开始日期
- `end_date`: 结束日期
- `view`: 视图类型（month|week|day）

#### 创建日程安排
```
POST /api/v1/calendar/events
```
**请求体**：
```json
{
  "title": "string",
  "description": "string",
  "start_time": "2024-01-01T09:00:00Z",
  "end_time": "2024-01-01T17:00:00Z",
  "event_type": "work|meeting|training|leave",
  "participants": ["string"],
  "location": "string",
  "project_id": "string"
}
```

### 7.2 调度时间管理

#### 记录调度时长
```
POST /api/v1/schedule-duration
```
**请求体**：
```json
{
  "personnel_id": "string",
  "project_id": "string",
  "schedule_date": "2024-01-01",
  "planned_hours": 8,
  "schedule_description": "string",
  "location": "string"
}
```

#### 获取调度时长记录
```
GET /api/v1/schedule-duration
```
**查询参数**：
- `personnel_id`: 人员ID
- `project_id`: 项目ID
- `start_date`: 开始日期
- `end_date`: 结束日期

#### 调度时长统计
```
GET /api/v1/schedule-duration/statistics
```

### 7.3 ERP系统集成接口

#### 同步ERP人员数据
```
POST /api/v1/erp/sync-personnel
```
**请求体**：
```json
{
  "sync_type": "full|incremental",
  "last_sync_time": "2024-01-01T00:00:00Z",
  "erp_system": "sap|oracle|kingdee|ufida",
  "data_mapping": {
    "personnel_id_field": "string",
    "name_field": "string",
    "department_field": "string",
    "position_field": "string"
  }
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "sync_id": "string",
    "sync_status": "success|partial|failed",
    "processed_records": "number",
    "success_count": "number",
    "error_count": "number",
    "errors": [
      {
        "record_id": "string",
        "error_message": "string",
        "error_code": "string"
      }
    ]
  }
}
```

#### 推送调度数据到ERP
```
POST /api/v1/erp/push-scheduling
```
**请求体**：
```json
{
  "target_system": "string",
  "data_type": "assignment|cost|timesheet",
  "date_range": {
    "start_date": "string",
    "end_date": "string"
  },
  "filters": {
    "project_ids": ["string"],
    "department_ids": ["string"]
  }
}
```

## 9. 数据驱动评估分析 API

### 9.1 资源配置合理性评估

#### 配置效果评估
```
POST /api/v1/analytics/configuration-assessment
```
**请求体**：
```json
{
  "assessment_scope": "project|department|global",
  "target_ids": ["string"],
  "evaluation_period": {
    "start_date": "string",
    "end_date": "string"
  },
  "benchmark_type": "industry|historical|target",
  "metrics": ["cost_efficiency|resource_utilization|delivery_quality|timeline_adherence"]
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "assessment_id": "string",
    "overall_score": "number",
    "detailed_scores": {
      "cost_efficiency": {
        "score": "number",
        "benchmark_comparison": "above|at|below",
        "improvement_potential": "number"
      },
      "resource_utilization": {
        "score": "number",
        "optimal_range": "string",
        "current_status": "optimal|underutilized|overutilized"
      }
    },
    "recommendations": [
      {
        "category": "resource_reallocation|skill_development|process_optimization",
        "priority": "high|medium|low",
        "description": "string",
        "expected_impact": "number",
        "implementation_effort": "low|medium|high"
      }
    ],
    "roi_projection": {
      "investment_required": "number",
      "expected_savings": "number",
      "payback_period": "string",
      "risk_factors": ["string"]
    }
  }
}
```

### 9.2 智能决策支持系统

#### 多方案对比分析
```
POST /api/v1/analytics/scenario-comparison
```
**请求体**：
```json
{
  "comparison_type": "resource_allocation|project_scheduling|cost_optimization",
  "scenarios": [
    {
      "scenario_id": "string",
      "scenario_name": "string",
      "parameters": {
        "resource_allocation": {},
        "timeline": {},
        "budget_constraints": {}
      }
    }
  ],
  "evaluation_criteria": {
    "cost_weight": "number",
    "time_weight": "number",
    "quality_weight": "number",
    "risk_weight": "number"
  },
  "simulation_parameters": {
    "monte_carlo_iterations": "number",
    "confidence_level": "number"
  }
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "comparison_id": "string",
    "recommended_scenario": "string",
    "scenario_rankings": [
      {
        "scenario_id": "string",
        "rank": "number",
        "overall_score": "number",
        "detailed_scores": {
          "cost_score": "number",
          "time_score": "number",
          "quality_score": "number",
          "risk_score": "number"
        },
        "pros_cons": {
          "advantages": ["string"],
          "disadvantages": ["string"]
        }
      }
    ],
    "sensitivity_analysis": {
      "critical_factors": ["string"],
      "impact_analysis": [
        {
          "factor": "string",
          "impact_magnitude": "number",
          "confidence_interval": "string"
        }
      ]
    }
  }
}
```

### 9.3 预测性分析

#### 资源需求预测
```
POST /api/v1/analytics/demand-forecast
```
**请求体**：
```json
{
  "forecast_scope": "personnel|skills|budget|equipment",
  "forecast_horizon": "1m|3m|6m|1y",
  "historical_data_range": {
    "start_date": "string",
    "end_date": "string"
  },
  "external_factors": {
    "market_trends": ["string"],
    "seasonal_patterns": ["string"],
    "business_growth_rate": "number"
  },
  "model_parameters": {
    "algorithm": "arima|lstm|prophet|ensemble",
    "confidence_level": "number",
    "seasonality_adjustment": "boolean"
  }
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "forecast_id": "string",
    "model_accuracy": {
      "mape": "number",
      "rmse": "number",
      "r_squared": "number"
    },
    "predictions": [
      {
        "period": "string",
        "predicted_value": "number",
        "confidence_interval": {
          "lower_bound": "number",
          "upper_bound": "number"
        },
        "trend_direction": "increasing|decreasing|stable"
      }
    ],
    "insights": {
      "key_drivers": ["string"],
      "seasonal_patterns": ["string"],
      "anomaly_detection": ["string"]
    },
    "recommendations": [
      {
        "action_type": "hiring|training|reallocation|outsourcing",
        "timing": "string",
        "magnitude": "number",
        "rationale": "string"
      }
    ]
  }
}
```

## 10. ERP系统集成增强API

### 10.1 双向数据同步

#### 实时数据同步
```
POST /api/v1/erp/realtime-sync
```
**请求体**：
```json
{
  "sync_direction": "bidirectional|to_erp|from_erp",
  "data_types": ["personnel|projects|costs|schedules"],
  "erp_endpoint": {
    "system_type": "sap|oracle|kingdee|ufida|custom",
    "connection_string": "string",
    "authentication": {
      "type": "oauth|api_key|basic",
      "credentials": {}
    }
  },
  "sync_rules": {
    "conflict_resolution": "erp_priority|hrs_priority|manual_review",
    "data_validation": "strict|lenient",
    "batch_size": "number"
  }
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "sync_session_id": "string",
    "sync_status": "in_progress|completed|failed|partial",
    "progress": {
      "total_records": "number",
      "processed_records": "number",
      "success_count": "number",
      "error_count": "number",
      "warning_count": "number"
    },
    "data_summary": {
      "personnel_synced": "number",
      "projects_synced": "number",
      "cost_records_synced": "number"
    },
    "conflicts": [
      {
        "record_id": "string",
        "conflict_type": "data_mismatch|duplicate_key|validation_error",
        "description": "string",
        "resolution_options": ["string"]
      }
    ]
  }
}
```

#### ERP数据映射配置
```
POST /api/v1/erp/field-mapping
```
**请求体**：
```json
{
  "erp_system": "string",
  "entity_type": "personnel|project|cost_center|department",
  "field_mappings": [
    {
      "hrs_field": "string",
      "erp_field": "string",
      "data_type": "string|number|date|boolean",
      "transformation_rule": "string",
      "is_required": "boolean",
      "default_value": "string"
    }
  ],
  "validation_rules": [
    {
      "field": "string",
      "rule_type": "format|range|enum|custom",
      "rule_definition": "string"
    }
  ]
}
```

### 10.2 财务集成

#### 成本中心同步
```
POST /api/v1/erp/cost-centers/sync
```
**请求体**：
```json
{
  "sync_mode": "full|incremental",
  "cost_center_hierarchy": "boolean",
  "include_budgets": "boolean",
  "fiscal_year": "string"
}
```
**响应**：
```json
{
  "code": 200,
  "data": {
    "cost_centers": [
      {
        "cost_center_id": "string",
        "cost_center_code": "string",
        "name": "string",
        "parent_id": "string",
        "budget_info": {
          "annual_budget": "number",
          "used_budget": "number",
          "remaining_budget": "number"
        },
        "responsible_person": "string"
      }
    ],
    "hierarchy_structure": {},
    "sync_timestamp": "string"
  }
}
```

#### 费用报销集成
```
POST /api/v1/erp/expense-integration
```
**请求体**：
```json
{
  "expense_data": [
    {
      "personnel_id": "string",
      "project_id": "string",
      "expense_type": "travel|material|equipment|other",
      "amount": "number",
      "currency": "string",
      "expense_date": "string",
      "description": "string",
      "receipts": ["string"]
    }
  ],
  "approval_workflow": "boolean",
  "cost_center_allocation": "automatic|manual"
}
```

### 10.3 工作流集成

#### 审批流程同步
```
POST /api/v1/erp/workflow-sync
```
**请求体**：
```json
{
  "workflow_type": "personnel_request|budget_approval|project_change",
  "erp_workflow_id": "string",
  "mapping_rules": {
    "approval_levels": ["string"],
    "notification_settings": {},
    "escalation_rules": []
  }
}
```

## 11. 调度分析API

### 11.1 调度资源分析

#### 调度资源配置报表
```
GET /api/v1/reports/schedule-allocation
```
**查询参数**：
- `start_date`: 开始日期
- `end_date`: 结束日期
- `region_id`: 区域ID
- `department_id`: 部门ID
- `group_by`: 分组方式（person|department|region|skill）

#### 调度成本分析报表
```
GET /api/v1/reports/schedule-costs
```

#### 调度冲突分析报表
```
GET /api/v1/reports/schedule-conflicts
```

### 11.2 项目分析

#### 项目进度报表
```
GET /api/v1/reports/project-progress
```

#### 项目人力配置报表
```
GET /api/v1/reports/project-staffing
```

### 11.3 自定义报表

#### 创建自定义报表
```
POST /api/v1/reports/custom
```
**请求体**：
```json
{
  "report_name": "string",
  "description": "string",
  "data_source": "string",
  "filters": {},
  "grouping": ["string"],
  "metrics": ["string"],
  "chart_type": "table|bar|line|pie"
}
```

#### 执行自定义报表
```
POST /api/v1/reports/custom/{report_id}/execute
```

## 12. 系统管理API

### 12.1 系统配置

#### 获取系统配置
```
GET /api/v1/system/config
```

#### 更新系统配置
```
PUT /api/v1/system/config
```

### 12.2 数据管理

#### 数据备份
```
POST /api/v1/system/backup
```

#### 数据恢复
```
POST /api/v1/system/restore
```

### 12.3 系统监控

#### 获取系统状态
```
GET /api/v1/system/status
```

#### 获取操作日志
```
GET /api/v1/system/logs
```

## 13. 移动端专用API

### 13.1 移动端认证

#### 移动端登录
```
POST /api/v1/mobile/auth/login
```
**请求体**：
```json
{
  "username": "string",
  "password": "string",
  "device_info": {
    "device_id": "string",
    "device_type": "ios|android",
    "app_version": "string",
    "os_version": "string"
  },
  "push_token": "string",
  "location": {
    "latitude": 39.9042,
    "longitude": 116.4074
  }
}
```

### 13.2 现场管理

#### 现场签到
```
POST /api/v1/mobile/checkin
```
**请求体**：
```json
{
  "project_id": "string",
  "location": {
    "latitude": 39.9042,
    "longitude": 116.4074,
    "address": "string"
  },
  "photos": ["base64_string"],
  "notes": "string"
}
```

#### 现场签退
```
POST /api/v1/mobile/checkout
```

#### 上传现场照片
```
POST /api/v1/mobile/photos
```

### 13.3 移动端数据同步

#### 获取离线数据包
```
GET /api/v1/mobile/sync/download
```

#### 上传离线数据
```
POST /api/v1/mobile/sync/upload
```

## API安全规范

### 1. 认证机制
- JWT Token认证
- Token过期时间：1小时
- Refresh Token有效期：7天
- 支持Token黑名单机制

### 2. 权限控制
- 基于角色的访问控制（RBAC）
- API级别权限验证
- 数据级别权限过滤
- 操作审计日志

### 3. 数据安全
- HTTPS强制加密
- 敏感数据脱敏
- SQL注入防护
- XSS攻击防护
- CSRF防护

### 4. 接口限流
- 基于用户的请求频率限制
- 基于IP的请求频率限制
- 重要接口特殊限流策略

## API版本管理

### 版本策略
- URL路径版本控制：`/api/v1/`
- 向后兼容原则
- 废弃接口提前通知
- 版本生命周期管理

### 版本规划
- v1.0：基础功能API
- v1.1：增强功能和优化
- v2.0：重大架构升级

## 14. 系统集成模块API

### 14.1 第三方系统对接

#### 通用集成接口
```
POST /api/v1/integration/third-party/connect
```
**请求体**：
```json
{
  "system_type": "erp|crm|oa|hr|finance|custom",
  "system_name": "string",
  "connection_config": {
    "endpoint_url": "string",
    "authentication": {
      "type": "oauth2|api_key|basic|certificate",
      "credentials": {}
    },
    "data_format": "json|xml|csv|custom",
    "sync_frequency": "realtime|hourly|daily|weekly"
  },
  "data_mapping": {
    "entity_mappings": [
      {
        "source_entity": "string",
        "target_entity": "string",
        "field_mappings": []
      }
    ]
  }
}
```

#### 数据交换平台
```
POST /api/v1/integration/data-exchange
```
**请求体**：
```json
{
  "exchange_type": "import|export|sync",
  "source_system": "string",
  "target_system": "string",
  "data_package": {
    "format": "json|xml|csv|excel",
    "compression": "none|zip|gzip",
    "encryption": "none|aes256|rsa",
    "data_content": "string"
  },
  "validation_rules": [
    {
      "field": "string",
      "rule": "required|format|range|custom",
      "parameters": {}
    }
  ],
  "error_handling": {
    "on_validation_error": "skip|abort|log",
    "retry_policy": {
      "max_retries": "number",
      "retry_interval": "number"
    }
  }
}
```

### 14.2 消息队列集成

#### 事件发布
```
POST /api/v1/integration/events/publish
```
**请求体**：
```json
{
  "event_type": "personnel_assigned|project_updated|schedule_changed|approval_completed",
  "event_data": {
    "entity_id": "string",
    "entity_type": "string",
    "change_details": {},
    "timestamp": "string",
    "user_id": "string"
  },
  "routing_key": "string",
  "priority": "low|normal|high|urgent",
  "delivery_mode": "persistent|transient"
}
```

#### 事件订阅管理
```
POST /api/v1/integration/events/subscribe
```
**请求体**：
```json
{
  "subscription_name": "string",
  "event_types": ["string"],
  "filter_conditions": {
    "department_ids": ["string"],
    "project_ids": ["string"],
    "priority_levels": ["string"]
  },
  "callback_config": {
    "webhook_url": "string",
    "authentication": {},
    "retry_policy": {}
  }
}
```

## 总结

本API接口设计文档涵盖了人力资源调度系统的核心功能模块，包括：

1. **认证授权**：完整的用户认证和权限管理
2. **人员管理**：人员信息的增删改查和技能管理
3. **项目管理**：项目全生命周期管理
4. **智能化资源调度管理**：AI驱动的智能匹配和可视化调度
5. **全流程资源风险管控**：实时监控、预警和应急响应
6. **审批流程**：灵活的工作流管理
7. **日历管理**：时间和日程安排
8. **数据驱动评估分析**：配置评估、决策支持和预测分析
9. **ERP系统集成**：双向数据同步和财务工作流集成
10. **报表分析**：数据分析和可视化
11. **系统管理**：系统配置和监控
12. **移动端支持**：移动设备专用功能
13. **系统集成模块**：第三方系统对接和数据交换平台

### API设计原则

- **RESTful设计**：遵循REST架构风格
- **统一响应格式**：标准化的JSON响应结构
- **版本控制**：通过URL路径进行版本管理
- **安全性**：JWT认证和权限控制
- **模块化架构**：支持独立部署和系统集成
- **可扩展性**：预留ERP集成接口，支持未来扩展
- **性能优化**：支持分页、缓存和批量操作
- **智能化支持**：集成AI算法和数据分析能力

### 技术规范

- **协议**：HTTPS
- **数据格式**：JSON
- **认证方式**：JWT Bearer Token
- **字符编码**：UTF-8
- **时间格式**：ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)
- **集成标准**：支持多种ERP系统标准接口

### 接口统计

- **总接口数量**：150+
- **核心业务接口**：95+
- **智能化功能接口**：25+
- **系统集成接口**：20+
- **管理类接口**：15+
- **移动端专用接口**：10+

### 系统特色

- **不包含考勤功能**：专注资源调度核心业务
- **智能化驱动**：AI算法支持的智能匹配和预测
- **可视化交互**：现代化拖拽式操作界面
- **风险管控**：全流程风险识别和预警机制
- **数据驱动**：基于数据分析的决策支持
- **系统集成**：预留标准化ERP集成接口

本文档为系统开发提供了完整的API规范，确保前后端开发的一致性和系统的可维护性，同时为未来的系统集成和功能扩展奠定了坚实基础。

---

## 文档信息

**文档版本**：v1.0  
**创建日期**：2024年  
**API总数**：150+ 个接口  
**支持格式**：JSON  
**认证方式**：JWT Bearer Token  
**文档类型**：RESTful API设计规范