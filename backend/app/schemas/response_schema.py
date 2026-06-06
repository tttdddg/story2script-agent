from typing import Optional
from pydantic import BaseModel, Field


class ChapterInfo(BaseModel):
    """章节信息"""
    chapter_id: str = Field(..., description="章节唯一 ID，如 chapter_001")
    title: str = Field(..., description="章节标题，如 第一章 退稿的傍晚")
    word_count: int = Field(..., description="章节字数")
    content: str = Field(..., description="章节正文内容")


class CreateProjectResponse(BaseModel):
    """创建项目响应"""
    project_id: str = Field(..., description="项目唯一 ID")
    title: str = Field(..., description="项目标题")
    chapter_count: int = Field(..., description="识别到的章节数量")
    word_count: int = Field(..., description="小说总字数")


class ParseChaptersResponse(BaseModel):
    """章节解析响应"""
    project_id: str = Field(..., description="项目 ID")
    chapter_count: int = Field(..., description="章节数量")
    chapters: list[ChapterInfo] = Field(default_factory=list, description="章节列表")


class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str = Field(..., description="错误详情")
    error_code: Optional[str] = Field(None, description="错误码")


# ── Story Bible 相关 ──

class CharacterInfo(BaseModel):
    """人物信息"""
    id: str = Field(..., description="人物 ID，如 char_001")
    name: str = Field(..., description="人物名称")
    aliases: list[str] = Field(default_factory=list, description="别名列表")
    role: str = Field(..., description="角色类型：protagonist/antagonist/supporting/minor")
    personality: str = Field("", description="性格描述")
    motivation: str = Field("", description="角色动机")


class RelationshipInfo(BaseModel):
    """人物关系"""
    model_config = {"populate_by_name": True}

    from_char: str = Field(..., alias="from", description="关系源角色")
    to: str = Field(..., description="关系目标角色")
    relation: str = Field(..., description="关系描述")


class KeyEventInfo(BaseModel):
    """关键事件"""
    event_id: str = Field(..., description="事件 ID")
    description: str = Field(..., description="事件描述")
    related_chapters: list[str] = Field(default_factory=list, description="相关章节")
    related_characters: list[str] = Field(default_factory=list, description="相关人物")


class StoryBibleData(BaseModel):
    """Story Bible 完整数据"""
    characters: list[CharacterInfo] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    key_events: list[KeyEventInfo] = Field(default_factory=list)
    relationships: list[RelationshipInfo] = Field(default_factory=list)


class ExtractStoryBibleResponse(BaseModel):
    """Story Bible 抽取响应"""
    project_id: str = Field(..., description="项目 ID")
    story_bible: StoryBibleData = Field(..., description="Story Bible 数据")
