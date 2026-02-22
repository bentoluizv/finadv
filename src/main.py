"""
FinAdv FastAPI app: routers, static files, and template config.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import http
from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

TEMPLATES_DIR = Path(__file__).resolve().parent / 'resources' / '_base' / 'templates'
STATIC_DIR = Path(__file__).resolve().parent / 'static'

_4XX_5XX_MESSAGES: dict[int, tuple[str, str]] = {
    400: ('Bad request', "The request could not be understood."),
    403: ('Forbidden', "You don't have permission to access this resource."),
    404: ('Page not found', "The page you're looking for doesn't exist."),
    422: ('Validation error', 'The request contained invalid data.'),
    500: ('Internal server error', 'Something went wrong. Please try again later.'),
}


def _error_context(status_code: int, detail: object) -> dict[str, str | int]:
    if status_code in _4XX_5XX_MESSAGES:
        title, message = _4XX_5XX_MESSAGES[status_code]
    else:
        try:
            title = http.HTTPStatus(status_code).phrase
        except ValueError:
            title = 'Error'
        message = str(detail) if isinstance(detail, str) else 'An error occurred.'
    return {'status_code': status_code, 'title': title, 'message': message}


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title='FinAdv', description='Income & Debt tracking', lifespan=lifespan)

app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler_custom(
    request: Request, exc: StarletteHTTPException
) -> HTMLResponse | Response:
    if 400 <= exc.status_code < 500:
        context = _error_context(exc.status_code, exc.detail)
        return templates.TemplateResponse(
            request=request,
            name='error.html',
            context=context,
            status_code=exc.status_code,
        )
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    logging.exception('Unhandled exception: %s', exc)
    context = _error_context(500, _4XX_5XX_MESSAGES[500][1])
    return templates.TemplateResponse(
        request=request,
        name='error.html',
        context=context,
        status_code=500,
    )


@app.get('/', response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name='index.html', context={'active_page': 'overview'}
    )


@app.post('/theme/toggle')
async def toggle_theme(request: Request) -> Response:
    current = request.cookies.get('theme', 'light')
    next_theme = 'dark' if current == 'light' else 'light'
    response = Response(status_code=204)
    response.set_cookie('theme', next_theme, max_age=60 * 60 * 24 * 365, samesite='lax')
    response.headers['HX-Refresh'] = 'true'
    return response
