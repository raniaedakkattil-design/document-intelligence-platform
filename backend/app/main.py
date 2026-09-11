from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.documents import router as documents_router
from app.core.database import Base, engine
from app.models.document import Document

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Document Intelligence Platform",
    description="AI-powered financial document extraction and validation API",
    version="1.0.0",
)


app.include_router(documents_router)

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend",
)


@app.get("/", response_class=HTMLResponse)
def root():

    frontend_path = FRONTEND_DIR / "index.html"

    with open(frontend_path, "r", encoding="utf-8") as file:
        return file.read()


@app.get("/api/v1/health")
def health_check():

    return {
        "status": "ok",
        "service": "Document Intelligence Platform",
    }