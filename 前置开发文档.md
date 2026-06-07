# Story2Script Agent 开发文档

## 1. 项目概述

### 1.1 项目名称

Story2Script Agent：AI 小说剧本结构化改编平台

### 1.2 项目定位

Story2Script Agent 是一款面向小说作者、短剧编剧和内容创作团队的 AI 辅助剧本创作工具。系统支持输入 3 个章节以上的小说文本，自动完成章节解析、人物信息抽取、场景拆分、结构化剧本生成、YAML Schema 校验、错误自动修复、剧本预览和 YAML 文件导出，帮助创作者快速获得可编辑、可追溯、可继续打磨的剧本初稿。

### 1.3 核心目标

本项目不是简单地将小说文本交给大模型生成剧本，而是构建一套完整的 AI 内容生产工作流：

小说文本输入
→ 章节识别
→ 人物、地点、事件抽取
→ Story Bible 构建
→ 场景拆分
→ 剧本 YAML 生成
→ Schema 校验
→ 错误自动修复
→ 结构化预览
→ 剧本质量报告
→ YAML 导出

### 1.4 主要解决的问题

1. 小说改编剧本耗时长，人工整理人物、场景和对白成本高。
2. 大模型直接生成剧本时容易出现格式不稳定、字段缺失、角色名混乱等问题。
3. 普通文本剧本不方便程序化处理、二次编辑和后续接入其他工具。
4. 作者难以追溯剧本场景来自小说原文的哪个章节和片段。
5. 剧本初稿缺少基础质量分析，不方便判断对白、冲突和人物出场是否合理。

------

## 2. 技术栈

### 2.1 前端技术栈

| 技术                     | 用途                                           |
| ------------------------ | ---------------------------------------------- |
| Vue 3                    | 前端主框架                                     |
| TypeScript               | 类型约束，提高代码可维护性                     |
| Vite                     | 前端构建工具                                   |
| Element Plus             | UI 组件库                                      |
| Pinia                    | 前端状态管理                                   |
| Axios                    | 请求后端 API                                   |
| ECharts                  | 剧本质量报告可视化                             |
| Monaco Editor / textarea | YAML 源码预览与编辑，时间不足时可先用 textarea |

### 2.2 后端技术栈

| 技术                    | 用途                                           |
| ----------------------- | ---------------------------------------------- |
| FastAPI                 | 后端 API 服务                                  |
| Python 3.10+            | 后端开发语言                                   |
| Pydantic                | 请求参数、响应结果和 Schema 校验               |
| PyYAML                  | YAML 解析与导出                                |
| DeepSeek API            | 大模型能力接入                                 |
| SQLite / 本地 JSON 文件 | 保存项目记录和生成结果，MVP 阶段避免复杂数据库 |
| Uvicorn                 | FastAPI 服务运行                               |
| python-dotenv           | 管理 API Key 等环境变量                        |

### 2.3 可选扩展技术

| 技术                    | 用途                           |
| ----------------------- | ------------------------------ |
| Redis                   | 缓存生成结果和任务状态         |
| PostgreSQL              | 后续正式版本存储项目和用户数据 |
| LangChain / LangChain4j | 后续扩展 Agent 工作流          |
| JSON Schema             | 更通用的 Schema 校验方式       |

### 2.4 本项目推荐最小技术组合

比赛周期较短，优先保证稳定演示，因此推荐：

前端：Vue3 + TypeScript + Element Plus + Pinia + Axios
后端：FastAPI + Pydantic + PyYAML + DeepSeek API
存储：本地 JSON 文件 / SQLite
可视化：ECharts

------

## 3. 功能模块设计

### 3.1 小说输入模块

功能：

1. 支持用户粘贴小说文本。
2. 支持上传 `.txt` 文件。
3. 检测文本是否包含 3 个以上章节。
4. 显示文本字数、章节数量和预计处理状态。
5. 提供内置原创示例小说，保证 Demo 演示稳定。

输入示例：

```text
第一章 退稿的傍晚
……

第二章 雨夜重逢
……

第三章 旧稿与新剧本
……
```

------

### 3.2 章节解析模块

功能：

1. 自动识别章节标题。
2. 将小说拆分为章节列表。
3. 支持常见章节格式：
   - 第一章
   - 第1章
   - Chapter 1
   - 一、标题
4. 对每个章节统计字数。
5. 将章节内容传递给后续 AI 分析流程。

输出结构示例：

