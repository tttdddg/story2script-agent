# Story2Script Agent API 文档

## 概述

- **Base URL**: `http://localhost:8000/api`
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

所有响应均遵循以下格式：

- 成功：HTTP 2xx，返回 JSON 数据
- 失败：HTTP 4xx/5xx，返回 `{ "detail": "错误描述" }`

---

## 接口总览

| 序号 | 方法 | 路径 | 说明 | 依赖 LLM |
|------|------|------|------|----------|
| 1 | `GET` | `/api/health` | 健康检查 | ❌ |
| 2 | `POST` | `/api/projects` | 创建项目并上传小说 | ❌ |
| 3 | `POST` | `/api/projects/{id}/parse` | 重新解析章节 | ❌ |
| 4 | `POST` | `/api/projects/{id}/extract` | 抽取 Story Bible | ✅ |
| 5 | `POST` | `/api/projects/{id}/generate` | 生成剧本 YAML | ✅ |
| 6 | `POST` | `/api/projects/{id}/validate` | 校验 YAML | ❌ |
| 7 | `POST` | `/api/projects/{id}/repair` | 自动修复 YAML | ✅ |
| 8 | `GET` | `/api/projects/{id}/export` | 导出 YAML 文件 | ❌ |
| 9 | `GET` | `/api/projects/{id}/report` | 生成质量报告 | ❌ |

---

## 1. 健康检查

```http
GET /api/health
```

**响应 200**

```json
{
  "status": "ok",
  "message": "Story2Script Agent backend is running"
}
```

---

## 2. 创建项目并上传小说

```http
POST /api/projects
```

**请求体**

```json
{
  "title": "雨夜重逢",
  "novel_text": "第一章 退稿的傍晚\n\n林晚坐在咖啡馆……\n\n第二章 雨夜重逢\n\n……"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 项目/小说标题，最长 200 字符 |
| `novel_text` | string | 是 | 小说全文，须包含 ≥3 个标准章节标题 |

**支持的章节标题格式**

| 格式 | 示例 |
|------|------|
| 中文数字 | `第一章 退稿的傍晚` |
| 阿拉伯数字 | `第1章 开始` |
| 英文 | `Chapter 1 The Beginning` |
| 简单编号 | `一、背景介绍` |

**章节数不足 3 → 400**

```json
{
  "detail": "检测到 2 个章节，至少需要 3 个章节才能继续。请检查文本格式……"
}
```

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "title": "雨夜重逢",
  "chapter_count": 4,
  "word_count": 1021
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_id` | string | 项目唯一 ID，后续接口均需使用 |
| `title` | string | 项目标题 |
| `chapter_count` | int | 识别到的章节数量 |
| `word_count` | int | 小说总字数 |

---

## 3. 重新解析章节

对已有项目重新执行章节识别与拆分。

```http
POST /api/projects/{project_id}/parse
```

**路径参数**

| 参数 | 说明 |
|------|------|
| `project_id` | 项目 ID |

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "chapter_count": 4,
  "chapters": [
    {
      "chapter_id": "chapter_001",
      "title": "第一章 退稿的傍晚",
      "word_count": 199,
      "content": "林晚坐在老城区咖啡馆的角落……"
    },
    {
      "chapter_id": "chapter_002",
      "title": "第二章 雨夜重逢",
      "word_count": 230,
      "content": "雨越下越大……"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `chapters[].chapter_id` | string | 章节 ID，格式 `chapter_001` |
| `chapters[].title` | string | 识别到的章节标题 |
| `chapters[].word_count` | int | 该章节字数 |
| `chapters[].content` | string | 章节正文内容 |

**404** — 项目不存在

---

## 4. 抽取 Story Bible

调用 DeepSeek AI 从章节中抽取人物、地点、关键事件和人物关系。

```http
POST /api/projects/{project_id}/extract
```

**前置条件**：项目已通过章节解析（有 chapters 数据）

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "story_bible": {
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
      "出版社会议室"
    ],
    "key_events": [
      {
        "event_id": "event_001",
        "description": "女主收到退稿意见",
        "related_chapters": ["第一章 退稿的傍晚"],
        "related_characters": ["林晚"]
      }
    ],
    "relationships": [
      {
        "from": "林晚",
        "to": "周屿",
        "relation": "旧日恋人，三年前分开"
      }
    ]
  }
}
```

**角色类型（role）**

| 值 | 含义 |
|------|------|
| `protagonist` | 主角 |
| `antagonist` | 对手 |
| `supporting` | 重要配角 |
| `minor` | 次要角色 |

**400** — 无章节数据（需先解析章节）
**500** — LLM 调用失败或 API Key 无效

---

## 5. 生成剧本 YAML

调用 DeepSeek AI 基于章节和 Story Bible 生成结构化 YAML 剧本。

```http
POST /api/projects/{project_id}/generate
```

**前置条件**：项目已有 Story Bible（已执行 extract）

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "yaml_content": "script:\n  title: \"雨夜重逢\"\n  genre: \"都市情感短剧\"\n……",
  "scene_count": 4
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `yaml_content` | string | 完整 YAML 剧本文本 |
| `scene_count` | int | 生成的场景数量 |

**生成的 YAML 结构**详见 `docs/YAML_SCHEMA.md`，顶层包含 `script` / `characters` / `scenes`。

**400** — 无章节或 Story Bible 数据
**500** — LLM 调用或 YAML 解析失败

---

## 6. 校验 YAML

对生成的剧本 YAML 进行结构化校验，不依赖大模型，毫秒级响应。

```http
POST /api/projects/{project_id}/validate
```

**前置条件**：项目已有生成的 YAML（已执行 generate）

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "validation": {
    "valid": false,
    "errors": [
      {
        "path": "scenes[0].dialogues[0].speaker",
        "message": "speaker「小晚」未在 characters 中定义"
      }
    ],
    "warnings": [
      {
        "path": "scenes[2].conflict",
        "message": "scene_003 缺少 'conflict' 字段（建议补充戏剧冲突）"
      },
      {
        "path": "scenes[2].dialogues",
        "message": "scene_003 对白数量较少（1 条），建议增加人物互动"
      }
    ]
  }
}
```

