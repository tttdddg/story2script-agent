from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    """创建项目 / 上传小说请求"""
    title: str = Field(..., min_length=1, max_length=200, description="项目/小说标题")
    novel_text: str = Field(..., min_length=1, description="小说全文文本")
