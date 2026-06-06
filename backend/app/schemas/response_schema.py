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


class GenerateScriptResponse(BaseModel):
    """剧本生成响应"""
    project_id: str = Field(..., description="项目 ID")
    yaml_content: str = Field(..., description="生成的 YAML 剧本文本")
    scene_count: int = Field(..., description="场景数量")


# ── YAML 校验相关 ──

class ValidationError(BaseModel):
    """单个校验错误/警告"""
    path: str = Field(..., description="出错字段路径，如 scenes[3].conflict")
    message: str = Field(..., description="错误描述")


class ValidationResult(BaseModel):
    """校验结果"""
    valid: bool = Field(..., description="是否通过校验")
    errors: list[ValidationError] = Field(default_factory=list, description="错误列表")
    warnings: list[ValidationError] = Field(default_factory=list, description="警告列表")


class ValidateResponse(BaseModel):
    """校验 API 响应"""
    project_id: str = Field(..., description="项目 ID")
    validation: ValidationResult = Field(..., description="校验结果")


class RepairResponse(BaseModel):
    """修复 API 响应"""
    project_id: str = Field(..., description="项目 ID")
    repaired_yaml: str = Field("", description="修复后的 YAML")
    valid: bool = Field(False, description="修复后是否通过校验")
    repair_notes: list[str] = Field(default_factory=list, description="修复记录")
    remaining_errors: list[ValidationError] = Field(default_factory=list, description="剩余错误")
    remaining_warnings: list[ValidationError] = Field(default_factory=list, description="剩余警告")


# ── 质量报告相关 ──

class CharacterAppearance(BaseModel):
    """人物出场统计"""
    name: str = Field(..., description="人物名称")
    count: int = Field(..., description="出场次数")


class SceneDialogueStat(BaseModel):
    """场景对白统计"""
    scene_id: str = Field(..., description="场景 ID")
    dialogue_count: int = Field(..., description="对白数量")


class QualityReport(BaseModel):
    """剧本质量报告"""
    chapter_count: int = Field(0, description="原文章节数")
    scene_count: int = Field(0, description="场景总数")
    character_count: int = Field(0, description="人物总数")
    dialogue_count: int = Field(0, description="对白总数")
    action_count: int = Field(0, description="动作描写总数")
    conflict_scene_count: int = Field(0, description="包含冲突的场景数")
    character_appearances: list[CharacterAppearance] = Field(default_factory=list, description="人物出场次数")
    scene_dialogue_stats: list[SceneDialogueStat] = Field(default_factory=list, description="每场景对白数")
    suggestions: list[str] = Field(default_factory=list, description="优化建议")


class ReportResponse(BaseModel):
    """质量报告 API 响应"""
    project_id: str = Field(..., description="项目 ID")
    report: QualityReport = Field(..., description="质量报告")
