"""
FinAdv FastAPI app: routers, static files, and template config.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent / "resources" / "_base" / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="FinAdv", description="Income & Debt tracking")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Serve the overview page with base layout."""
    return templates.TemplateResponse(request=request, name="index.html", context={})
