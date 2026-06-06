### PR 1：初始化前后端项目结构与基础 README

#### PR 标题

```text
PR 1: 初始化前后端项目结构与基础 README
```

#### 开发目标

搭建项目基础结构，保证前端和后端可以独立启动，为后续功能开发提供基础工程环境。

#### 主要功能

1. 创建项目仓库。
2. 初始化前端 Vue3 + TypeScript + Vite 项目。
3. 初始化后端 FastAPI 项目。
4. 创建基础目录结构。
5. 添加 `.gitignore`。
6. 添加 `.env.example`。
7. 编写 README 初稿。
8. 添加项目启动说明。

#### 具体做法

前端：

1. 使用 Vite 创建 Vue3 + TypeScript 项目。
2. 安装 Element Plus、Pinia、Axios、ECharts。
3. 创建基础页面 `HomeView.vue`。
4. 配置路由或先使用单页结构。

后端：

1. 创建 `backend/app/main.py`。
2. 添加 FastAPI 实例。
3. 添加健康检查接口：

```text
GET /api/health
```

1. 返回：

```json
{
  "status": "ok",
  "message": "Story2Script Agent backend is running"
}
```

文档：

1. README 写明项目简介。
2. README 写明技术栈。
3. README 写明本地运行方式。
4. README 写明 PR 开发计划。

#### 涉及文件

```text
README.md
.gitignore
frontend/
backend/
backend/app/main.py
backend/requirements.txt
backend/.env.example
docs/DEVELOPMENT_PLAN.md
```

#### 验收标准

1. 前端可以正常启动。
2. 后端可以正常启动。
3. 访问 `/api/health` 返回正常。
4. README 中有清晰的运行说明。
5. PR 描述清楚初始化内容。