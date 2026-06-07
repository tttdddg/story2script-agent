import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DATA_DIR = os.getenv("DATA_DIR", "./data/projects")

# Demo 模式：未配置 API Key 时自动启用，使用预计算示例数据
DEMO_MODE = not bool(DEEPSEEK_API_KEY)
