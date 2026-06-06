"""
Story Bible 抽取服务

将小说章节文本提交给大模型，抽取人物、地点、关键事件和人物关系。
"""

from pathlib import Path

from app.schemas.response_schema import (
    CharacterInfo,
    KeyEventInfo,
    RelationshipInfo,
    StoryBibleData,
)
from app.services.llm_client import chat_completion, extract_json_from_response

# Prompt 模板路径
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "extract_story_bible.txt"


def _load_prompt_template() -> str:
    """加载 Prompt 模板"""
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt 模板文件不存在: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def _format_chapters(chapters: list[dict]) -> str:
    """
    将章节列表格式化为 Prompt 中的文本。

    每个章节格式：
    ### {title}
    {content}
    """
    parts = []
    for chapter in chapters:
        title = chapter.get("title", "")
        content = chapter.get("content", "")
        parts.append(f"### {title}\n\n{content}")
    return "\n\n".join(parts)


def _validate_and_clean_story_bible(raw: dict) -> StoryBibleData:
    """
    校验并清洗 LLM 返回的原始 JSON 数据。

    - 确保必要字段存在
    - 补全缺失的字段
    - 统一 ID 格式
    """
    # 人物
    characters = []
    for i, char in enumerate(raw.get("characters", []) or []):
        characters.append(CharacterInfo(
            id=char.get("id", f"char_{i + 1:03d}"),
            name=char.get("name", f"未知角色_{i + 1}"),
            aliases=char.get("aliases", []) or [],
            role=char.get("role", "supporting"),
            personality=char.get("personality", ""),
            motivation=char.get("motivation", ""),
        ))

    # 地点（可能是字符串列表或对象列表）
    locations = []
    for loc in raw.get("locations", []) or []:
        if isinstance(loc, str):
            locations.append(loc)
        elif isinstance(loc, dict):
            locations.append(loc.get("name", str(loc)))

    # 关键事件
    key_events = []
    for i, evt in enumerate(raw.get("key_events", []) or []):
        key_events.append(KeyEventInfo(
            event_id=evt.get("event_id", f"event_{i + 1:03d}"),
            description=evt.get("description", ""),
            related_chapters=evt.get("related_chapters", []) or [],
            related_characters=evt.get("related_characters", []) or [],
        ))

    # 人物关系
    relationships = []
    for rel in raw.get("relationships", []) or []:
        relationships.append(RelationshipInfo(
            from_char=rel.get("from", rel.get("from_char", "")),
            to=rel.get("to", ""),
            relation=rel.get("relation", ""),
        ))

    return StoryBibleData(
        characters=characters,
        locations=locations,
        key_events=key_events,
        relationships=relationships,
    )


def extract_story_bible(chapters: list[dict]) -> StoryBibleData:
    """
    从章节列表中抽取 Story Bible。

    Args:
        chapters: 章节列表，每项包含 title, content 等字段

    Returns:
        StoryBibleData 结构化数据
    """
    # 加载 Prompt 模板
    system_prompt = _load_prompt_template()

    # 格式化章节文本
    chapters_text = _format_chapters(chapters)

    # 调用 LLM
    response_text = chat_completion(
        system_prompt=system_prompt,
        user_prompt=chapters_text,
        temperature=0.3,
        json_mode=True,
    )

    # 解析 JSON
    raw_data = extract_json_from_response(response_text)

    # 校验并清洗
    story_bible = _validate_and_clean_story_bible(raw_data)

    return story_bible
