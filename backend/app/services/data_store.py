import json
import os
import uuid
from pathlib import Path

# 数据存储根目录
DATA_DIR = Path(os.getenv("DATA_DIR", "./data/projects"))


def _ensure_data_dir() -> Path:
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def _project_path(project_id: str) -> Path:
    """获取项目 JSON 文件路径"""
    return _ensure_data_dir() / f"{project_id}.json"


def generate_project_id() -> str:
    """生成唯一项目 ID"""
    return f"project_{uuid.uuid4().hex[:8]}"


def save_project(project_data: dict) -> dict:
    """保存项目数据到 JSON 文件，返回保存的数据"""
    project_id = project_data.get("project_id") or generate_project_id()
    project_data["project_id"] = project_id

    path = _project_path(project_id)
    path.write_text(json.dumps(project_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return project_data


def load_project(project_id: str) -> dict | None:
    """加载项目数据，不存在则返回 None"""
    path = _project_path(project_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def update_project(project_id: str, updates: dict) -> dict | None:
    """更新项目数据，返回更新后的完整数据"""
    project = load_project(project_id)
    if project is None:
        return None
    project.update(updates)
    save_project(project)
    return project
