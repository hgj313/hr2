# 人力资源调度系统 - 后端服务

基于 FastAPI 的现代化人力资源调度管理系统后端服务，提供完整的 RESTful API 接口。

## 🚀 功能特性

### 核心功能模块
- **用户认证与授权** - JWT令牌认证、角色权限管理、多因素认证
- **组织架构管理** - 部门、职位、人员信息管理
- **项目管理** - 项目创建、任务分配、里程碑跟踪
- **调度管理** - 智能调度算法、资源分配、冲突检测
- **审批流程** - 可配置工作流、多级审批、委托机制
- **风险管控** - 风险评估、预警系统、缓解计划
- **数据分析** - 报表生成、仪表板、数据可视化

### 技术特性
- **高性能** - 异步处理、数据库连接池、Redis缓存
- **可扩展** - 微服务架构、模块化设计、插件系统
- **安全性** - 数据加密、SQL注入防护、访问控制
- **可观测** - 结构化日志、性能监控、健康检查
- **开发友好** - 自动API文档、类型提示、测试覆盖

## 📋 系统要求

- **Python**: 3.8+
- **数据库**: PostgreSQL 12+
- **缓存**: Redis 6+
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

## 🛠️ 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd "Human resource scheduling/backend"

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

```bash
# 安装 PostgreSQL
# Windows: 下载官方安装包
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# 创建数据库
psql -U postgres
CREATE DATABASE hr_scheduling;
CREATE USER hr_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hr_scheduling TO hr_user;
```

### 3. Redis 配置

```bash
# 安装 Redis
# Windows: 下载官方安装包或使用 WSL
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server

# 启动 Redis
redis-server
```

### 4. 环境变量配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置数据库和其他设置
# 主要配置项：
# - DATABASE_URL: 数据库连接字符串
# - REDIS_URL: Redis连接字符串
# - SECRET_KEY: JWT密钥（生产环境请使用强密钥）
```

### 5. 一键启动（推荐）

```bash
# 使用启动脚本（自动检查环境、初始化数据库、启动服务）
python start_dev.py
```

### 6. 手动启动

```bash
# 数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API 文档

启动服务后，可通过以下地址访问 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 默认账户

系统初始化后会创建默认管理员账户：

- **邮箱**: admin@example.com
- **密码**: admin123
- **角色**: 系统管理员

⚠️ **生产环境请立即修改默认密码！**

## 🏗️ 项目结构

```
backend/
├── app/
│   ├── api/                    # API路由
│   │   └── v1/
│   │       ├── endpoints/      # API端点
│   │       └── api.py         # 路由汇总
│   ├── core/                   # 核心配置
│   │   ├── config.py          # 应用配置
│   │   ├── database.py        # 数据库配置
│   │   └── security.py        # 安全配置
│   ├── models/                 # 数据模型
│   ├── schemas/                # Pydantic模式
│   ├── services/               # 业务逻辑
│   ├── utils/                  # 工具函数
│   └── main.py                # 应用入口
├── alembic/                    # 数据库迁移
├── tests/                      # 测试代码
├── logs/                       # 日志文件
├── uploads/                    # 上传文件
├── requirements.txt            # 依赖列表
├── .env.example               # 环境变量模板
├── start_dev.py               # 开发启动脚本
└── README.md                  # 项目说明
```

## 🔧 开发指南

### 代码规范

```bash
# 代码格式化
black app/
isort app/

# 代码检查
flake8 app/
mypy app/

# 运行测试
pytest tests/ -v --cov=app
```

### 数据库迁移

```bash
# 创建迁移文件
alembic revision --autogenerate -m "描述信息"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 添加新功能模块

1. 在 `models/` 中创建数据模型
2. 在 `schemas/` 中创建 Pydantic 模式
3. 在 `api/v1/endpoints/` 中创建 API 端点
4. 在 `services/` 中实现业务逻辑
5. 更新路由配置和文档

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

## 📊 监控和日志

### 健康检查
- **基础健康检查**: GET /health
- **详细健康检查**: GET /health/detailed
- **数据库健康检查**: GET /health/database
- **Redis健康检查**: GET /health/redis

### 日志配置
日志文件位置：`logs/app.log`

日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL

### 性能监控
- **Prometheus指标**: http://localhost:8001/metrics
- **应用指标**: 请求数、响应时间、错误率
- **系统指标**: CPU、内存、数据库连接数

## 🚀 部署

### Docker 部署

```bash
# 构建镜像
docker build -t hr-scheduling-backend .

# 运行容器
docker run -p 8000:8000 --env-file .env hr-scheduling-backend
```

### 生产环境配置

1. **环境变量**
   - 设置 `ENVIRONMENT=production`
   - 使用强密钥 `SECRET_KEY`
   - 配置生产数据库

2. **安全配置**
   - 启用 HTTPS
   - 配置防火墙
   - 设置访问控制

3. **性能优化**
   - 使用 Gunicorn + Uvicorn
   - 配置负载均衡
   - 启用数据库连接池

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 提交规范

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果您遇到问题或有疑问：

1. 查看 [FAQ](docs/FAQ.md)
2. 搜索 [Issues](../../issues)
3. 创建新的 [Issue](../../issues/new)
4. 联系开发团队

## 📈 路线图

- [ ] 微服务架构重构
- [ ] GraphQL API 支持
- [ ] 实时通知系统
- [ ] 移动端 API 优化
- [ ] AI 智能调度算法
- [ ] 多租户支持
- [ ] 国际化支持

---

**开发团队** | **版本**: 1.0.0 | **最后更新**: 2024年