```json
{
  "chapter_count": 3,
  "chapters": [
    {
      "chapter_id": "chapter_001",
      "title": "第一章 退稿的傍晚",
      "content": "……",
      "word_count": 1800
    }
  ]
}
```

------

### 3.3 Story Bible 抽取模块

Story Bible 是后续剧本生成的基础资料，相当于小说改编前的结构化设定表。

功能：

1. 抽取人物列表。
2. 抽取人物别名。
3. 抽取人物性格。
4. 抽取人物动机。
5. 抽取人物关系。
6. 抽取主要地点。
7. 抽取关键事件。
8. 抽取故事主线。

输出结构示例：

```json
{
  "characters": [
    {
      "id": "char_001",
      "name": "林晚",
      "aliases": ["小晚"],
      "role": "protagonist",
      "personality": "敏感、倔强、重视表达真实",
      "motivation": "坚持自己的创作方式"
    }
  ],
  "locations": [
    "老城区咖啡馆",
    "出版社会议室",
    "雨夜天桥"
  ],
  "key_events": [
    "女主收到退稿意见",
    "男主在雨夜重新出现",
    "两人围绕旧稿产生冲突"
  ]
}
```

------

### 3.4 剧本 YAML 生成模块

功能：

1. 根据小说章节和 Story Bible 生成剧本。
2. 输出 YAML 格式。
3. 每个场景包含地点、时间、人物、冲突、动作、对白、舞台提示和来源章节。
4. 对人物名称进行一致性约束。
5. 保留 `source_chapter` 和 `source_excerpt`，方便作者回查原文。

核心输出结构：

```yaml
script:
  title: "雨夜重逢"
  genre: "都市情感短剧"
  logline: "一位被退稿的小说作者在雨夜重逢旧人，被迫重新面对过去与创作的选择。"
  source:
    chapter_count: 3
    word_count: 5200

characters:
  - id: "char_001"
    name: "林晚"
    aliases: ["小晚"]
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

### 3.5 YAML Schema 校验模块

功能：

1. 检查 YAML 是否可以正常解析。
2. 检查顶层字段是否完整。
3. 检查每个场景的必要字段是否存在。
4. 检查对白中的 `speaker` 是否出现在人物表中。
5. 检查每个场景是否绑定 `source_chapter`。
6. 输出校验结果和错误列表。

校验内容：

| 校验项         | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| YAML 语法校验  | 检查缩进、冒号、列表格式是否正确                             |
| 顶层字段校验   | 必须包含 `script`、`characters`、`scenes`                    |
| 人物字段校验   | 人物必须包含 `id`、`name`、`role`                            |
| 场景字段校验   | 场景必须包含 `scene_id`、`location`、`characters`、`dialogues` |
| 对白字段校验   | 对白必须包含 `speaker`、`line`                               |
| 人物一致性校验 | `speaker` 必须存在于人物表                                   |
| 来源绑定校验   | 每个 scene 必须包含 `source_chapter`                         |

前端展示示例：

```text
✅ YAML 语法校验通过
✅ 顶层字段完整
✅ 所有场景均绑定来源章节
⚠️ scene_004 缺少 conflict 字段
⚠️ scene_006 的 speaker「小晚」未在 characters 中定义
```

------

### 3.6 YAML 自动修复模块

功能：

1. 当 YAML 校验失败时，将错误信息和原始 YAML 提交给大模型。
2. 要求模型只修复格式和缺失字段，不改变原剧情。
3. 修复后再次校验。
4. 如果仍然失败，返回错误详情给前端。

修复策略：

1. 优先修复 YAML 语法错误。
2. 再补充缺失字段。
3. 最后处理人物名称不一致问题。
4. 修复后保留原始内容，不随意删减有效信息。

------

### 3.7 结构化预览模块

功能：

1. 展示人物卡片。
2. 展示地点列表。
3. 展示关键事件。
4. 按场景展示剧本内容。
5. 支持 YAML 源码预览。
6. 支持复制和导出。

页面结构：

```text
左侧：小说章节列表 / 原文片段
中间：人物卡片 / 场景预览
右侧：YAML 源码 / 校验结果
```

MVP 阶段可简化为：

```text
上方：输入区
中间：生成结果区
下方：校验结果和导出按钮
```

------

### 3.8 剧本质量报告模块

功能：

1. 统计总章节数。
2. 统计总场景数。
3. 统计人物数量。
4. 统计对白数量。
5. 统计动作描写数量。
6. 统计每个人物出场次数。
7. 统计每个场景对白数量。
8. 检测缺少冲突的场景。
9. 给出简单优化建议。

报告示例：

```text
总章节数：3
总场景数：9
主要人物数：4
对白数量：46
动作描写数量：28
冲突场景数：7

