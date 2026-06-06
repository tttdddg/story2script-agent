from fastapi import APIRouter, HTTPException

from app.schemas.request_schema import CreateProjectRequest
from app.schemas.response_schema import (
    ChapterInfo,
    CreateProjectResponse,
    ErrorResponse,
    ParseChaptersResponse,
)
from app.services.chapter_parser import parse_chapters, validate_chapter_count
from app.services.data_store import generate_project_id, load_project, save_project

router = APIRouter(prefix="/api")


@router.post(
    "/projects",
    response_model=CreateProjectResponse,
    responses={400: {"model": ErrorResponse}},
    summary="创建项目并上传小说",
)
async def create_project(req: CreateProjectRequest):
    """
    创建新项目，上传小说全文文本。

    - 自动识别章节并校验至少 3 个章节
    - 章节数不足 3 时返回 400 错误
    - 成功时返回项目 ID、标题、章节数与总字数
    """
    # 解析章节
    chapters = parse_chapters(req.novel_text)

    # 校验章节数
    error_msg = validate_chapter_count(chapters)
    if error_msg:
        raise HTTPException(status_code=400, detail=error_msg)

    total_words = sum(c.word_count for c in chapters)

    # 保存项目
    project_data = save_project({
        "project_id": generate_project_id(),
        "title": req.title,
        "novel_text": req.novel_text,
        "chapter_count": len(chapters),
        "word_count": total_words,
        "chapters": [c.model_dump() for c in chapters],
    })

    return CreateProjectResponse(
        project_id=project_data["project_id"],
        title=project_data["title"],
        chapter_count=project_data["chapter_count"],
        word_count=project_data["word_count"],
    )


@router.post(
    "/projects/{project_id}/parse",
    response_model=ParseChaptersResponse,
    responses={404: {"model": ErrorResponse}},
    summary="重新解析项目章节",
)
async def parse_project_chapters(project_id: str):
    """
    对已有项目重新执行章节解析。

    - 从项目存储中读取小说原文
    - 重新识别章节标题并拆分
    - 返回最新的章节列表
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    chapters = parse_chapters(project["novel_text"])

    # 更新项目
    total_words = sum(c.word_count for c in chapters)
    project["chapters"] = [c.model_dump() for c in chapters]
    project["chapter_count"] = len(chapters)
    project["word_count"] = total_words

    from app.services.data_store import save_project
    save_project(project)

    return ParseChaptersResponse(
        project_id=project_id,
        chapter_count=len(chapters),
        chapters=chapters,
    )
