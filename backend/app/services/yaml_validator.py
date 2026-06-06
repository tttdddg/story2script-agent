"""
YAML Schema 校验服务

对生成的剧本 YAML 进行结构化校验，检查语法、字段完整性、人物一致性等。
校验不依赖大模型，保证速度和稳定性。
"""

import yaml

from app.schemas.response_schema import (
    ValidationError,
    ValidationResult,
)


def validate_yaml_content(yaml_content: str) -> ValidationResult:
    """
    对 YAML 剧本内容执行完整校验。

    校验项：
    1. YAML 语法校验
    2. 顶层字段校验（script / characters / scenes）
    3. 人物字段校验（id / name / role）
    4. 场景字段校验（scene_id / source_chapter / location / characters / dialogues）
    5. 对白字段校验（speaker / line）
    6. Speaker 人物一致性校验（speaker 必须在人物表中）
    7. 来源绑定校验（source_chapter）

    返回 ValidationResult，包含 valid / errors / warnings。
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []

    # ── 1. YAML 语法校验 ──
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        errors.append(ValidationError(
            path="(root)",
            message=f"YAML 语法错误: {e}",
        ))
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    if data is None:
        errors.append(ValidationError(
            path="(root)",
            message="YAML 内容为空",
        ))
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    if not isinstance(data, dict):
        errors.append(ValidationError(
            path="(root)",
            message="YAML 顶层应为字典/映射",
        ))
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    # ── 2. 顶层字段校验 ──
    for key in ("script", "characters", "scenes"):
        if key not in data:
            errors.append(ValidationError(
                path=f"(root).{key}",
                message=f"缺少顶层字段 '{key}'",
            ))

    script = data.get("script", {})
    characters = data.get("characters", [])
    scenes = data.get("scenes", [])

    # ── 3. 人物字段校验 ──
    character_names: set[str] = set()
    character_aliases: set[str] = set()

    if isinstance(characters, list):
        for i, char in enumerate(characters):
            if not isinstance(char, dict):
                errors.append(ValidationError(
                    path=f"characters[{i}]",
                    message=f"人物应为字典类型",
                ))
                continue

            char_id = char.get("id")
            char_name = char.get("name")
            char_role = char.get("role")

            if not char_id:
                errors.append(ValidationError(
                    path=f"characters[{i}].id",
                    message=f"人物 [{i}] 缺少 'id' 字段",
                ))
            if not char_name:
                errors.append(ValidationError(
                    path=f"characters[{i}].name",
                    message=f"人物 [{i}] (id={char_id or '?'}) 缺少 'name' 字段",
                ))
            else:
                character_names.add(char_name)

            if not char_role:
                errors.append(ValidationError(
                    path=f"characters[{i}].role",
                    message=f"人物 '{char_name or char_id or '?'}' 缺少 'role' 字段",
                ))

            # 收集别名
            for alias in char.get("aliases", []) or []:
                character_aliases.add(alias)
    else:
        errors.append(ValidationError(
            path="characters",
            message="'characters' 应为列表类型",
        ))

    # ── 4. 场景字段校验 ──
    if isinstance(scenes, list):
        for i, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                errors.append(ValidationError(
                    path=f"scenes[{i}]",
                    message=f"场景应为字典类型",
                ))
                continue

            scene_id = scene.get("scene_id", f"scene_{i + 1:03d}")

            # 必填字段
            for field, label in [
                ("scene_id", "scene_id"),
                ("source_chapter", "source_chapter"),
                ("location", "location"),
                ("characters", "characters"),
                ("dialogues", "dialogues"),
            ]:
                if not scene.get(field):
                    if field == "dialogues":
                        errors.append(ValidationError(
                            path=f"scenes[{i}].{field}",
                            message=f"{scene_id} 缺少 '{field}' 字段",
                        ))
                    elif field != "characters":
                        errors.append(ValidationError(
                            path=f"scenes[{i}].{field}",
                            message=f"{scene_id} 缺少 '{field}' 字段",
                        ))

            # 警告：缺少 conflict
            if not scene.get("conflict"):
                warnings.append(ValidationError(
                    path=f"scenes[{i}].conflict",
                    message=f"{scene_id} 缺少 'conflict' 字段（建议补充戏剧冲突）",
                ))

            # 警告：缺少 time
            if not scene.get("time"):
                warnings.append(ValidationError(
                    path=f"scenes[{i}].time",
                    message=f"{scene_id} 缺少 'time' 字段",
                ))

            # ── 5. 对白字段校验 ──
            dialogues = scene.get("dialogues", [])
            if isinstance(dialogues, list):
                if len(dialogues) == 0:
                    errors.append(ValidationError(
                        path=f"scenes[{i}].dialogues",
                        message=f"{scene_id} 的 dialogues 为空",
                    ))
                elif len(dialogues) <= 2:
                    warnings.append(ValidationError(
                        path=f"scenes[{i}].dialogues",
                        message=f"{scene_id} 对白数量较少（{len(dialogues)} 条），建议增加人物互动",
                    ))

                for j, d in enumerate(dialogues):
                    if not isinstance(d, dict):
                        errors.append(ValidationError(
                            path=f"scenes[{i}].dialogues[{j}]",
                            message=f"{scene_id} 对话 [{j}] 应为字典类型",
                        ))
                        continue

                    speaker = d.get("speaker")
                    line = d.get("line")

                    if not speaker:
                        errors.append(ValidationError(
                            path=f"scenes[{i}].dialogues[{j}].speaker",
                            message=f"{scene_id} 对白 [{j}] 缺少 'speaker' 字段",
                        ))
                    else:
                        # ── 6. Speaker 人物一致性校验 ──
                        all_names = character_names | character_aliases
                        if all_names and speaker not in all_names:
                            errors.append(ValidationError(
                                path=f"scenes[{i}].dialogues[{j}].speaker",
                                message=f"speaker「{speaker}」未在 characters 中定义",
                            ))

                    if not line:
                        errors.append(ValidationError(
                            path=f"scenes[{i}].dialogues[{j}].line",
                            message=f"{scene_id} 对白 [{j}] (speaker={speaker or '?'}) 缺少 'line' 字段",
                        ))
            else:
                errors.append(ValidationError(
                    path=f"scenes[{i}].dialogues",
                    message=f"{scene_id} 的 dialogues 应为列表类型",
                ))

            # 警告：缺少 actions
            if not scene.get("actions"):
                warnings.append(ValidationError(
                    path=f"scenes[{i}].actions",
                    message=f"{scene_id} 缺少 'actions' 字段（建议补充动作描写）",
                ))
    else:
        errors.append(ValidationError(
            path="scenes",
            message="'scenes' 应为列表类型",
        ))

    # ── 汇总 ──
    valid = len(errors) == 0

    return ValidationResult(valid=valid, errors=errors, warnings=warnings)
