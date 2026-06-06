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
