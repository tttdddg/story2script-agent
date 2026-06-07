from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.schemas.response_schema import ErrorResponse, ReportResponse
from app.services.data_store import load_project
from app.services.file_exporter import export_yaml
from app.services.report_generator import generate_report

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

    # URL-encode the filename for Content-Disposition to handle Chinese characters
    from urllib.parse import quote
    encoded_filename = quote(filename)

    return Response(
        content=content_bytes,
        media_type="application/x-yaml; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
        },
    )


@router.get(
    "/projects/{project_id}/report",
    response_model=ReportResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="生成剧本质量报告",
)
async def get_project_report(project_id: str):
    """
    生成剧本质量报告。

    - 从项目存储读取 yaml_content
    - 统计章节/场景/人物/对白/动作等指标
    - 生成优化建议
    - 不依赖大模型，纯规则驱动
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    yaml_content = project.get("yaml_content")
    if not yaml_content:
        raise HTTPException(
            status_code=400, detail="项目中没有生成的 YAML，请先执行剧本生成"
        )

    try:
        report = generate_report(yaml_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告生成失败: {e}")

    return ReportResponse(
        project_id=project_id,
        report=report,
    )
