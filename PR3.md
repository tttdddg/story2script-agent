### PR 3：新增人物、地点、关键事件抽取能力

#### PR 标题

```text
PR 3: 新增人物、地点和关键事件抽取能力
```

#### 开发目标

接入大模型能力，从小说章节中抽取 Story Bible，包括人物、地点、关键事件和人物关系，为后续剧本生成提供结构化基础。

#### 主要功能

1. 接入 DeepSeek API。
2. 新增统一 LLM 调用模块。
3. 新增 Story Bible 抽取 Prompt。
4. 抽取人物卡片。
5. 抽取地点列表。
6. 抽取关键事件。
7. 前端展示人物卡片和事件列表。

#### 具体做法

后端：

1. 创建 `llm_client.py`。
2. 从 `.env` 读取 `DEEPSEEK_API_KEY`。
3. 创建 `extract_story_bible.txt` Prompt 文件。
4. 创建 `story_extractor.py`。
5. 将章节文本传入大模型。
6. 要求模型输出 JSON。
7. 对返回结果做 JSON 解析。
8. 如果 JSON 解析失败，返回错误或进行简单修复。

前端：

1. 创建 `CharacterCards.vue`。
2. 创建地点展示区域。
3. 创建关键事件展示区域。
4. 调用 `/extract` 接口。
5. 展示抽取状态和结果。

#### Prompt 设计

```text
你是一名专业剧本策划，请阅读以下小说章节，抽取人物、地点、关键事件和人物关系。

要求：
1. 不要改写剧情。
2. 人物名称必须保持一致。
3. 如果同一人物存在别名，请放入 aliases 字段。
4. 输出 JSON，不要输出解释性文字。

输出字段：
characters, locations, key_events, relationships, timeline
```

#### 涉及文件

```text
backend/app/services/llm_client.py
backend/app/services/story_extractor.py
backend/app/prompts/extract_story_bible.txt
backend/app/api/routes_generate.py
frontend/src/components/CharacterCards.vue
frontend/src/views/AnalyzeView.vue
```

#### 验收标准

1. 可以成功调用大模型。
2. 可以返回人物列表。
3. 可以返回地点列表。
4. 可以返回关键事件。
5. 前端可以结构化展示 Story Bible。
6. 接口失败时有错误提示。

#### 测试方式

1. 使用示例小说测试抽取结果。
2. 删除 API Key 测试错误提示。
3. 使用短文本测试异常情况。
4. 检查人物名称是否基本一致。