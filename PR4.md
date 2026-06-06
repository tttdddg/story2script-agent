### PR 4：新增剧本 YAML Schema 与剧本生成流程

#### PR 标题

```text
PR 4: 新增剧本 YAML Schema 与生成流程
```

#### 开发目标

定义剧本 YAML Schema，并基于小说文本和 Story Bible 生成结构化剧本 YAML。

#### 主要功能

1. 编写 `docs/YAML_SCHEMA.md`。
2. 定义剧本 YAML 顶层结构。
3. 新增剧本生成 Prompt。
4. 调用大模型生成 YAML。
5. 保存生成结果。
6. 前端展示 YAML 源码。

#### 具体做法

文档：

1. 在 `docs/YAML_SCHEMA.md` 中说明 Schema 结构。
2. 说明每个字段的作用。
3. 说明设计原因。
4. 给出完整 YAML 示例。

后端：

1. 创建 `script_generator.py`。
2. 创建 `generate_script_yaml.txt` Prompt。
3. 将小说文本、Story Bible、Schema 说明传给模型。
4. 要求模型只输出 YAML，不输出 Markdown 代码块。
5. 保存 `yaml_content`。

前端：

1. 创建 `YamlViewer.vue`。
2. 展示 YAML 内容。
3. 支持复制 YAML。
4. 支持切换“结构化预览 / YAML 源码”。

#### YAML Schema 设计原则

1. `script` 描述剧本整体信息。
2. `characters` 统一管理人物，减少人物漂移。
3. `scenes` 表示剧本场景，是核心内容。
4. 每个 scene 绑定 `source_chapter` 和 `source_excerpt`，保证可追溯。
5. `dialogues` 结构化记录对白，方便后续编辑和导出。
6. `conflict` 和 `dramatic_purpose` 用于强化剧本化表达。

#### 涉及文件

```text
docs/YAML_SCHEMA.md
backend/app/services/script_generator.py
backend/app/prompts/generate_script_yaml.txt
backend/app/schemas/script_schema.py
frontend/src/components/YamlViewer.vue
frontend/src/components/ScenePreview.vue
frontend/src/views/ScriptView.vue
```

#### 验收标准

1. 项目包含独立 YAML Schema 文档。
2. 可以生成 YAML 剧本。
3. YAML 中包含 `script`、`characters`、`scenes`。
4. 每个 scene 包含来源章节。
5. 前端可以展示 YAML 内容。
6. 生成结果可以复制。

#### 测试方式

1. 使用示例小说生成 YAML。
2. 检查 YAML 是否包含必要字段。
3. 检查人物是否来自 Story Bible。
4. 检查每个场景是否有 `source_chapter`。