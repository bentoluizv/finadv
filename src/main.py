"""
FinAdv FastAPI app: routers, static files, and template config.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fasthx.jinja import Jinja

TEMPLATES_DIR = Path(__file__).resolve().parent / 'resources' / '_base' / 'templates'
STATIC_DIR = Path(__file__).resolve().parent / 'static'


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title='FinAdv', description='Income & Debt tracking', lifespan=lifespan)

app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

jinja = Jinja(Jinja2Templates(directory=str(TEMPLATES_DIR)))


@app.get('/')
@jinja.page('index.html')
async def home() -> None: ...


@app.post('/theme/toggle')
async def toggle_theme(request: Request) -> Response:
    current = request.cookies.get('theme', 'light')
    next_theme = 'dark' if current == 'light' else 'light'
    response = Response(status_code=204)
    response.set_cookie('theme', next_theme, max_age=60 * 60 * 24 * 365, samesite='lax')
    response.headers['HX-Refresh'] = 'true'
    return response
