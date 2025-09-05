# 人力资源调度系统 - 后端API集成手册

## 文档概述

### 文档目的
本文档提供人力资源调度系统后端API的完整技术规范，为前端开发团队提供标准化的接口集成指南。

### API基础信息
- **基础URL**：`${base_url}/api/v1`
- **协议**：HTTPS
- **数据格式**：JSON
- **字符编码**：UTF-8
- **API版本**：v1.0

### 文档约定
- 所有时间格式采用ISO 8601标准：`YYYY-MM-DDTHH:mm:ssZ`
- 所有金额字段保留2位小数
- 布尔值使用`true`/`false`
- 空值使用`null`

## 通用响应格式

### 成功响应格式
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体业务数据
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 分页响应格式
```json
{
  "success": true,
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 错误响应格式
```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "type": "VALIDATION_ERROR",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      }
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## HTTP状态码规范

### 成功状态码
- **200 OK**：请求成功
- **201 Created**：资源创建成功
- **204 No Content**：删除成功，无返回内容

### 客户端错误状态码
- **400 Bad Request**：请求参数错误
- **401 Unauthorized**：未授权，需要登录
- **403 Forbidden**：权限不足
- **404 Not Found**：资源不存在
- **409 Conflict**：资源冲突
- **422 Unprocessable Entity**：业务逻辑错误
- **429 Too Many Requests**：请求频率超限

### 服务器错误状态码
- **500 Internal Server Error**：服务器内部错误
- **502 Bad Gateway**：网关错误
- **503 Service Unavailable**：服务不可用

## 业务错误码定义

### 通用错误码 (1000-1999)
- **1001**：参数缺失
- **1002**：参数格式错误
- **1003**：参数值超出范围
- **1004**：请求频率超限
- **1005**：系统维护中

### 认证错误码 (2000-2999)
- **2001**：Token无效
- **2002**：Token过期
- **2003**：权限不足
- **2004**：账号被锁定
- **2005**：密码错误

### 业务错误码 (3000-3999)
- **3001**：用户不存在
- **3002**：项目不存在
- **3003**：调度冲突
- **3004**：资源不足
- **3005**：操作不允许

## 认证与授权

### JWT Token认证

#### 获取Token
**接口路径**：`POST /auth/login`

**请求参数**：
```json
{
  "username": "string",     // 必填，用户名
  "password": "string",     // 必填，密码
  "remember": "boolean"     // 可选，记住登录状态
}
```

**响应示例**：
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "username": "admin",
      "name": "管理员",
      "role": "admin",
      "permissions": ["user:read", "project:write"]
    }
  }
}
```

#### Token使用方式
在所有需要认证的请求头中添加：
```
Authorization: Bearer {token}
```

#### Token刷新
**接口路径**：`POST /auth/refresh`

**请求参数**：
```json
{
  "refresh_token": "string"  // 必填，刷新令牌
}
```

### 权限控制

#### 权限模型
系统采用RBAC（基于角色的访问控制）模型：
- **用户** → **角色** → **权限**
- 支持多角色分配
- 支持权限继承

#### 权限验证
每个API接口都会验证用户权限，权限不足时返回403错误。

## 核心API接口

### 1. 用户管理API

#### 获取用户列表
**接口路径**：`GET /users`
**HTTP方法**：GET
**权限要求**：`user:read`

**查询参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| size | integer | 否 | 每页数量，默认20 |
| keyword | string | 否 | 搜索关键词 |
| role | string | 否 | 角色筛选 |
| status | string | 否 | 状态筛选：active/inactive |

**响应示例**：
```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "username": "zhangsan",
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "role": "employee",
        "department": "技术部",
        "status": "active",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

#### 创建用户
**接口路径**：`POST /users`
**HTTP方法**：POST
**权限要求**：`user:write`

**请求参数**：
```json
{
  "username": "string",      // 必填，用户名，3-20字符
  "name": "string",          // 必填，姓名，2-50字符
  "email": "string",         // 必填，邮箱地址
  "phone": "string",         // 可选，手机号码
  "password": "string",      // 必填，密码，8-20字符
  "role": "string",          // 必填，角色：admin/manager/employee
  "department_id": "integer", // 可选，部门ID
  "skills": ["string"],      // 可选，技能标签数组
  "status": "string"         // 可选，状态，默认active
}
```

#### 更新用户信息
**接口路径**：`PUT /users/{id}`
**HTTP方法**：PUT
**权限要求**：`user:write`

**路径参数**：
- `id`：用户ID

**请求参数**：同创建用户，但所有字段都是可选的

#### 删除用户
**接口路径**：`DELETE /users/{id}`
**HTTP方法**：DELETE
**权限要求**：`user:delete`

