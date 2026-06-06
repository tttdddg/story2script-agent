# Story2Script Agent 开发计划

## 概述

本项目采用迭代式开发，每个 PR 对应一个独立的功能模块，逐步构建完整的 AI 小说剧本结构化改编平台。

## PR 开发路线图

### PR 1：初始化前后端项目结构与基础 README ✓

**目标**：搭建项目基础结构，保证前端和后端可以独立启动。

**内容**：
- 初始化前端 Vue3 + TypeScript + Vite 项目
- 安装 Element Plus、Pinia、Axios、ECharts
- 初始化后端 FastAPI 项目
- 添加健康检查接口 `GET /api/health`
- 创建 `.gitignore`、`.env.example`
- 编写 README

### PR 2：小说输入与章节解析

**目标**：实现小说文本输入和自动章节拆分。

**内容**：
- 前端：小说输入页面（粘贴文本 + 上传 `.txt`）
- 后端：章节解析服务，支持常见章节格式
- API：`POST /api/projects`、`POST /api/projects/{id}/parse`

### PR 3：Story Bible 抽取模块

**目标**：通过 AI 抽取人物、地点、事件等信息。

**内容**：
- 后端：接入 DeepSeek API
- 后端：实现 Story Bible 抽取服务
- API：`POST /api/projects/{id}/extract`

### PR 4：剧本 YAML 生成模块

**目标**：根据章节和 Story Bible 生成结构化剧本。

**内容**：
- 后端：YAML 生成服务
- 后端：生成 Prompt 模板
- API：`POST /api/projects/{id}/generate`

### PR 5：YAML Schema 校验与自动修复

**目标**：校验生成的 YAML，自动修复格式和字段问题。

**内容**：
- 后端：YAML Schema 校验服务
- 后端：自动修复服务
- API：`POST /api/projects/{id}/validate`、`POST /api/projects/{id}/repair`

### PR 6：结构化预览与导出

**目标**：前端展示剧本预览，支持导出 YAML 文件。

**内容**：
- 前端：人物卡片、场景预览组件
- 前端：YAML 源码预览
- 后端：YAML 导出接口
- API：`GET /api/projects/{id}/export`

### PR 7：剧本质量报告与可视化

**目标**：生成质量报告，ECharts 可视化展示。

**内容**：
- 后端：质量报告生成服务
- 前端：ECharts 图表展示
- API：`GET /api/projects/{id}/report`

### PR 8：内置 Demo 示例与联调优化

**目标**：内置示例小说，端到端联调，优化体验。

**内容**：
- 内置原创示例小说
- 端到端测试
- UI/UX 优化
- 文档完善
