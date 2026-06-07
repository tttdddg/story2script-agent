import sys
from pathlib import Path

_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_project import router as project_router
from app.api.routes_generate import router as generate_router
from app.api.routes_validate import router as validate_router
from app.api.routes_export import router as export_router

app = FastAPI(
    title="Story2Script Agent",
    description="AI 小说剧本结构化改编平台",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(generate_router)
app.include_router(validate_router)
app.include_router(export_router)


@app.get("/api/health")
async def health_check():
    from app.config import DEMO_MODE

    return {
        "status": "ok",
        "message": "Story2Script Agent backend is running",
        "demo_mode": DEMO_MODE,
        "api_key_configured": not DEMO_MODE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
