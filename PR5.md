### PR 5：新增 YAML 结构校验与人物一致性检查

#### PR 标题

```text
PR 5: 新增 YAML 结构校验与人物一致性检查
```

#### 开发目标

实现 YAML 校验机制，检查大模型生成结果是否符合 Schema，提升系统稳定性和工程完整度。

#### 主要功能

1. YAML 语法校验。
2. 顶层字段校验。
3. 人物字段校验。
4. 场景字段校验。
5. 对白字段校验。
6. speaker 人物一致性校验。
7. 前端展示校验结果。

#### 具体做法

后端：

1. 创建 `yaml_validator.py`。
2. 使用 PyYAML 解析 YAML。
3. 如果解析失败，返回语法错误。
4. 检查顶层字段：
   - `script`
   - `characters`
   - `scenes`
5. 检查人物字段：
   - `id`
   - `name`
   - `role`
6. 检查场景字段：
   - `scene_id`
   - `source_chapter`
   - `location`
   - `time`
   - `characters`
   - `conflict`
   - `dialogues`
7. 检查对白字段：
   - `speaker`
   - `line`
8. 将所有 characters.name 建立集合。
9. 检查 dialogue.speaker 是否在集合中。
10. 返回 errors 和 warnings。

前端：

1. 创建 `ValidationPanel.vue`。
2. 显示校验通过项。
3. 显示错误和警告。
4. 提供“自动修复”按钮入口。

#### 校验返回示例

```json
{
  "valid": false,
  "errors": [
    {
      "path": "scenes[3].conflict",
      "message": "scene_004 缺少 conflict 字段"
    },
    {
      "path": "scenes[5].dialogues[0].speaker",
      "message": "speaker「小晚」未在 characters 中定义"
    }
  ],
  "warnings": [
    {
      "path": "scenes[2].dialogues",
      "message": "该场景对白数量较少"
    }
  ]
}
```

#### 涉及文件

```text
backend/app/services/yaml_validator.py
backend/app/api/routes_validate.py
frontend/src/components/ValidationPanel.vue
frontend/src/api/generate.ts
```

#### 验收标准

1. 可以校验合法 YAML。
2. 可以识别 YAML 语法错误。
3. 可以识别缺失字段。
4. 可以识别 speaker 不一致。
5. 前端可以清晰展示校验结果。
6. 校验接口不依赖大模型，保证速度稳定。

#### 测试方式

1. 使用正确 YAML 测试。
2. 手动删除 `conflict` 字段测试。
3. 手动写错 YAML 缩进测试。
4. 手动修改 speaker 名称测试。