**校验项**

| 序号 | 校验内容 | 级别 |
|------|----------|------|
| 1 | YAML 语法正确性 | error |
| 2 | 顶层字段完整性（script / characters / scenes） | error |
| 3 | 人物必填字段（id / name / role） | error |
| 4 | 场景必填字段（scene_id / source_chapter / location / dialogues） | error |
| 5 | 对白必填字段（speaker / line） | error |
| 6 | Speaker 与人物表一致性（含别名匹配） | error |
| 7 | 增强字段（conflict / time / actions / 对白数） | warning |

**400** — 无 YAML 数据
**404** — 项目不存在

---

## 7. 自动修复 YAML

将校验错误和原始 YAML 提交给大模型修复，修复后自动再次校验（最多 2 轮）。

```http
POST /api/projects/{project_id}/repair
```

**前置条件**：项目已有 YAML（已执行 generate）

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "repaired_yaml": "script:\n  title: \"雨夜重逢\"\n……",
  "valid": true,
  "repair_notes": [
    "第 1 次修复：3 个错误 → 0 个错误，修复成功"
  ],
  "remaining_errors": [],
  "remaining_warnings": [
    {
      "path": "scenes[0].actions",
      "message": "scene_001 缺少 'actions' 字段（建议补充动作描写）"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `repaired_yaml` | string | 修复后的完整 YAML |
| `valid` | bool | 修复后是否通过校验 |
| `repair_notes` | string[] | 每轮修复的记录 |
| `remaining_errors` | object[] | 仍未修复的错误 |
| `remaining_warnings` | object[] | 剩余的警告 |

**修复原则**
- 只修复格式和缺失字段，不改变剧情
- 优先修正 YAML 语法 → 补充字段 → 统一人物名称

**400** — 无 YAML 数据
**500** — LLM 修复失败

---

## 8. 导出 YAML 文件

下载生成的 YAML 剧本文件。

```http
GET /api/projects/{project_id}/export
```

**响应 200**

返回 YAML 文件下载流。

| 响应头 | 说明 |
|------|------|
| `Content-Type` | `application/x-yaml; charset=utf-8` |
| `Content-Disposition` | `attachment; filename="{标题}_{时间戳}.yaml"` |

文件名示例：`雨夜重逢_20260606_184429.yaml`

---

## 9. 生成质量报告

统计分析 YAML 剧本的各项指标并给出优化建议，不依赖大模型。

```http
GET /api/projects/{project_id}/report
```

**响应 200**

```json
{
  "project_id": "project_a1b2c3d4",
  "report": {
    "chapter_count": 4,
    "scene_count": 4,
    "character_count": 3,
    "dialogue_count": 7,
    "action_count": 10,
    "conflict_scene_count": 4,
    "character_appearances": [
      { "name": "林晚", "count": 4 },
      { "name": "周屿", "count": 2 },
      { "name": "陈姐", "count": 1 }
    ],
    "scene_dialogue_stats": [
      { "scene_id": "scene_001", "dialogue_count": 1 },
      { "scene_id": "scene_002", "dialogue_count": 2 }
    ],
    "suggestions": [
      "第 1 场（scene_001）对白偏少（1 条），建议增加人物互动和对话。"
    ]
  }
}
```

**优化建议规则**

| 规则 | 触发条件 |
|------|----------|
| 缺少冲突 | 场景无 `conflict` 字段 |
| 对白偏少 | 场景 `dialogues` < 2 条 |
| 主角戏份不足 | 主角出场次数 < 总场次的一半 |
| 缺少动作 | 场景无 `actions` 字段 |

---

## 完整工作流

```
POST /api/projects                    → project_id
POST /api/projects/{id}/parse         → chapters
POST /api/projects/{id}/extract       → story_bible (LLM)
POST /api/projects/{id}/generate      → yaml_content (LLM)
POST /api/projects/{id}/validate      → validation
POST /api/projects/{id}/repair        → repaired_yaml (LLM)
GET  /api/projects/{id}/report        → quality_report
GET  /api/projects/{id}/export        → 文件下载
```

---

## 错误码速查

| 状态码 | 含义 | 常见原因 |
|--------|------|----------|
| 200 | 成功 | — |
| 400 | 请求错误 | 章节不足 3、缺少前置数据、请求体格式错误 |
| 404 | 未找到 | 项目 ID 不存在 |
| 500 | 服务器错误 | LLM API Key 无效、网络超时、YAML 解析失败 |
