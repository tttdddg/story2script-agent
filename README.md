# Story2Script Agent：AI小说剧本结构化改编系统

面向小说作者、短剧编剧和内容创作团队的 AI 辅助剧本创作工具。
支持将**3 个章节以上的小说文本**自动转换为**结构化YAML格式剧本初稿**，并提供Story Bible抽取、剧本预览、YAML Schema校验和文件导出能力。

#### 视频网盘链接：https://pan.baidu.com/s/1tYoQYrG8UEovg2R9rCHWLA?pwd=vd5b 

本项目按照功能模块拆分PR，保证每个PR聚焦单一功能点，并在主分支保持可运行状态，具体实际PR记录请以GitHub Pull Request页面为准,其中要求额外定义剧本的YAML Schema文档位于项目的samples/sample_output.yaml。

**本项目仅用于七牛云 × XEngineer 暑期实训营作品展示与学习交流。**
**如需进一步使用或改造，请遵守相关平台规则和知识产权要求。**
#### 提交说明


本项目核心功能开发已在实训营规定时间内完成，截止时间后产生的提交仅用于处理GitHub推送冲突,该提交不涉及核心功能新增或业务逻辑开发，仅用于保证仓库可正常访问、README信息完整以及提交材料符合规范。

------

## 1. 在线演示与提交材料

