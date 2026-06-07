"""
DeepSeek API 客户端

封装 DeepSeek Chat API 调用，支持 JSON 模式输出和错误处理。
DeepSeek API 兼容 OpenAI SDK 格式。

当未配置 DEEPSEEK_API_KEY 时抛出 NoApiKeyError，
调用方应捕获此异常并回退到 Demo 模式。
"""

import json
import re
import time
from typing import Optional

from openai import OpenAI

from app.config import DEEPSEEK_API_KEY, DEMO_MODE


class NoApiKeyError(Exception):
    """API Key 未配置异常 — 调用方应回退到 Demo 模式"""

    def __init__(self):
        super().__init__(
            "DEEPSEEK_API_KEY 未配置。"
            "请在 backend/.env 中设置 DEEPSEEK_API_KEY=your_key，"
            "或使用 Demo 模式（当前已自动启用 Demo 模式）。"
        )

# DeepSeek API 配置
DEEPSEEK_BASE_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
MAX_RETRIES = 2
RETRY_DELAY = 1.0  # 秒
REQUEST_TIMEOUT = 90.0  # 秒


def _api_key() -> str:
    """获取 API Key，未配置时抛出 NoApiKeyError"""
    if not DEEPSEEK_API_KEY:
        raise NoApiKeyError()
    return DEEPSEEK_API_KEY


def is_demo_mode() -> bool:
    """判断当前是否为 Demo 模式（无 API Key）"""
    return DEMO_MODE


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.3,
    json_mode: bool = True,
    max_tokens: int = 4096,
) -> str:
    """
    调用 DeepSeek Chat API 并返回响应内容。

    Args:
        system_prompt: 系统提示词
        user_prompt: 用户提示词
        temperature: 生成温度 (0-2)
        json_mode: 是否启用 JSON 模式
        max_tokens: 最大输出 token 数

    Returns:
        模型响应的文本内容
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Use OpenAI-compatible SDK for reliability
    client = OpenAI(api_key=_api_key(), base_url="https://api.deepseek.com")

    last_error: Optional[Exception] = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"} if json_mode else None,
                timeout=REQUEST_TIMEOUT,
            )
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("模型返回空内容")
            return content

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (attempt + 1))

    raise RuntimeError(
        f"DeepSeek API 调用失败（已重试 {MAX_RETRIES} 次）: {last_error}"
    )


def extract_json_from_response(text: str) -> dict:
    """
    从模型响应中提取 JSON 对象。

    - 如果整个文本是 JSON，直接解析
    - 否则尝试提取 ```json ... ``` 代码块
    - 否则尝试提取 { ... } 包裹的部分
    """
    text = text.strip()

    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试提取 markdown 代码块
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 尝试提取最外层 { ... }
    brace_match = re.search(r"\{[\s\S]*\}", text)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"无法从响应中解析 JSON: {text[:200]}...")
