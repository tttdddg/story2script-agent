"""
剧本质量报告生成服务

解析生成的 YAML 剧本，统计关键指标并生成优化建议。
不依赖大模型，纯规则驱动。
"""

import yaml

from app.schemas.response_schema import (
    CharacterAppearance,
    QualityReport,
    SceneDialogueStat,
)


def generate_report(yaml_content: str) -> QualityReport:
    """
    从 YAML 剧本内容生成质量报告。

    统计指标：
    - 章节数 / 场景数 / 人物数
    - 对白总数 / 动作描写总数
    - 冲突场景数
    - 每人物出场次数
    - 每场景对白数量

    生成优化建议：
    - 缺少 conflict 的场景
    - 对白偏少的场景
    - 主角出场次数过少
    - 缺少动作描写的场景
    """
    data = yaml.safe_load(yaml_content)
    if data is None:
        raise ValueError("YAML 内容为空")

    script = data.get("script", {})
    source = script.get("source", {})
    characters = data.get("characters", [])
    scenes = data.get("scenes", [])

    # ── 基础统计 ──
    chapter_count = source.get("chapter_count", 0) or 0
    scene_count = len(scenes)
    character_count = len(characters)

    dialogue_count = 0
    action_count = 0
    conflict_scene_count = 0
    character_appearances: dict[str, int] = {}
    scene_dialogue_stats: list[SceneDialogueStat] = []

    # 初始化人物出场计数器
    for char in characters:
        name = char.get("name", "")
        if name:
            character_appearances[name] = 0

    for i, scene in enumerate(scenes):
        scene_id = scene.get("scene_id", f"scene_{i + 1:03d}")

        # 对白统计
        dialogues = scene.get("dialogues", []) or []
        dialogue_count += len(dialogues)
        scene_dialogue_stats.append(SceneDialogueStat(
            scene_id=scene_id,
            dialogue_count=len(dialogues),
        ))

        # 动作统计
        actions = scene.get("actions", []) or []
        action_count += len(actions)

        # 冲突场景
        if scene.get("conflict"):
            conflict_scene_count += 1

        # 人物出场
        scene_characters = scene.get("characters", []) or []
        for char_name in scene_characters:
            if char_name in character_appearances:
                character_appearances[char_name] += 1

    # ── 生成建议 ──
    suggestions: list[str] = []

    # 找出主角（protagonist）
    protagonist_name = ""
    for char in characters:
        if char.get("role") == "protagonist":
            protagonist_name = char.get("name", "")
            break

    for i, scene in enumerate(scenes):
        scene_id = scene.get("scene_id", f"scene_{i + 1:03d}")

        # 1. 缺少 conflict
        if not scene.get("conflict"):
            suggestions.append(
                f"第 {i + 1} 场（{scene_id}）缺少明确的 'conflict' 字段，建议补充戏剧冲突。"
            )

        # 2. 对白偏少
        dialogues = scene.get("dialogues", []) or []
        if len(dialogues) < 2:
            suggestions.append(
                f"第 {i + 1} 场（{scene_id}）对白偏少（{len(dialogues)} 条），建议增加人物互动和对话。"
            )

        # 4. 缺少动作描写
        actions = scene.get("actions", []) or []
        if len(actions) == 0:
            suggestions.append(
                f"第 {i + 1} 场（{scene_id}）缺少 'actions' 动作描写，建议补充人物动作和舞台提示。"
            )

    # 3. 主角出场次数
    if protagonist_name and character_appearances.get(protagonist_name, 0) == 0:
        suggestions.append(
            f"主角「{protagonist_name}」在场景中未出场，请检查人物分配。"
        )
    elif protagonist_name:
        protagonist_appearances = character_appearances.get(protagonist_name, 0)
        if protagonist_appearances < scene_count // 2:
            suggestions.append(
                f"主角「{protagonist_name}」仅出场 {protagonist_appearances} 次（共 {scene_count} 场），"
                f"建议增加主角戏份。"
            )

    # ── 构造人物出场列表 ──
    appearance_list = [
        CharacterAppearance(name=name, count=count)
        for name, count in sorted(
            character_appearances.items(),
            key=lambda x: -x[1],
        )
    ]

    return QualityReport(
        chapter_count=chapter_count,
        scene_count=scene_count,
        character_count=character_count,
        dialogue_count=dialogue_count,
        action_count=action_count,
        conflict_scene_count=conflict_scene_count,
        character_appearances=appearance_list,
        scene_dialogue_stats=scene_dialogue_stats,
        suggestions=suggestions,
    )