| 内容             | 链接                                                         |
| ---------------- | ------------------------------------------------------------ |
| Demo 视频        | https://pan.baidu.com/s/1tYoQYrG8UEovg2R9rCHWLA?pwd=vd5b / 代码仓库里下载 |
| 代码仓库         | [tttdddg/story2script-agent](https://github.com/tttdddg/story2script-agent) |
| YAML Schema 文档 | [docs/YAML_SCHEMA.md](https://chatgpt.com/c/docs/YAML_SCHEMA.md) |
| 示例小说文本     | [samples/sample_novel.txt](https://chatgpt.com/c/samples/sample_novel.txt) |
| 示例 YAML 输出   | [samples/sample_output.yaml](https://chatgpt.com/c/samples/sample_output.yaml) |

注意：Demo 视频链接已放置在 README 顶部显眼位置，便于评委快速查看作品效果。

------

## 2. 项目简介

Story2Script Agent是一个AI小说剧本结构化改编系统，面向小说作者、短剧编剧和内容创作者，帮助用户将长篇小说章节快速转换为可编辑、可校验、可继续打磨的 YAML 格式剧本初稿。

系统并不是简单地将小说文本交给大模型生成一段普通剧本文本，而是将小说改编过程拆解为多个结构化步骤：

```text
小说输入
→ 章节解析
→ Story Bible 抽取
→ 剧本 YAML 生成
→ YAML Schema 校验
→ 结构化剧本预览
→ YAML 文件导出
```

通过这种AI工作流设计，系统能够在生成剧本初稿的同时，尽量保证人物、场景、对白和来源章节之间的结构一致性，降低小说作者将作品改编为剧本的门槛。

------

## 3. 选题背景

很多小说作者希望将自己的作品改编为短剧、广播剧、舞台剧或影视剧本，但在实际创作过程中通常会遇到以下问题：

1. 小说文本较长，人工整理人物、地点、事件和场景成本较高。
2. 小说叙事语言与剧本语言差异较大，需要重新拆分场景、动作和对白。
3. 普通大模型直接生成剧本时，容易出现格式不统一、字段缺失、人物名称混乱等问题。
4. 作者需要一个可编辑、可追溯、可进一步打磨的结构化剧本初稿，而不是一次性生成的散文式文本。
5. 后续如果要接入剧本编辑器、短剧制作平台或自动化内容工作流，结构化 YAML 格式更方便扩展。

因此，本项目围绕“小说文本 → 结构化剧本 YAML”的核心任务，设计了一套轻量级 AI 剧本改编工作流。

------

## 4. 核心功能

### 4.1 小说输入与章节解析

- 支持粘贴小说文本。
- 支持加载内置示例小说。
- 自动识别章节标题。
- 校验小说是否满足 **3 个章节以上** 的题目要求。
- 统计小说字数、章节数量和章节列表。

### 4.2 Story Bible抽取

系统会先从小说中抽取Story Bible，用于后续剧本生成。

Story Bible 包括：

- 人物列表
- 人物身份
- 人物性格
- 人物关系
- 主要地点
- 关键事件
- 故事主线

这样可以减少大模型直接生成剧本时出现的人物漂移、角色混乱和剧情不一致问题。

### 4.3 剧本YAML生成

系统基于小说内容和Story Bible，生成结构化YAML格式剧本。

剧本内容包括：

- 剧本标题
- 剧本类型
- 故事简介
- 人物表
- 场景列表
- 场景来源章节
- 场景地点和时间
- 出场人物
- 场景冲突
- 动作描写
- 人物对白
- 情绪标注
- 舞台 / 镜头提示

### 4.4 YAML Schema校验

系统会对生成的 YAML 进行结构化校验，检查内容是否符合预设Schema。

校验内容包括：

- YAML 语法是否正确
- 顶层字段是否完整
- `script`、`characters`、`scenes` 是否存在
- 每个scene是否包含必要字段
- 每句对白的speaker是否存在于人物表中
- 每个场景是否绑定来源章节

### 4.5 结构化剧本预览

系统支持将生成的YAML剧本转换为更直观的结构化预览。

预览内容包括：

- 人物卡片
- 场景卡片
- 场景冲突
- 动作描写
- 人物对白
- 来源章节
- 原文片段

### 4.6 YAML 文件导出

用户可以将生成后的剧本导出为 `.yaml` 文件，便于后续继续编辑、保存或接入其他剧本创作工具。

------

## 5. 项目亮点

### 5.1 Schema First：先定义结构，再生成内容

本项目不是直接让大模型自由生成剧本，而是先定义剧本YAML Schema，再引导模型按照Schema输出结构化内容，这样可以提高输出结果的稳定性和可解析性。

### 5.2 Story Bible：先理解小说，再改编剧本

系统在生成剧本前，会先抽取人物、地点、事件和关系，形成Story Bible。

这样可以提升多章节小说改编时的人物一致性和剧情连贯性。

### 5.3 YAML Validate：对大模型输出进行结构校验

大模型生成结果可能存在格式不稳定、字段缺失、角色名称不一致等问题。

系统通过YAML Schema校验机制，对生成结果进行检查，提升作品的工程完整度。

### 5.4 Source Trace：保留剧本与原文的映射关系

每个剧本场景都包含 `source_chapter` 和 `source_excerpt` 字段，方便作者回查该场景来自小说原文的哪个章节和片段。

### 5.5 可编辑、可扩展、可二次创作

YAML格式天然适合结构化编辑、版本管理和后续扩展。

后续可以进一步接入：

- 剧本编辑器
- 短剧分镜生成
- 角色配音
- 剧本杀创作
- 广播剧脚本生成
- 多版本改写与对比

------

## 6. 系统流程

```text
┌────────────────────┐
│  小说文本输入       │
│  粘贴 / 示例文本    │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  章节解析           │
│  识别章节 / 统计字数 │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  Story Bible 抽取   │
│  人物 / 地点 / 事件 │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  剧本 YAML 生成     │
│  场景 / 动作 / 对白 │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  YAML Schema 校验   │
│  字段 / 人物一致性  │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  预览与导出         │
│  场景卡片 / YAML文件 │
└────────────────────┘
```

------

## 7. 系统架构

```text
story2script-agent
├── frontend                 # 前端项目
│   ├── src
│   │   ├── api              # API 请求封装
│   │   ├── components       # 页面组件
│   │   ├── stores           # 状态管理
│   │   └── views            # 页面视图
│   └── package.json
│
├── backend                  # 后端项目
│   ├── app
│   │   ├── api              # 后端路由
│   │   ├── services         # 核心业务逻辑
│   │   ├── schemas          # 请求与响应结构
│   │   ├── prompts          # Prompt 模板
│   │   └── main.py          # FastAPI 入口
│   └── requirements.txt
│
├── docs                     # 项目文档
│   ├── YAML_SCHEMA.md       # YAML Schema 设计文档
│   ├── DEVELOPMENT_PLAN.md  # 开发计划
│   └── DEMO_GUIDE.md        # Demo 使用说明
│
├── samples                  # 示例数据
│   ├── sample_novel.txt
│   └── sample_output.yaml
│
├── README.md
└── .gitignore
```

------

## 8. 技术栈

### 8.1 前端

| 技术         | 说明         |
| ------------ | ------------ |
| Vue 3        | 前端主框架   |
| TypeScript   | 类型约束     |
| Vite         | 前端构建工具 |
| Element Plus | UI 组件库    |
| Pinia        | 状态管理     |
| Axios        | 请求后端接口 |

### 8.2 后端

| 技术          | 说明                   |
| ------------- | ---------------------- |
| FastAPI       | 后端 API 服务          |
| Python 3.10+  | 后端开发语言           |
| Pydantic      | 参数校验与数据结构定义 |
| PyYAML        | YAML 解析与校验        |
| DeepSeek API  | 大模型能力接入         |
| python-dotenv | 环境变量管理           |

### 8.3 数据存储

本项目为实训营MVP作品，当前阶段采用本地JSON / YAML文件保存中间结果和示例输出，减少数据库部署依赖，保证评委可以快速启动和复现Demo。

后续正式版本可扩展为：

- MySQL / PostgreSQL 项目存储
- Redis 生成任务缓存
- 用户历史项目管理
- 剧本版本管理
- 多用户协同编辑

------

## 9. 本地运行方式

### 9.1 克隆项目

```bash
git clone 请填写你的仓库地址
cd story2script-agent
```

------

### 9.2 后端启动

进入后端目录：

```bash
cd backend
```

创建虚拟环境：

```bash
python -m venv venv
```

激活虚拟环境：

Windows：

```bash
venv\Scripts\activate
```

macOS / Linux：

```bash
source venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

#### 🔑 API Key 配置（重要）

本项目使用 DeepSeek API 提供 AI 能力。为了保护 API Key 安全：

- **`.env` 已加入 `.gitignore`**，不会被提交到 Git 仓库
- **`.env.example` 已提交**，评委可参考其格式自行配置

**方式一：配置真实 API Key（推荐）**

1. 前往 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并获取 API Key
2. 创建环境变量文件：
   ```bash
   cp .env.example .env
   ```
3. 编辑 `.env`，填入你的 API Key：
   ```env
   DEEPSEEK_API_KEY=sk-your_actual_api_key_here
   ```
4. 正常启动后端，系统将调用 DeepSeek API 处理你输入的小说文本

**方式二：无 Key 自动 Demo 模式**

如果评委没有 DeepSeek API Key，**无需任何额外配置**：
- 系统会自动检测 API Key 是否配置
- 未配置时自动进入 **Demo 模式**
- Demo 模式使用基于示例小说（`samples/sample_novel.txt`）预计算的数据
- 评委仍可完整体验：章节解析 → Story Bible → 剧本生成 → Schema 校验 → 导出的全流程
- 健康检查接口会返回 `demo_mode: true`，方便前端展示 Demo 状态

启动后端服务：

```bash
uvicorn app.main:app --reload
```

默认后端地址：

```text
http://localhost:8000
```

健康检查接口：

```text
GET http://localhost:8000/api/health
```

响应示例（含 API Key 状态）：

```json
{
  "status": "ok",
  "message": "Story2Script Agent backend is running",
  "demo_mode": false,
  "api_key_configured": true
}
```

------

### 9.3 前端启动

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

创建前端环境变量文件：

```bash
cp .env.example .env
```

配置后端 API 地址：

```env
VITE_API_BASE_URL=http://localhost:8000
```

启动前端：

```bash
npm run dev
```

默认前端地址：

```text
http://localhost:5173
```

------

## 10. 使用说明

### 10.1 基础使用流程

1. 打开系统首页。
2. 点击“加载示例小说”或粘贴自己的小说文本。
3. 点击“解析小说”，系统自动识别章节并统计字数。
4. 点击“抽取 Story Bible”，系统生成角色、地点和关键事件。
5. 点击“生成剧本 YAML”，系统输出结构化剧本。
6. 点击“Schema 校验”，系统检查 YAML 结构是否符合规范。
7. 查看结构化剧本预览。
8. 点击“导出 YAML”，保存剧本初稿。



## 11. YAML Schema 设计说明

本项目额外编写了剧本YAML Schema文档，用于说明结构化剧本的字段定义和设计原因。

文档位置：[docs/YAML_SCHEMA.md](https://chatgpt.com/c/docs/YAML_SCHEMA.md)

### 11.1 Schema 顶层结构

```yaml
script:
  title:
  genre:
  logline:

characters:
  - id:
    name:
    role:
    personality:
    motivation:

scenes:
  - scene_id:
    source_chapter:
    source_excerpt:
    location:
    time:
    characters:
    dramatic_purpose:
    conflict:
    actions:
    dialogues:
      - speaker:
        emotion:
        line:
    stage_directions:
```

### 11.2 字段设计原因

| 字段               | 设计原因                                         |
| ------------------ | ------------------------------------------------ |
| `script`           | 描述剧本整体信息，包括标题、类型和一句话简介     |
| `characters`       | 统一管理人物信息，减少多章节改编中的人物名称漂移 |
| `scenes`           | 剧本的核心单位，方便按场景组织动作、对白和冲突   |
| `source_chapter`   | 记录场景来自哪个小说章节，方便作者回查           |
| `source_excerpt`   | 保留原文片段，提高生成结果可追溯性               |
| `conflict`         | 剧本比小说更强调戏剧冲突，因此单独设计该字段     |
| `dialogues`        | 将人物对白结构化，方便后续编辑、导出和二次生成   |
| `emotion`          | 标注台词情绪，便于后续配音、表演或短剧制作       |
| `stage_directions` | 记录舞台 / 镜头提示，增强剧本可拍摄性            |

------

## 12. 示例输入与输出

### 12.1 示例输入

示例小说文本位于：[samples/sample_novel.txt](https://chatgpt.com/c/samples/sample_novel.txt)

示例结构：

```text
第一章 退稿的傍晚
……

第二章 雨夜重逢
……

第三章 旧稿与新剧本
……
```

------

### 12.2 示例输出

示例 YAML 输出位于：[samples/sample_output.yaml](https://chatgpt.com/c/samples/sample_output.yaml)

部分输出示例：

```yaml
script:
  title: "雨夜重逢"
  genre: "都市情感短剧"
  logline: "一位被退稿的小说作者在雨夜重逢旧人，被迫重新面对过去与创作的选择。"

characters:
  - id: "char_001"
    name: "林晚"
    role: "protagonist"
    personality: "敏感、倔强、重视表达真实"
    motivation: "坚持自己的创作方式"

scenes:
  - scene_id: "scene_001"
    source_chapter: "第一章 退稿的傍晚"
    source_excerpt: "林晚坐在咖啡馆角落，看着编辑发来的修改意见。"
    location: "老城区咖啡馆"
    time: "傍晚"
    characters: ["林晚", "陈姐"]
    dramatic_purpose: "引出女主的创作困境"
    conflict: "商业化修改要求与作者表达之间的冲突"
    actions:
      - "林晚低头看着电脑屏幕，手指停在删除键上。"
    dialogues:
      - speaker: "陈姐"
        emotion: "理性、急切"
        line: "你这个故事有情绪，但缺少能抓住观众的冲突。"
      - speaker: "林晚"
        emotion: "压抑"
        line: "如果所有沉默都要改成争吵，那它还是我的故事吗？"
    stage_directions:
      - "窗外开始下雨，咖啡馆灯光变暗。"
```

------

## 13. API 接口说明

### 13.1 健康检查

```http
GET /api/health
```

返回示例：

```json
{
  "status": "ok",
  "message": "Story2Script Agent backend is running"
}
```

------

### 13.2 章节解析

```http
POST /api/parse
```

请求示例：

```json
{
  "novel_text": "第一章……第二章……第三章……"
}
```

返回示例：

```json
{
  "chapter_count": 3,
  "word_count": 5200,
  "chapters": [
    {
      "chapter_id": "chapter_001",
      "title": "第一章 退稿的傍晚",
      "word_count": 1700
    }
  ]
}
```

------

### 13.3 Story Bible 抽取

```http
POST /api/extract
```

请求示例：

```json
{
  "novel_text": "第一章……第二章……第三章……",
  "chapters": []
}
```

返回示例：

```json
{
  "characters": [],
  "locations": [],
  "key_events": [],
  "relationships": []
}
```

------

### 13.4 剧本 YAML 生成

```http
POST /api/generate
```

请求示例：

```json
{
  "novel_text": "第一章……第二章……第三章……",
  "story_bible": {}
}
```

返回示例：

```json
{
  "yaml_content": "script:\n  title: ...",
  "scene_count": 8
}
```

------

### 13.5 YAML Schema 校验

```http
POST /api/validate
```

请求示例：

```json
{
  "yaml_content": "script:\n  title: ..."
}
```

返回示例：

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

------

## 14. 页面说明

系统采用单页 AI 创作工作台布局，减少页面跳转，让评委和用户能够快速理解完整流程。

页面主要分为：

1. 顶部项目介绍区
2. 小说输入与章节解析区
3. Story Bible 展示区
4. 剧本 YAML 生成区
5. 结构化剧本预览区
6. YAML Schema 校验区
7. YAML 导出区

这种布局适合 Demo 展示，能够在一个页面中完整呈现“小说 → 剧本 YAML → 校验 → 导出”的核心链路。

------

## 15. 当前版本说明

当前版本为实训营 MVP 版本，重点完成题目核心要求：

- 3 个章节以上小说文本输入
- 自动转换为结构化剧本 YAML
- 额外提供 YAML Schema 文档
- 说明 Schema 字段设计原因
- 提供结构化预览与校验
- 支持 YAML 导出

当前版本暂未引入登录注册、用户权限、历史项目管理和数据库存储。

原因是本项目优先聚焦题目要求中的核心创作流程，保证小说改编、结构化生成、Schema 校验和 Demo 演示稳定可用。

------

## 16. 后续优化方向

后续可以从以下方向继续扩展：

1. **用户系统**
   - 登录注册
   - 个人项目管理
   - 历史剧本保存
2. **版本管理**
   - 多版本剧本对比
   - 修改记录
   - 一键回滚
3. **自动修复增强**
   - 更精细的 YAML 修复
   - 字段缺失自动补全
   - 人物名称统一
4. **创作风格控制**
   - 短剧风格
   - 影视剧风格
   - 舞台剧风格
   - 广播剧风格
5. **多轮编辑能力**
   - 用户指定修改某个场景
   - 增加冲突
   - 改写对白
   - 压缩剧情
6. **剧本质量分析**
   - 人物出场频率
   - 对白占比
   - 冲突密度
   - 场景节奏
7. **平台化能力**
   - MySQL / PostgreSQL 持久化存储
   - Redis 任务缓存
   - 多用户协同编辑
   - 在线剧本编辑器

------

## 17. 第三方依赖说明

本项目使用以下主要第三方依赖：

### 前端依赖

- Vue 3
- TypeScript
- Vite
- Element Plus
- Pinia
- Axios

### 后端依赖

- FastAPI
- Uvicorn
- Pydantic
- PyYAML
- python-dotenv
- requests / httpx

### AI 能力

- DeepSeek API

所有第三方依赖均用于项目工程实现和 AI 能力调用，不包含未经授权的第三方作品内容。

------

## 18. 原创性与知识产权说明

本项目为七牛云 × XEngineer 暑期实训营第三批次议题作品，围绕“AI 小说转剧本工具”题目要求进行开发。

项目说明如下：

1. 本项目代码在实训营规定开发周期内完成。

2. 项目核心功能围绕小说解析、Story Bible 抽取、剧本 YAML 生成、Schema 校验和导出流程自主实现。

3. 项目使用的第三方依赖已在 README 中列明。

4. 示例小说文本仅用于功能演示，不涉及第三方版权内容。

5. 项目未提交真实 API Key（`.env` 已加入 `.gitignore`，仅提交 `.env.example` 模板），相关密钥通过环境变量配置；未配置 Key 时系统自动进入 Demo 模式，使用预计算示例数据。

6. 如复用了本人过往项目中的通用代码组织方式或工程经验，均已根据本项目需求重新实现，不涉及往期参赛作品核心业务代码复用。

7. 本项目的知识产权归提交者所有。

   

## 19.相关说明

### 为什么没有登录注册？

本项目是围绕实训营题目要求开发的 MVP 版本，题目核心是将 3 个章节以上小说文本转换为结构化剧本 YAML，并提供 YAML Schema 文档。

因此当前版本优先保证小说改编、YAML 生成、Schema 校验和导出流程完整稳定。登录注册、用户权限和历史项目管理属于后续平台化扩展方向。

### 为什么使用YAML？

YAML 结构清晰、可读性强，适合表示剧本中的人物、场景、动作、对白和舞台提示。相比普通文本，YAML 更方便后续编辑、校验、导出和接入其他工具链。

### 为什么需要Story Bible？

小说通常包含多个人物、地点和事件。直接让大模型生成剧本容易导致人物名称混乱或剧情不一致。Story Bible 可以先统一人物、地点和关键事件信息，再用于后续剧本生成。

### 为什么需要 Schema校验？

大模型输出结构化内容时可能出现字段缺失、格式错误或人物名称不一致。Schema 校验可以提高输出稳定性，让生成结果更适合作为可编辑的剧本初稿。

### 项目后续如何扩展？

后续可以扩展为完整的 AI 剧本创作平台，支持用户登录、历史项目管理、多版本剧本、自动修复、多轮改写、剧本质量分析和协同编辑。

------

## 20. 项目总结

Story2Script Agent 聚焦小说作者将作品改编为剧本时的真实需求，通过 AI 工作流将小说理解、人物抽取、剧本生成、Schema 校验和文件导出串联起来，形成一个完整的 AI 辅助剧本创作闭环。

相比普通文本生成工具，本项目更强调：

- 结构化输出
- 格式可校验
- 结果可编辑
- 内容可追溯
- 后续可扩展

最终目标是帮助创作者更快获得可继续打磨的剧本初稿，降低小说改编剧本的门槛，提升内容创作效率。
