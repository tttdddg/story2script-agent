import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DATA_DIR = os.getenv("DATA_DIR", "./data/projects")
