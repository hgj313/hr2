# 人力资源调度系统

一个现代化的企业级人力资源调度管理系统，采用前后端分离架构，提供智能化的人员调度、项目管理和数据分析功能。

## 🚀 项目概述

本系统旨在解决企业人力资源调度中的复杂问题，通过智能算法优化人员分配，提高工作效率，降低管理成本。

### 核心功能

- 🏠 **智能仪表盘**: 实时数据概览和关键指标监控
- 👥 **用户管理**: 完整的用户生命周期管理和权限控制
- 📋 **项目管理**: 项目创建、任务分配和进度跟踪
- 📅 **智能调度**: 基于AI的自动化排班和冲突解决
- 📊 **数据分析**: 多维度数据分析和可视化报表
- 🔔 **通知系统**: 实时消息推送和智能提醒
- 🔐 **安全认证**: 多层级权限管理和安全防护

## 🏗️ 技术架构

### 前端技术栈
- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **UI组件**: Radix UI + shadcn/ui
- **状态管理**: TanStack Query
- **图表**: Recharts

### 后端技术栈
- **框架**: FastAPI (Python)
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **认证**: JWT + OAuth2
- **API文档**: OpenAPI/Swagger
- **测试**: Pytest

## 📁 项目结构

```
Human-Resource-Scheduling/
├── frontend/                   # 前端应用
│   ├── app/                   # Next.js 页面
│   ├── components/            # React 组件
│   ├── lib/                   # 工具库和API客户端
│   ├── package.json           # 前端依赖
│   └── README.md             # 前端文档
├── backend/                   # 后端应用
│   ├── app/                   # FastAPI 应用
│   │   ├── api/              # API 路由
│   │   ├── core/             # 核心配置
│   │   ├── crud/             # 数据库操作
│   │   ├── models/           # 数据模型
│   │   ├── schemas/          # Pydantic 模式
│   │   └── utils/            # 工具函数
│   ├── tests/                # 测试用例
│   ├── requirements.txt      # Python 依赖
│   └── README.md            # 后端文档
├── docs/                     # 项目文档
├── .gitignore               # Git 忽略规则
└── README.md               # 项目总览
```

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.9+
- PostgreSQL 13+
- Git

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:3000 启动

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python start_dev.py
```

后端API将在 http://localhost:8000 启动

## 📖 文档

- [前端开发文档](./frontend/README.md)
- [后端开发文档](./backend/README.md)
- [API接口文档](./docs/Technical%20Documentation/API接口设计文档.md)
- [业务需求文档](./docs/Technical%20Documentation/人力资源调度系统业务需求文档.md)
- [技术实现文档](./docs/Technical%20Documentation/人力资源调度系统技术实现文档.md)

## 🔧 开发规范

### 代码规范
- 前端遵循 ESLint + Prettier 规范
- 后端遵循 PEP 8 Python 代码规范
- 使用 TypeScript 进行类型安全开发
- 统一的命名规范和注释标准

### Git 工作流
- 使用 GitFlow 分支管理策略
- 提交信息遵循 Conventional Commits 规范
- 代码审查和自动化测试

### 测试策略
- 前端: Jest + React Testing Library
- 后端: Pytest + 覆盖率报告
- E2E测试: Playwright

## 🚀 部署

### 开发环境
- 前端: Vercel / Netlify
- 后端: Docker + Docker Compose
- 数据库: PostgreSQL

### 生产环境
- 容器化部署 (Docker)
- CI/CD 自动化流水线
- 监控和日志系统

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- 项目维护者: [项目团队]
- 邮箱: [联系邮箱]
- 问题反馈: [GitHub Issues](https://github.com/your-repo/issues)

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！