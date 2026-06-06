"""
剧本 YAML 生成服务

将小说章节和 Story Bible 提交给大模型，生成结构化 YAML 剧本。
"""

import json
import re
from pathlib import Path

import yaml

from app.schemas.script_schema import ScriptYaml
from app.services.llm_client import chat_completion

# Prompt 模板路径
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "generate_script_yaml.txt"


def _load_prompt_template() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt 模板文件不存在: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def _format_chapters_text(chapters: list[dict]) -> str:
    """将章节列表格式化为纯文本"""
    parts = []
    for chapter in chapters:
        title = chapter.get("title", "")
        content = chapter.get("content", "")
        parts.append(f"### {title}\n\n{content}")
    return "\n\n".join(parts)


def _extract_yaml_from_response(text: str) -> str:
    """
    从 LLM 响应文本中提取 YAML 内容。

    处理以下情况：
    - 纯 YAML 文本
    - ```yaml ... ``` 代码块包裹
    - ``` ... ``` 代码块包裹
    """
    text = text.strip()

    # 尝试提取 ```yaml ... ``` 代码块
    yaml_match = re.search(r"```yaml\s*([\s\S]*?)```", text)
    if yaml_match:
        return yaml_match.group(1).strip()

    # 尝试提取 ``` ... ``` 代码块
    code_match = re.search(r"```\s*([\s\S]*?)```", text)
    if code_match:
        return code_match.group(1).strip()

    # 否则直接返回原文本
    return text


def _clean_yaml(text: str) -> str:
    """清洗 YAML 文本：移除首尾空白行、统一换行"""
    lines = text.splitlines()
    # 移除首尾空行
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def generate_script_yaml(
    chapters: list[dict],
    story_bible: dict,
) -> ScriptYaml:
    """
    根据章节和 Story Bible 生成剧本 YAML。

    Args:
        chapters: 章节列表
        story_bible: Story Bible 数据字典

    Returns:
        解析后的 ScriptYaml 结构化对象
    """
    system_prompt = _load_prompt_template()

    # 格式化 Story Bible 为 JSON
    story_bible_json = json.dumps(story_bible, ensure_ascii=False, indent=2)

    # 格式化章节文本
    chapters_text = _format_chapters_text(chapters)

    # 构造用户提示
    user_prompt = system_prompt.replace(
        "{story_bible_json}", story_bible_json
    ).replace(
        "{chapters_text}", chapters_text
    )

    # 调用 LLM（不使用 JSON 模式，因为需要输出 YAML）
    response_text = chat_completion(
        system_prompt="你是一名专业剧本编剧，请根据输入生成 YAML 格式剧本。只输出 YAML，不要添加任何解释或标记。",
        user_prompt=user_prompt,
        temperature=0.4,
        json_mode=False,
    )

    # 提取 YAML 内容
    yaml_text = _extract_yaml_from_response(response_text)
    yaml_text = _clean_yaml(yaml_text)

    # 解析 YAML
    try:
        raw_data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        # 尝试修复常见 YAML 问题
        yaml_text = _fix_common_yaml_issues(yaml_text)
        try:
            raw_data = yaml.safe_load(yaml_text)
        except yaml.YAMLError:
            raise ValueError(
                f"YAML 解析失败: {e}\n\n原始输出（前 500 字符）:\n{yaml_text[:500]}"
            )

    if raw_data is None:
        raise ValueError(f"YAML 解析结果为空。原始输出（前 500 字符）:\n{yaml_text[:500]}")

    # 校验并转换为结构化对象
    script_yaml = ScriptYaml.model_validate(raw_data)

    return script_yaml


def _fix_common_yaml_issues(yaml_text: str) -> str:
    """修复常见的 YAML 格式问题"""
    # 移除可能的 BOM 标记
    yaml_text = yaml_text.lstrip("﻿")

    # 确保行首没有 tab，替换为空格
    lines = []
    for line in yaml_text.splitlines():
        # 将行首的 tab 替换为 2 个空格
        stripped = line.lstrip("\t")
        indent = len(line) - len(stripped)
        lines.append("  " * indent + stripped)
    yaml_text = "\n".join(lines)

    return yaml_text
