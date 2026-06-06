### PR 6：新增 YAML 自动修复与导出功能

#### PR 标题

```text
PR 6: 新增 YAML 自动修复与导出功能
```

#### 开发目标

当生成的 YAML 不符合 Schema 时，系统可以基于校验错误调用大模型自动修复，并支持导出最终 YAML 文件。

#### 主要功能

1. 新增 YAML 修复 Prompt。
2. 调用大模型修复 YAML。
3. 修复后自动再次校验。
4. 返回修复说明。
5. 支持导出 `.yaml` 文件。
6. 前端新增修复和导出按钮。

#### 具体做法

后端：

1. 创建 `yaml_repairer.py`。
2. 创建 `repair_yaml.txt` Prompt。
3. 将原始 YAML 和校验错误传给模型。
4. 要求模型只修复格式和字段，不改变剧情。
5. 修复后调用 `yaml_validator.py` 再次校验。
6. 如果通过，保存 repaired_yaml。
7. 创建 `file_exporter.py`。
8. 提供导出接口。

前端：

1. 在 `ValidationPanel.vue` 中添加“自动修复”按钮。
2. 修复成功后更新 YAML 展示。
3. 添加“导出 YAML”按钮。
4. 下载文件名格式：`story2script_output.yaml`。

#### 修复 Prompt

```text
以下 YAML 未通过校验，请在不改变剧情内容的前提下修复格式和缺失字段。

校验错误：
{errors}

原始 YAML：
{yaml_content}

要求：
1. 只修复 YAML 格式、字段缺失和字段类型错误。
2. 不要删除已有有效内容。
3. speaker 必须来自 characters 中的 name。
4. 只输出修复后的 YAML。
```

#### 涉及文件

```text
backend/app/services/yaml_repairer.py
backend/app/services/file_exporter.py
backend/app/prompts/repair_yaml.txt
backend/app/api/routes_export.py
frontend/src/components/ValidationPanel.vue
frontend/src/components/YamlViewer.vue
```

#### 验收标准

1. 错误 YAML 可以被自动修复。
2. 修复后会再次校验。
3. 修复失败时能显示错误原因。
4. 用户可以导出 YAML 文件。
5. 导出的 YAML 文件可以正常打开。
6. 修复不会明显改变原剧情内容。

#### 测试方式

1. 使用缺字段 YAML 测试修复。
2. 使用 speaker 不一致 YAML 测试修复。
3. 使用语法错误 YAML 测试修复。
4. 测试导出文件是否能正常下载。