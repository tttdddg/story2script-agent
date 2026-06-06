from fastapi import APIRouter, HTTPException

from app.schemas.response_schema import (
    ErrorResponse,
    ValidateResponse,
    RepairResponse,
)
from app.services.data_store import load_project, update_project
from app.services.yaml_validator import validate_yaml_content
from app.services.yaml_repairer import repair_yaml, repair_and_validate

router = APIRouter(prefix="/api")


@router.post(
    "/projects/{project_id}/validate",
    response_model=ValidateResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    },
    summary="校验剧本 YAML",
)
async def validate_project_yaml(project_id: str):
    """
    对项目中的剧本 YAML 进行结构化校验。

    - 从项目存储读取 yaml_content
    - 执行 YAML 语法、字段完整性、人物一致性等校验
    - 返回校验结果（valid / errors / warnings）
    - 不依赖大模型，速度快
    """
    project = load_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"项目 {project_id} 不存在")

    yaml_content = project.get("yaml_content")
    if not yaml_content:
        raise HTTPException(
            status_code=400, detail="项目中没有生成的 YAML，请先执行剧本生成"
        )

    validation = validate_yaml_content(yaml_content)

    # 保存校验结果
    update_project(project_id, {
        "validation": validation.model_dump()
    })

    return ValidateResponse(
        project_id=project_id,
        validation=validation,
    )


@router.post(
    "/projects/{project_id}/repair",
    response_model=RepairResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="自动修复 YAML",
)
async def repair_project_yaml(project_id: str):
    """
    对校验失败的 YAML 进行自动修复。

    - 校验 → 调用 LLM 修复 → 再校验（最多 2 轮）
    - 修复过程中不改变剧情内容
    - 返回修复后的 YAML 和修复记录
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
        result = repair_and_validate(yaml_content)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"大模型修复失败: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 保存修复结果
    update_project(project_id, {
        "yaml_content": result["repaired_yaml"],
        "repair_result": {
            "valid": result["valid"],
            "repair_notes": result["repair_notes"],
        },
    })

    return RepairResponse(
        project_id=project_id,
        repaired_yaml=result["repaired_yaml"],
        valid=result["valid"],
        repair_notes=result["repair_notes"],
        remaining_errors=result.get("remaining_errors", []),
        remaining_warnings=result.get("remaining_warnings", []),
    )
