from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse
import io

from app.schemas.response_schema import ErrorResponse
from app.services.data_store import load_project
from app.services.file_exporter import export_yaml

router = APIRouter(prefix="/api")


@router.get(
    "/projects/{project_id}/export",
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    },
    summary="导出剧本 YAML 文件",
)
async def export_project_yaml(project_id: str):
    """
    导出项目的剧本 YAML 文件。

    - 从项目存储读取 yaml_content
    - 生成带时间戳的 .yaml 文件名
    - 返回文件下载响应
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    yaml_content = project.get("yaml_content")
    if not yaml_content:
        raise HTTPException(
            status_code=400, detail="项目中没有生成的 YAML，请先执行剧本生成"
        )

    title = project.get("title", "script")

    content_bytes, filename = export_yaml(yaml_content, title=title)

    return StreamingResponse(
        io.BytesIO(content_bytes),
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "application/x-yaml; charset=utf-8",
        },
    )
