# Story2Script 剧本 YAML Schema

## 设计目标

本 Schema 定义了 Story2Script Agent 生成的标准剧本 YAML 格式。设计遵循以下原则：

1. **可追溯**：每个场景绑定来源章节和原文片段
2. **结构化**：人物、对白、动作、舞台提示均为独立字段，方便程序化处理
3. **一致性**：人物统一在顶层声明，避免名称漂移
4. **可编辑**：YAML 格式可直接用文本编辑器修改，也可导入其他工具

## 顶层结构

```yaml
script:        # 剧本元信息
characters:    # 人物表（全局声明）
scenes:        # 场景列表（剧本核心）
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `script` | object | 是 | 剧本基本信息 |
| `characters` | array | 是 | 剧本涉及的所有人物 |
| `scenes` | array | 是 | 按顺序排列的场景列表 |

## script — 剧本元信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 剧本标题 |
| `genre` | string | 否 | 剧本类型（如 都市情感短剧） |
| `logline` | string | 否 | 一句话梗概 |
| `source` | object | 否 | 来源小说信息 |
| `source.chapter_count` | int | 否 | 原文章节数 |
| `source.word_count` | int | 否 | 原文总字数 |

## characters — 人物表

每个角色包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 唯一 ID，如 `char_001` |
| `name` | string | 是 | 角色名称 |
| `aliases` | array | 否 | 别名/昵称列表 |
| `role` | string | 是 | 角色类型：protagonist / antagonist / supporting / minor |
| `personality` | string | 否 | 性格描述 |
| `motivation` | string | 否 | 角色动机 |

**设计原因**：在顶层统一声明所有人物，场景中通过 `characters` 字段引用人物名称。这样可以在校验阶段检测人物名称是否与人物表一致，减少大模型生成时的"人物漂移"。

## scenes — 场景列表

每个场景包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scene_id` | string | 是 | 场景唯一 ID，如 `scene_001` |
| `source_chapter` | string | 是 | 来源章节标题 |
| `source_excerpt` | string | 否 | 原文相关片段 |
| `location` | string | 是 | 场景发生地点 |
| `time` | string | 否 | 时间（如 傍晚、第二天上午） |
| `characters` | array | 是 | 出场人物名称列表 |
| `dramatic_purpose` | string | 否 | 戏剧目的 |
| `conflict` | string | 否 | 核心冲突 |
| `actions` | array | 否 | 动作描写列表 |
| `dialogues` | array | 是 | 结构化对白列表 |
| `stage_directions` | array | 否 | 舞台提示列表 |

### 对白结构 (dialogues)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `speaker` | string | 是 | 说话人名称 |
| `emotion` | string | 否 | 情绪描述 |
| `line` | string | 是 | 台词内容 |

## 完整示例

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
  - id: "char_002"
    name: "周屿"
    role: "supporting"
    personality: "沉默但坚定"
    motivation: "弥补过去的遗憾"
  - id: "char_003"
    name: "陈姐"
    role: "supporting"
    personality: "理性、直接"
    motivation: "帮助作者完成商业化改编"

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

  - scene_id: "scene_002"
    source_chapter: "第二章 雨夜重逢"
    source_excerpt: "一个人从雨中推门而入。周屿收起黑色的长柄伞。"
    location: "老城区咖啡馆门口"
    time: "夜晚"
    characters: ["林晚", "周屿"]
    dramatic_purpose: "引入男主的再次出现"
    conflict: "暌违三年的重逢带来的复杂情绪"
    actions:
      - "周屿推门而入，伞尖雨水滴落。"
      - "林晚愣在原地，手指抓紧电脑包带子。"
    dialogues:
      - speaker: "周屿"
        emotion: "克制"
        line: "好久不见。"
      - speaker: "林晚"
        emotion: "震惊、复杂"
        line: "你怎么会在这里？"
    stage_directions:
      - "雨声渐大，两人之间隔着三张桌子。"
```

## Schema 校验项

以下校验项将在后续 PR 中实现：

| 校验项 | 说明 |
|--------|------|
| YAML 语法 | 检查缩进、冒号、列表格式 |
| 顶层字段 | 必须包含 `script`、`characters`、`scenes` |
| 人物 ID | 每个角色必须包含 `id`、`name`、`role` |
| 场景 ID | 每个场景必须包含 `scene_id`、`location`、`characters` |
| 对白字段 | 对白必须包含 `speaker`、`line` |
| 人物一致性 | `speaker` 必须在人物表中 |
| 来源绑定 | 每个 scene 必须包含 `source_chapter` |
