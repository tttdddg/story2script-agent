from fastapi import APIRouter, HTTPException

from app.schemas.response_schema import (
    ErrorResponse,
    ExtractStoryBibleResponse,
    GenerateScriptResponse,
)
from app.services.data_store import load_project, update_project
from app.services.script_generator import generate_script_yaml
from app.services.story_extractor import extract_story_bible

router = APIRouter(prefix="/api")


@router.post(
    "/projects/{project_id}/extract",
    response_model=ExtractStoryBibleResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="抽取 Story Bible",
)
async def extract_project_story_bible(project_id: str):
    """
    对已解析章节的项目执行 Story Bible 抽取。

    - 从项目存储中读取章节列表
    - 调用大模型抽取人物、地点、关键事件、人物关系
    - 结果保存到项目数据中
    - 返回结构化 Story Bible
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    chapters = project.get("chapters", [])
    if not chapters:
        raise HTTPException(
            status_code=400, detail="项目中没有已解析的章节，请先执行章节解析"
        )

    try:
        story_bible = extract_story_bible(chapters)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"大模型调用失败: {e}")

    # 保存到项目数据
    update_project(project_id, {
        "story_bible": story_bible.model_dump()
    })

    return ExtractStoryBibleResponse(
        project_id=project_id,
        story_bible=story_bible,
    )


@router.post(
    "/projects/{project_id}/generate",
    response_model=GenerateScriptResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="生成剧本 YAML",
)
async def generate_project_script(project_id: str):
    """
    根据已解析的章节和 Story Bible 生成剧本 YAML。

    - 从项目存储中读取章节和 Story Bible
    - 调用大模型生成结构化 YAML 剧本
    - 结果保存到项目数据中
    - 返回 YAML 文本和场景数量
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    chapters = project.get("chapters", [])
    if not chapters:
        raise HTTPException(
            status_code=400, detail="项目中没有已解析的章节，请先执行章节解析"
        )

    story_bible_raw = project.get("story_bible")
    if not story_bible_raw:
        raise HTTPException(
            status_code=400, detail="项目中没有 Story Bible 数据，请先执行抽取"
        )

    try:
        import yaml
        script_yaml = generate_script_yaml(chapters, story_bible_raw)
        # 将结构化对象序列化为 YAML 字符串
        yaml_content = yaml.dump(
            script_yaml.model_dump(),
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
        scene_count = len(script_yaml.scenes)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"大模型调用失败: {e}")

    # 保存到项目数据
    update_project(project_id, {
        "yaml_content": yaml_content,
        "scene_count": scene_count,
    })

    return GenerateScriptResponse(
        project_id=project_id,
        yaml_content=yaml_content,
        scene_count=scene_count,
    )
