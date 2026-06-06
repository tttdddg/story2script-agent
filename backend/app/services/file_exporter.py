"""
文件导出服务

将生成的 YAML 剧本导出为 .yaml 文件，支持编码处理与文件名生成。
"""

import re
from datetime import datetime


def sanitize_filename(name: str) -> str:
    """
    清理文件名，移除不安全的字符。

    Args:
        name: 原始名称

    Returns:
        安全的文件名（不含路径分隔符和特殊字符）
    """
    # 移除或替换不安全的字符
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # 压缩多余的空格和下划线
    name = re.sub(r'[\s_]+', '_', name).strip('_')
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name or "script"


def export_yaml(
    yaml_content: str,
    title: str = "script",
    include_timestamp: bool = True,
) -> tuple[bytes, str]:
    """
    导出 YAML 文件。

    Args:
        yaml_content: YAML 文本内容
        title: 项目标题，用于生成文件名
        include_timestamp: 是否在文件名中包含时间戳

    Returns:
        (文件字节内容, 文件名)
    """
    # 生成文件名
    safe_title = sanitize_filename(title)

    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.yaml"
    else:
        filename = f"{safe_title}.yaml"

    # 确保 UTF-8 BOM 以便 Windows 记事本正确识别
    content_bytes = yaml_content.encode("utf-8")

    return content_bytes, filename