优化建议：
1. 第 3 场对白偏少，可以增加人物目标冲突。
2. 第 6 场缺少明确 conflict 字段，建议补充戏剧冲突。
3. 林晚出场次数较高，周屿出场偏少，可适当增加对手戏。
```

------

## 4. 项目目录结构

### 4.1 总体目录

```text
story2script-agent/
  README.md
  docs/
    DEVELOPMENT_PLAN.md
    YAML_SCHEMA.md
    DEMO_GUIDE.md
  frontend/
  backend/
  samples/
    sample_novel.txt
    sample_output.yaml
```

### 4.2 前端目录

```text
frontend/
  package.json
  vite.config.ts
  src/
    main.ts
    App.vue
    api/
      project.ts
      generate.ts
    stores/
      projectStore.ts
    views/
      HomeView.vue
      AnalyzeView.vue
      ScriptView.vue
      ReportView.vue
    components/
      NovelInput.vue
      ChapterList.vue
      CharacterCards.vue
      ScenePreview.vue
      YamlViewer.vue
      ValidationPanel.vue
      QualityReport.vue
```

### 4.3 后端目录

```text
backend/
  requirements.txt
  .env.example
  app/
    main.py
    config.py
    api/
      routes_project.py
      routes_generate.py
      routes_validate.py
      routes_export.py
    services/
      chapter_parser.py
      llm_client.py
      story_extractor.py
      script_generator.py
      yaml_validator.py
      yaml_repairer.py
      report_generator.py
      file_exporter.py
    schemas/
      request_schema.py
      response_schema.py
      script_schema.py
    prompts/
      extract_story_bible.txt
      generate_script_yaml.txt
      repair_yaml.txt
    data/
      projects/
```

------

## 5. API 设计

### 5.1 创建项目 / 上传小说

接口：

```text
POST /api/projects
```

请求参数：

```json
{
  "title": "雨夜重逢",
  "novel_text": "第一章……第二章……第三章……"
}
```

返回结果：

```json
{
  "project_id": "project_001",
  "title": "雨夜重逢",
  "chapter_count": 3,
  "word_count": 5200
}
```

------

### 5.2 章节解析

接口：

```text
POST /api/projects/{project_id}/parse
```

返回结果：

```json
{
  "chapter_count": 3,
  "chapters": [
    {
      "chapter_id": "chapter_001",
      "title": "第一章 退稿的傍晚",
      "word_count": 1800
    }
  ]
}
```

------

### 5.3 Story Bible 抽取

接口：

```text
POST /api/projects/{project_id}/extract
```

返回结果：

```json
{
  "characters": [],
  "locations": [],
  "key_events": [],
  "relationships": []
}
```

------

### 5.4 剧本 YAML 生成

接口：

```text
POST /api/projects/{project_id}/generate
```

返回结果：

```json
{
  "yaml_content": "script:\n  title: ...",
  "scene_count": 9
}
```

------

### 5.5 YAML 校验

接口：

```text
POST /api/projects/{project_id}/validate
```

请求参数：

```json
{
  "yaml_content": "script:\n  title: ..."
}
```

返回结果：

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

------

### 5.6 YAML 自动修复

接口：

```text
POST /api/projects/{project_id}/repair
```

请求参数：

```json
{
  "yaml_content": "script:\n  title: ...",
  "errors": ["scene_004 缺少 conflict 字段"]
}
```

返回结果：

```json
{
  "repaired_yaml": "script:\n  title: ...",
  "valid": true,
  "repair_notes": ["已补充 scene_004 的 conflict 字段"]
}
```

------

### 5.7 剧本质量报告

接口：

```text
GET /api/projects/{project_id}/report
```

返回结果：

```json
{
  "chapter_count": 3,
  "scene_count": 9,
  "character_count": 4,
  "dialogue_count": 46,
  "action_count": 28,
  "conflict_scene_count": 7,
  "character_appearances": [
    {
      "name": "林晚",
      "count": 8
    }
  ],
  "suggestions": [
    "第 3 场对白偏少，可以增加人物目标冲突。"
  ]
}
```

------

### 5.8 导出 YAML

接口：

```text
GET /api/projects/{project_id}/export
```

返回：

```text
script.yaml
```