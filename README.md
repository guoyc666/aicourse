# AI辅助学习系统

一个基于知识图谱的个性化学习系统，集成了大模型微调、RAG技术、智能题库和AI助教等功能。

## 项目概述

本系统是一个完整的AI辅助学习平台，支持多角色用户（管理员、教师、学生），提供从知识资源管理到个性化学习的全流程解决方案。

## 技术架构

### 后端技术栈
- **FastAPI**: 现代化的Python Web框架
- **MySQL**: 关系型数据库
- **SQLAlchemy**: ORM框架
- **JWT**: 身份认证
- **Pydantic**: 数据验证
- **python-dotenv**: 环境变量管理

### 前端技术栈
- **Vue 3**: 渐进式JavaScript框架
- **Element Plus**: Vue 3 UI组件库
- **Vite**: 快速构建工具
- **Pinia**: 状态管理
- **Vue Router**: 路由管理

## 功能模块

### 1. 多角色支持模块
- **RBAC权限管理**: 基于角色的访问控制
- **用户认证**: JWT令牌认证
- **角色分配**: 管理员、教师、学生角色
- **权限控制**: 细粒度权限管理

### 2. 任务管理模块
- **任务创建与分配**: 教师可创建并分配学习任务
- **任务提交与评估**: 学生提交任务，教师进行评估
- **任务进度追踪**: 监控任务完成情况

### 3. 主题讨论模块
- **主题创建**: 教师可创建学习主题
- **讨论互动**: 学生可参与主题讨论
- **内容管理**: 管理讨论内容和回复

### 4. 用户管理模块
- **用户注册与登录**: 支持多种角色用户管理
- **个人信息维护**: 用户可更新个人资料
- **权限配置**: 管理员可配置用户权限

## 项目结构

```
ai/
├── backend/                 # 后端代码
│   ├── main.py             # 应用入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic模式
│   ├── auth.py             # 认证模块
│   ├── init_data.py        # 初始化数据
│   └── routers/            # API路由
│       ├── auth.py         # 认证路由
│       ├── tasks.py        # 任务相关路由
│       ├── topics.py       # 主题相关路由
│       └── users.py        # 用户管理路由
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── main.js        # 应用入口
│   │   ├── App.vue        # 根组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # 状态管理
│   │   ├── api/           # API接口
│   │   ├── views/         # 页面组件
│   │   ├── layout/        # 布局组件
│   │   └── styles/        # 样式文件
│   ├── package.json       # 依赖配置
│   └── vite.config.js     # 构建配置
├── requirements.txt        # Python依赖
├── start.bat              # 启动脚本
├── README.md              # 项目说明
└── 任务说明.txt            # 任务文档
```

## 安装和运行

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Neo4j 4.0+
- Redis 6.0+

### 后端安装
```bash
# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp backend/env_example.txt backend/.env
# 编辑 .env 文件，配置MySQL数据库连接
# 注意：使用MySQL前需手动创建ai_learning_system数据库

# 初始化数据库
python backend/init_data.py

# 启动后端服务
python backend/main.py
```

### 前端安装
```bash
# 安装Node.js依赖
cd frontend
npm install

# 启动开发服务器
npm run dev
```

### 访问地址
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 默认账户

系统初始化后提供默认管理员账户：
- 用户名: `admin`
- 密码: `admin123`

## 主要特性

### 🔐 安全可靠
- JWT身份认证系统
- RBAC权限控制机制
- 多角色用户管理（管理员、教师、学生）

### 📋 任务与主题管理
- 任务创建、分配与提交
- 主题讨论与互动
- 学习进度跟踪

### 💻 友好界面
- 现代化Web界面
- 响应式设计
- 简洁直观的用户体验

## 开发计划

### 已实现功能
- ✅ 项目基础架构搭建
- ✅ 多角色权限系统（管理员、教师、学生）
- ✅ 任务管理功能
- ✅ 主题讨论功能
- ✅ 用户管理功能

### 待开发功能
- ⬜ 知识资源管理系统
- ⬜ 文件上传处理功能
- ⬜ 数据可视化功能
- ⬜ AI模型集成
- ⬜ 实时通信功能

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

## 致谢

感谢所有开源项目的贡献者，特别是：
- FastAPI 团队
- Vue.js 团队
- Element Plus 团队
- Neo4j 团队

---

**注意**: 这是一个演示项目，部分功能使用模拟数据。在实际部署时需要连接真实的数据源和AI服务。