### 2. 项目管理API

#### 获取项目列表
**接口路径**：`GET /projects`
**HTTP方法**：GET
**权限要求**：`project:read`

**查询参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| size | integer | 否 | 每页数量，默认20 |
| status | string | 否 | 项目状态：planning/active/completed/cancelled |
| priority | string | 否 | 优先级：low/medium/high/urgent |
| start_date | string | 否 | 开始日期筛选，格式：YYYY-MM-DD |
| end_date | string | 否 | 结束日期筛选，格式：YYYY-MM-DD |

**响应示例**：
```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "移动应用开发项目",
        "description": "开发企业级移动应用",
        "status": "active",
        "priority": "high",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "budget": 500000.00,
        "progress": 65.5,
        "manager": {
          "id": 2,
          "name": "李四"
        },
        "team_size": 8,
        "required_skills": ["React", "Node.js", "MongoDB"],
        "created_at": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 50,
      "pages": 3
    }
  }
}
```

#### 创建项目
**接口路径**：`POST /projects`
**HTTP方法**：POST
**权限要求**：`project:write`

**请求参数**：
```json
{
  "name": "string",              // 必填，项目名称，2-100字符
  "description": "string",       // 可选，项目描述
  "priority": "string",          // 必填，优先级：low/medium/high/urgent
  "start_date": "string",        // 必填，开始日期，格式：YYYY-MM-DD
  "end_date": "string",          // 必填，结束日期，格式：YYYY-MM-DD
  "budget": "number",            // 可选，预算金额
  "manager_id": "integer",       // 必填，项目经理ID
  "required_skills": ["string"], // 可选，所需技能数组
  "team_size": "integer"         // 可选，团队规模
}
```

### 3. 智能调度API

#### 创建调度任务
**接口路径**：`POST /scheduling/tasks`
**HTTP方法**：POST
**权限要求**：`scheduling:write`

**请求参数**：
```json
{
  "project_id": "integer",       // 必填，项目ID
  "task_name": "string",         // 必填，任务名称
  "required_skills": ["string"], // 必填，所需技能
  "start_date": "string",        // 必填，开始日期
  "end_date": "string",          // 必填，结束日期
  "workload": "number",          // 必填，工作量（小时）
  "priority": "string",          // 必填，优先级
  "constraints": {               // 可选，约束条件
    "exclude_users": ["integer"], // 排除的用户ID
    "prefer_users": ["integer"],  // 偏好的用户ID
    "max_team_size": "integer"    // 最大团队规模
  }
}
```

**响应示例**：
```json
{
  "success": true,
  "code": 201,
  "message": "调度任务创建成功",
  "data": {
    "task_id": "12345",
    "status": "pending",
    "estimated_completion": "2024-01-01T15:30:00Z"
  }
}
```

#### 获取调度结果
**接口路径**：`GET /scheduling/tasks/{task_id}/result`
**HTTP方法**：GET
**权限要求**：`scheduling:read`

**响应示例**：
```json
{
  "success": true,
  "code": 200,
  "data": {
    "task_id": "12345",
    "status": "completed",
    "result": {
      "recommended_team": [
        {
          "user_id": 1,
          "name": "张三",
          "role": "前端开发",
          "match_score": 95.5,
          "availability": 80.0,
          "skills_match": ["React", "TypeScript"]
        }
      ],
      "alternative_teams": [],
      "conflicts": [],
      "confidence_score": 92.3
    },
    "completed_at": "2024-01-01T15:28:30Z"
  }
}
```

### 4. 数据分析API

#### 获取统计数据
**接口路径**：`GET /analytics/dashboard`
**HTTP方法**：GET
**权限要求**：`analytics:read`

**查询参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| period | string | 否 | 统计周期：day/week/month/quarter/year |
| start_date | string | 否 | 开始日期 |
| end_date | string | 否 | 结束日期 |

**响应示例**：
```json
{
  "success": true,
  "code": 200,
  "data": {
    "summary": {
      "total_projects": 156,
      "active_projects": 23,
      "total_users": 89,
      "utilization_rate": 78.5
    },
    "charts": {
      "project_trend": [
        {"date": "2024-01-01", "count": 12},
        {"date": "2024-01-02", "count": 15}
      ],
      "skill_distribution": [
        {"skill": "React", "count": 25},
        {"skill": "Python", "count": 18}
      ]
    }
  }
}
```

## API调用示例

### JavaScript/TypeScript示例

