### PR 7：新增人物卡片、场景预览和剧本质量报告

#### PR 标题

```text
PR 7: 新增人物卡片、场景预览和剧本质量报告
```

#### 开发目标

完善前端展示效果，让 Demo 更直观，同时增加剧本质量报告，体现产品化和商业化价值。

#### 主要功能

1. 展示人物卡片。
2. 展示场景列表。
3. 展示每个场景的地点、时间、人物、冲突、动作和对白。
4. 展示来源章节和原文片段。
5. 生成剧本质量报告。
6. 使用 ECharts 展示人物出场次数和场景对白数量。

#### 具体做法

后端：

1. 创建 `report_generator.py`。
2. 从 YAML 中解析 scenes。
3. 统计：
   - 章节数
   - 场景数
   - 人物数
   - 对白数
   - 动作数
   - 冲突场景数
   - 人物出场次数
   - 每场对白数量
4. 输出优化建议。

前端：

1. 创建 `ScenePreview.vue`。
2. 创建 `QualityReport.vue`。
3. 使用卡片展示场景。
4. 使用 ECharts 展示统计图。
5. 在页面中展示优化建议。

#### 剧本质量报告规则

1. 如果某个 scene 没有 conflict，提示补充冲突。
2. 如果某个 scene 的 dialogues 数量小于 2，提示对白偏少。
3. 如果主角出场次数过少，提示人物存在感不足。
4. 如果动作描写为空，提示补充动作和舞台提示。

#### 涉及文件

```text
backend/app/services/report_generator.py
frontend/src/components/ScenePreview.vue
frontend/src/components/QualityReport.vue
frontend/src/views/ReportView.vue
```

#### 验收标准

1. 剧本可以结构化预览。
2. 人物卡片展示清楚。
3. 每个场景展示来源章节。
4. 质量报告统计正确。
5. 图表可以正常显示。
6. 页面适合 Demo 视频展示。

#### 测试方式

1. 使用示例 YAML 查看预览。
2. 检查人物出场次数是否准确。
3. 检查对白数量是否准确。
4. 删除 conflict 字段测试建议生成。