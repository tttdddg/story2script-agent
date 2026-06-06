"""
YAML 自动修复服务

当校验发现错误时，将错误信息与原始 YAML 提交给大模型，
要求模型只修复格式和缺失字段，不改变剧情内容。
"""

from pathlib import Path

from app.services.llm_client import chat_completion
from app.services.yaml_validator import validate_yaml_content

# 修复 Prompt 模板路径
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "repair_yaml.txt"


def _load_repair_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"修复 Prompt 模板不存在: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def repair_yaml(yaml_content: str, errors: list[dict]) -> str:
    """
    调用大模型修复 YAML 中的错误。

    Args:
        yaml_content: 原始 YAML 文本
        errors: 错误列表，每项包含 path 和 message

    Returns:
        修复后的 YAML 文本
    """
    system_prompt = _load_repair_prompt()

    # 格式化错误列表
    error_lines = []
    for err in errors:
        error_lines.append(f"- [{err.get('path', '?')}] {err.get('message', '')}")
    error_text = "\n".join(error_lines)

    user_prompt = f"""## 校验错误列表

{error_text}

## 原始 YAML

{yaml_content}

请根据上述错误列表修复 YAML。只输出修复后的完整 YAML，不要添加任何解释、注释或 markdown 标记。"""

    response_text = chat_completion(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.2,
        json_mode=False,
    )

    # 提取 YAML
    import re
    yaml_match = re.search(r"```yaml\s*([\s\S]*?)```", response_text)
    if yaml_match:
        response_text = yaml_match.group(1).strip()

    # Also clean up code block without yaml marker
    code_match = re.search(r"```\s*([\s\S]*?)```", response_text)
    if code_match:
        response_text = code_match.group(1).strip()

    return response_text.strip()


def repair_and_validate(yaml_content: str) -> dict:
    """
    对 YAML 进行校验 → 修复 → 再校验的完整流程。

    最多尝试修复 2 次。如果修复后仍有错误，返回剩余错误。

    Returns:
        {
            "repaired_yaml": str,
            "valid": bool,
            "repair_notes": list[str],
            "remaining_errors": list,
            "remaining_warnings": list,
        }
    """
    max_attempts = 2
    repair_notes: list[str] = []
    current_yaml = yaml_content
    current_validation = validate_yaml_content(current_yaml)

    if current_validation.valid:
        return {
            "repaired_yaml": current_yaml,
            "valid": True,
            "repair_notes": ["YAML 已通过校验，无需修复"],
            "remaining_errors": [],
            "remaining_warnings": [],
        }

    original_errors = [e.model_dump() for e in current_validation.errors]

    for attempt in range(1, max_attempts + 1):
        # 调用 LLM 修复
        errors_to_fix = [e.model_dump() for e in current_validation.errors]
        repaired_yaml = repair_yaml(current_yaml, errors_to_fix)

        # 重新校验
        new_validation = validate_yaml_content(repaired_yaml)

        errors_before = len(current_validation.errors)
        errors_after = len(new_validation.errors)

        if errors_after == 0:
            repair_notes.append(
                f"第 {attempt} 次修复：{errors_before} 个错误 → 0 个错误，修复成功"
            )
            return {
                "repaired_yaml": repaired_yaml,
                "valid": True,
                "repair_notes": repair_notes,
                "remaining_errors": [],
                "remaining_warnings": [w.model_dump() for w in new_validation.warnings],
            }

        if errors_after < errors_before:
            repair_notes.append(
                f"第 {attempt} 次修复：{errors_before} 个错误 → {errors_after} 个错误"
            )
        else:
            repair_notes.append(
                f"第 {attempt} 次修复：错误数未减少（{errors_before} → {errors_after}），停止尝试"
            )
            break

        current_yaml = repaired_yaml
        current_validation = new_validation

    # 返回最后一次修复结果
    return {
        "repaired_yaml": repaired_yaml,
        "valid": new_validation.valid if new_validation.valid else False,
        "repair_notes": repair_notes,
        "remaining_errors": [e.model_dump() for e in new_validation.errors],
        "remaining_warnings": [w.model_dump() for w in new_validation.warnings],
    }