#### 基础API客户端
```typescript
class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('access_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}/api/v1${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || '请求失败');
    }

    return response.json();
  }

  // 登录
  async login(username: string, password: string) {
    const response = await this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    
    this.token = response.data.token;
    localStorage.setItem('access_token', this.token);
    return response;
  }

  // 获取用户列表
  async getUsers(params?: UserListParams) {
    const query = new URLSearchParams(params as any).toString();
    return this.request<UserListResponse>(`/users?${query}`);
  }

  // 创建项目
  async createProject(data: CreateProjectData) {
    return this.request<ProjectResponse>('/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

// 使用示例
const api = new ApiClient('https://api.example.com');

// 登录
try {
  const loginResult = await api.login('admin', 'password123');
  console.log('登录成功:', loginResult.data.user);
} catch (error) {
  console.error('登录失败:', error.message);
}

// 获取用户列表
try {
  const users = await api.getUsers({ page: 1, size: 20 });
  console.log('用户列表:', users.data.items);
} catch (error) {
  console.error('获取用户列表失败:', error.message);
}
```

#### React Hook示例
```typescript
import { useState, useEffect } from 'react';

// 自定义Hook：获取用户列表
function useUsers(params?: UserListParams) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await api.getUsers(params);
        setUsers(response.data.items);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [params]);

  return { users, loading, error };
}

// 组件使用示例
function UserList() {
  const { users, loading, error } = useUsers({ page: 1, size: 20 });

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误: {error}</div>;

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### 错误处理示例
```typescript
// 统一错误处理
class ApiError extends Error {
  constructor(
    public code: number,
    public type: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// 错误处理中间件
async function handleApiError(response: Response) {
  if (!response.ok) {
    const errorData = await response.json();
    throw new ApiError(
      errorData.code,
      errorData.error?.type || 'UNKNOWN_ERROR',
      errorData.message,
      errorData.error?.details
    );
  }
  return response;
}

// 使用示例
try {
  const result = await api.createUser(userData);
} catch (error) {
  if (error instanceof ApiError) {
    switch (error.code) {
      case 2001:
        // Token无效，跳转登录
        router.push('/login');
        break;
      case 3001:
        // 用户不存在
        showMessage('用户不存在', 'error');
        break;
      default:
        showMessage(error.message, 'error');
    }
  }
}
```

## 性能优化建议

### 请求优化
1. **请求合并**：使用批量接口减少请求次数
2. **缓存策略**：对静态数据进行客户端缓存
3. **分页加载**：大数据集使用分页或虚拟滚动
4. **请求去重**：避免重复请求

### 并发处理
1. **请求限流**：控制并发请求数量
2. **超时设置**：设置合理的请求超时时间
3. **重试机制**：网络错误时自动重试
4. **降级处理**：服务不可用时的降级方案

### 数据处理
1. **数据预处理**：在接收数据后进行格式化
2. **增量更新**：只更新变化的数据
3. **内存管理**：及时清理不需要的数据
4. **懒加载**：按需加载数据

## 安全注意事项

### Token安全
1. **安全存储**：使用httpOnly Cookie或安全的localStorage
2. **定期刷新**：Token过期前自动刷新
3. **退出清理**：登出时清除所有Token
4. **传输加密**：使用HTTPS传输

### 数据验证
1. **输入验证**：前端验证所有用户输入
2. **XSS防护**：对输出内容进行转义
3. **CSRF防护**：使用CSRF Token
4. **敏感信息**：避免在URL中传递敏感信息

### 权限控制
1. **最小权限**：只请求必要的权限
2. **权限验证**：每次操作前验证权限
3. **敏感操作**：重要操作需要二次确认
4. **审计日志**：记录重要操作日志

## 测试与调试

### API测试工具
- **Postman**：接口测试和文档
- **Insomnia**：REST客户端
- **curl**：命令行测试
- **浏览器开发者工具**：网络面板调试

### Mock服务
```typescript
// Mock数据示例
const mockUsers = [
  {
    id: 1,
    username: 'admin',
    name: '管理员',
    email: 'admin@example.com',
    role: 'admin',
    status: 'active'
  }
];

// Mock API服务
class MockApiClient {
  async getUsers(params?: UserListParams) {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return {
      success: true,
      code: 200,
      data: {
        items: mockUsers,
        pagination: {
          page: 1,
          size: 20,
          total: mockUsers.length,
          pages: 1
        }
      }
    };
  }
}
```

### 环境配置
```typescript
// 环境配置
const config = {
  development: {
    apiUrl: 'http://localhost:8000',
    mockEnabled: true
  },
  staging: {
    apiUrl: 'https://staging-api.example.com',
    mockEnabled: false
  },
  production: {
    apiUrl: 'https://api.example.com',
    mockEnabled: false
  }
};

const currentConfig = config[process.env.NODE_ENV || 'development'];
```

---

*本文档提供API集成规范，具体实现请参考前端开发团队技术选型。*