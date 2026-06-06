import re
from typing import Optional

from app.schemas.response_schema import ChapterInfo


# 章节标题正则模式
CHAPTER_PATTERNS = [
    # 第X章（中文数字或阿拉伯数字），如：第一章 / 第1章 / 第一百二十三章
    re.compile(r"^第[一二三四五六七八九十百千万零\d]+章\b", re.MULTILINE),
    # Chapter N（英文），如：Chapter 1 / CHAPTER 2
    re.compile(r"^Chapter\s+\d+\b", re.MULTILINE | re.IGNORECASE),
]

# 简单编号模式：一、二、三、… — 仅在其他模式都未匹配时作为回退
SIMPLE_NUMBERING = re.compile(r"^[一二三四五六七八九十]+、", re.MULTILINE)

# 最少章节数要求
MIN_CHAPTER_COUNT = 3


def _clean_text(text: str) -> str:
    """清洗文本：去除首尾空白，将连续空行压缩为单个换行"""
    text = text.strip()
    # 将 3 个以上连续换行压缩为 2 个
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _count_words(text: str) -> int:
    """统计中文字数（含标点），排除纯空白"""
    return len(text.replace("\n", "").replace("\r", "").replace(" ", "").replace("\t", ""))


def _match_chapter_headings(text: str) -> list[tuple[int, str]]:
    """
    在文本中查找所有章节标题，返回 (起始位置, 标题行) 列表。
    优先使用标准章节模式，若无匹配则尝试简单编号模式。
    """
    matches: list[tuple[int, str]] = []

    # 先尝试标准模式
    for pattern in CHAPTER_PATTERNS:
        for m in pattern.finditer(text):
            line_start = m.start()
            # 取完整标题行（到行尾）
            line_end = text.find("\n", m.start())
            if line_end == -1:
                line_end = len(text)
            heading = text[line_start:line_end].strip()
            matches.append((line_start, heading))

    # 去重并排序（可能出现不同模式匹配到同一位置的情况）
    matches = sorted(set(matches), key=lambda x: x[0])

    # 如果标准模式没匹配到，尝试简单编号
    if not matches:
        for m in SIMPLE_NUMBERING.finditer(text):
            line_start = m.start()
            line_end = text.find("\n", m.start())
            if line_end == -1:
                line_end = len(text)
            heading = text[line_start:line_end].strip()
            matches.append((line_start, heading))
        matches = sorted(set(matches), key=lambda x: x[0])

    return matches


def parse_chapters(novel_text: str) -> list[ChapterInfo]:
    """
    解析小说文本，按章节标题拆分为章节列表。

    支持的章节格式：
    - 第一章 / 第1章 / 第一百二十三章
    - Chapter 1 / CHAPTER 2
    - 一、二、三、（回退模式）

    返回章节信息列表，每个包含 chapter_id / title / word_count / content。
    """
    text = _clean_text(novel_text)
    headings = _match_chapter_headings(text)

    if not headings:
        return []

    chapters: list[ChapterInfo] = []

    for i, (pos, heading) in enumerate(headings):
        # 确定内容结束位置（下一个章节的起始位置，或文本末尾）
        if i + 1 < len(headings):
            content_end = headings[i + 1][0]
        else:
            content_end = len(text)

        # 提取内容：跳过标题行
        heading_line_end = text.find("\n", pos)
        if heading_line_end == -1:
            content_start = len(text)
        else:
            content_start = heading_line_end + 1

        chapter_content = text[content_start:content_end].strip()
        word_count = _count_words(heading) + _count_words(chapter_content)

        chapter_id = f"chapter_{i + 1:03d}"

        chapters.append(ChapterInfo(
            chapter_id=chapter_id,
            title=heading,
            word_count=word_count,
            content=chapter_content,
        ))

    return chapters


def validate_chapter_count(chapters: list[ChapterInfo]) -> Optional[str]:
    """
    校验章节数量是否满足最低要求。
    不足 3 章时返回错误消息，否则返回 None。
    """
    if len(chapters) < MIN_CHAPTER_COUNT:
        return (
            f"检测到 {len(chapters)} 个章节，"
            f"至少需要 {MIN_CHAPTER_COUNT} 个章节才能继续。"
            f"请检查文本格式，确保使用「第X章」或「Chapter N」等标准章节标题。"
        )
    return None
