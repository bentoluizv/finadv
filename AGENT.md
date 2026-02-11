# Agent Instructions: Financial Advisor

Coding standards and structure: see **`.cursorrules`**.

## Current Project State
Building the MVP for tracking Incomes and Debts (Sporadic/Recurrent).

## Product & UX: How the app works

**Purpose:** FinAdv helps a single user act as their own financial adviser by tracking **incomes** and **debts** in one place, with clear categories and payment methods, so they can see where money comes from and where it goes (including recurrent obligations).

**User:** One person managing their personal finances. No multi-user or roles in the MVP.

**How the user interacts:** Web app in the browser. Server-rendered pages with HTMX for partial updates (no SPA). Actions are: navigate (links), submit forms (add/edit income or debt), filter or list, delete. Prefer small, focused screens and inline feedback (e.g. swap a row or a list fragment after create/delete) instead of full-page reloads where it makes sense.

**What the app does (MVP):**
- **Incomes:** Register incoming money (fixed or variable); list and manage entries.
- **Debts:** Register expenses/obligations with category (Food, Rent, etc.) and payment method (Pix, Credit, Debit, Cash); mark as one-off or recurrent; list and manage entries.
- **Overview:** At least a clear list (or simple dashboard) of recent or all incomes and debts so the user can review the situation.

**Functional requirements (MVP):**
- CRUD for **incomes**: create, list, view, edit, delete.
- CRUD for **debts**: create, list, view, edit, delete.
- **Debt** has: category (e.g. Food, Rent), payment method (Pix, Credit, Debit, Cash), amount, optional description, and **is_recurrent** (boolean).
- **Income** has: amount, optional description, and fixed vs variable (or equivalent).
- Navigation between main areas (e.g. home, incomes, debts) from the layout.
- Validation and clear error messages on forms (e.g. required fields, invalid amounts).

**Non-functional requirements:**
- **Simplicity:** Few screens and concepts; no unnecessary features.
- **Clarity:** Labels and copy should be understandable at a glance (e.g. “Recurrent” vs “One-off”).
- **Responsive:** Usable on small screens (mobile-friendly layout).
- **Accessibility:** Semantic HTML, labels, and keyboard navigation; avoid interaction that relies only on hover or tiny targets.
- **Performance:** Fast response for list and form actions; HTMX used to update only the changed parts where appropriate.

**User stories (MVP):**
- As a user, I want to **add an income** (amount, optional note) so that I can track what I earn.
- As a user, I want to **add a debt** (amount, category, payment method, optional note, and whether it’s recurrent) so that I can track what I owe or spend.
- As a user, I want to **see a list of my incomes and debts** so that I can review my financial situation.
- As a user, I want to **edit or delete** an income or a debt so that I can correct or remove entries.
- As a user, I want to **navigate** between “Incomes”, “Debts”, and home/overview so that I can focus on one area at a time.

When implementing a feature, align with these stories and requirements; do not add flows or screens that are out of scope for the MVP (see Out of Scope).

## Project Layout
- **Entry point:** `src/main.py` (mounts routers, creates app).
- **Base resource:** `src/resources/_base/` — reusable building blocks for all resources. Not a domain resource (no routes mounted). Contains shared models, repository helpers, and a single layout template (see below). Add partials or shared templates only when a real use case appears.
- **Resources:** `src/resources/<name>/` — each has `models.py`, `logic.py`, `repository.py`, `routes.py`, `templates/`, and `tests/` (tests for that resource only). Domain resources inherit or use the base where appropriate.
- **Infrastructure:** `src/ext/` — e.g. `db.py` (async engine, `get_session` yielding `AsyncSession`), future async API clients. All models used by Alembic must be imported there (or in a central metadata). Shared test fixtures (e.g. test client, async session) live in `src/ext/` or project-root `conftest.py`.

## Tools & Dependencies (pyproject.toml)
- **Runtime:** Python ≥3.14; **uv** (package manager and runner).
- **Web:** **FastAPI** (API + server; `[all]` includes Jinja2, static files, etc.); **fasthx** (HTMX integration for FastAPI); **htmy** (HTML templating).
- **Data:** **SQLModel** (ORM + Pydantic models); **Alembic** (DB migrations); **pydantic** (validation/settings); **orjson** (fast JSON); **python-ulid** (ULID identifiers).
- **Dev / quality:** **ruff** (lint + format); **ty** (static type checker); **pytest** (tests); **taskipy** (task runner from pyproject); **pytailwindcss** (Tailwind CSS build); **ignr** (CLI to fetch .gitignore templates from gitignore.io).

## Async-first rule

All request-handling and I/O must be **async**: use `async def` for routes, repository functions, and logic that performs DB or external API calls. Use **AsyncSession** (SQLModel) and async HTTP clients; do not use sync `Session` or blocking I/O in the request path. This keeps the event loop non-blocking and matches FastAPI/htmy async usage.

## Dependency usage examples

Use these patterns in code; adapt to your resource and base layer. All examples are async.

### FastAPI — router, Depends, async response
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/debts", tags=["Debts"])

@router.get("/{id}", response_model=DebtRead)
async def get_debt(id: str, session: AsyncSession = Depends(get_session)) -> Debt:
    debt = await repository.get_by_id(session, id)
    if debt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return debt

@router.post("", response_model=DebtRead, status_code=status.HTTP_201_CREATED)
async def create_debt(body: DebtCreate, session: AsyncSession = Depends(get_session)) -> Debt:
    entity = factory.build_debt(**body.model_dump())
    return await repository.add(session, entity)
```
Define `get_session` in `src/ext/db.py` as an **async** dependency that yields an `AsyncSession` (e.g. `async with AsyncSession(engine) as session: yield session`).

### SQLModel — AsyncSession, select, add, commit
```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_by_id(session: AsyncSession, model: type[Debt], id: str) -> Debt | None:
    return await session.get(model, id)

async def list_all(session: AsyncSession, model: type[Debt]) -> list[Debt]:
    statement = select(model)
    result = await session.exec(statement)
    return list(result.all())

async def add(session: AsyncSession, entity: Debt) -> Debt:
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity
```
Use `await session.exec(select(Model).where(...))` for filtered queries; keep all such code inside `repository.py`. Engine must be created with `create_async_engine` for async.

### fasthx — HTMX vs full page (async routes)
```python
from fasthx.htmy import HTMY
from sqlmodel.ext.asyncio.session import AsyncSession

htmy = HTMY()  # or pass template dir / renderer config

@router.get("/debts")
@htmy.hx(DebtListComponent)   # HTMX request → render fragment
async def list_debts(session: AsyncSession = Depends(get_session)) -> list[Debt]:
    return await repository.list_all(session, Debt)

@router.get("/")
@htmy.page(IndexPageComponent)  # full page (e.g. layout + content)
async def index() -> None: ...
```
The decorator uses the route’s return value and request context; the component (htmy or Jinja) receives that data. Same route can serve both HTMX and non-HTMX by returning data and letting the decorator choose the view. Prefer **small HTMX fragments** (for `hx-swap`) for list rows, tables, and form regions, and use full pages only for top-level shells (layout + initial content).

### htmy — components and rendering
```python
from htmy import Renderer, component, html, Context, Component

@component
def debt_row(debt: Debt, context: Context) -> Component:
    return html.tr(
        html.td(debt.id),
        html.td(debt.category),
        html.td(str(debt.amount)),
    )

@component
def debt_table(debts: list[Debt], context: Context) -> Component:
    return html.table([debt_row(d) for d in debts])

# In a route (e.g. with fasthx): return data; fasthx passes it to the component.
# Standalone render: result = await Renderer().render(debt_table(debts))
```
Use `html.<tag>(*children, attr=value)` for elements; `@component` (or `@component.context_only`) for **function components**; and optional class-based components with an `htmy(self, context)` method when you want to attach behavior to domain objects. Attributes use snake_case and are converted to kebab-case (e.g. `data_theme` → `data-theme`).

- **Component factories vs components:** When you only need to build markup without context, use simple factories that return components (e.g. `def debt_row_factory(...) -> Component`). When you need access to request/route context or want reusable behavior, prefer **htmy components** (`@component` or classes with `htmy()`), as described in the htmy components and function components guides.
- **Streaming (optional):** For very long lists or slow-per-item rendering, you may use `StreamingRenderer` from htmy together with FastHX (see the HTMY Streaming example). Only introduce streaming when you have a real performance need; otherwise keep rendering simple for the MVP.

### python-ulid — IDs for new entities
```python
from ulid import ULID

def build_debt(..., id: str | None = None) -> Debt:
    return Debt(id=str(ULID()) if id is None else id, ...)
```
Use `str(ULID())` when creating new records so every entity has a unique, sortable id.

### Pytest — client and async session fixtures
```python
# conftest.py (e.g. in src/ext/ or resource tests/)
import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main import app

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
async def session():
    async with AsyncSession(engine) as s:
        yield s
        await s.rollback()
```
In resource tests: use `client.get("/debts")`, `client.post("/debts", json={...})` for route tests. For repository or logic tests that need a DB, use the async `session` fixture and `await` repository calls. Use `pytest-asyncio` and mark async tests with `@pytest.mark.asyncio` (or configure asyncio mode in `pytest.ini`/`pyproject.toml`).

### orjson — optional fast JSON
FastAPI can use orjson for response serialization (faster for large payloads). To enable: set a custom `JSONResponse` that uses `orjson.dumps`, or use FastAPI’s built-in orjson support if available for your version. Request bodies are still parsed by FastAPI; use orjson mainly for responses when needed.

## Terminal & Tooling Protocol
- **Installation:** `uv add <package>`
- **Execution:** `uv run fastapi dev src/main.py`
- **Quality Control:** `uv run task check` (runs ruff then ty). See **Ruff (lint and format)** for rule explanations and recommendations.
- **Database Migrations:**
  1. Update `src/resources/<resource>/models.py` and import the new model in `alembic/env.py`.
  2. `uv run alembic revision --autogenerate -m "description"`
  3. `uv run alembic upgrade head`
- **Testing Alembic:** Use the `migrated_db_path` fixture (in `tests/conftest.py`): it runs `alembic upgrade head` against a temporary DB and yields the path. Tests in `tests/test_alembic.py` are atomic (no user action): they use this fixture or a fresh `tmp_path` and run upgrade/downgrade in-process. Run: `uv run pytest tests/test_alembic.py -v`.

## Environment & Config
- Prefer env vars and **pydantic-settings** (or a single settings module in `src/ext/`). Do not hardcode secrets or DB URLs.
- Use a conventional name for the DB: e.g. `DATABASE_URL` or `SQLITE_PATH`. For async SQLModel use `create_async_engine` (e.g. `sqlite+aiosqlite:///...` for SQLite). Document in README or here if you introduce one.

## Testing
- **Run:** `uv run pytest`
- **Location:** Inside each resource: `src/resources/<name>/tests/` (e.g. `test_logic.py`, `test_repository.py`, `test_routes.py`). Tests live next to the code they cover, same as models, routes, and logic.
- **Fixtures:** Resource-specific fixtures in that resource’s `tests/conftest.py`; shared fixtures (DB session, test client) in `src/ext/conftest.py` or project-root `conftest.py`.

## Static Assets
- **CSS:** Tailwind via **pytailwindcss** — run its watch/build as needed; keep built assets in a single known directory (e.g. `static/` under `src` or project root) and serve via FastAPI static mount. Use utility classes in templates/htmy components instead of custom CSS files where possible.
- **JS:** Rely on **HTMX** attributes and FastHX/htmy components for interactivity. Do not introduce a SPA framework or custom front-end build unless explicitly requested.

## Ruff (lint and format)

Configuration is in `pyproject.toml` under `[tool.ruff]`, `[tool.ruff.lint]`, and `[tool.ruff.format]`. Run lint + format and type-check together with **`uv run task check`** (or `uv run task ruff` and `uv run task ty` separately).

### Format rules
- **Single quotes** for strings (`quote-style = "single"`). Use double quotes only when the string contains a single quote or for docstrings if you prefer.
- **Indent width 2** spaces (`indent-width = 2`, `indent-style = "space"`). Keep blocks aligned with 2 spaces; do not use tabs.
- **Line length 88** (Black-compatible). Break long lines; prefer one logical statement per line.
- **Target Python 3.14** (`target-version = "py314"`). Use modern syntax and stdlib; no legacy compatibility hacks for older Python.

### Lint rule sets (modern pythonic)
- **E (pycodestyle):** Style and formatting (indentation, whitespace, line length). Keeps code consistent and readable.
- **F (Pyflakes):** Unused imports, undefined names, dead code. Catches real bugs and clutter.
- **I (isort):** Import order and grouping. Standard library first, then third-party, then local; alphabetical within groups. Run with `--fix` to auto-sort.
- **UP (pyupgrade):** Modern Python syntax and stdlib (e.g. `list[...]` instead of `List` from typing, f-strings, `pathlib`). Aligns code with the target version.
- **B (flake8-bugbear):** Common bugs and anti-patterns (e.g. mutable defaults, bare `except`, assert in production). Prefer fixing the cause over disabling.
- **C4 (flake8-comprehensions):** Clearer list/dict/set comprehensions and avoid unnecessary `list()` around generators where a list comp is clearer.
- **SIM (flake8-simplify):** Simpler equivalents (e.g. single `if` instead of redundant `if/else`, mergeable `with`). Reduces noise without changing behavior.

### Recommendations
- **Run `uv run task check`** after editing Python under `src`; fix any reported issues before considering the task done.
- **Prefer fixing violations** (refactor or correct the code) over adding `# noqa` or ignoring rules. Use `# noqa` only when the rule is a false positive and a one-line comment explains why.
- **Keep the rule set as-is** when adding features. If a rule conflicts with a deliberate pattern, document the exception in code and prefer a narrow per-file or per-line ignore over disabling the rule globally.
- **Format before committing:** `uv run ruff format src` (or run the full check task) so diffs stay clean and consistent.

## Standard Patterns

### Repository
- **Purpose:** Abstract all database access for a resource in one place so logic and routes stay free of session/query details.
- **Location:** `src/resources/<name>/repository.py`.
- **Content:** **Async** functions that take `AsyncSession` and perform CRUD/queries (e.g. `async def get_by_id(session, id)`, `list_all(session)`, `add(session, entity)`, `delete(session, id)`). Use `await session.get`, `await session.exec(select(...))`, `await session.commit`, `await session.refresh`. Return domain models or None; raise or return Result-style for errors if you prefer.
- **Usage:** Routes and logic `await` repository functions; they do not build raw SQL or use the session directly outside the repository.

### Factory (per resource, only when needed)
- **Purpose:** Centralize creation of domain entities when you need overrides (e.g. explicit id/timestamps in tests) or building from a dict. If the model’s `default_factory` is enough (e.g. BaseTable already sets id, created_at, updated_at), instantiate the model directly and skip a factory.
- **Location:** `src/resources/<name>/factory.py` or builder functions in `models.py` (e.g. `build_debt(...)`).
- **When to add:** Add a factory when you have repeated construction logic, test fixtures that need controlled ids/timestamps, or creation from external data. Do not add a factory “for consistency” if `Model(**kwargs)` is enough.

### Base resource (`src/resources/_base/`)
Reusable logic and templates shared by all resources. Do not mount routes for `_base`; it is not a domain.

- **Base models (`_base/models.py`):** Shared fields or a base table class that all domain models can inherit (e.g. `id: str` ULID, `created_at`, `updated_at`). Resource models inherit from this base so schema and migrations stay consistent.
- **Base repository (`_base/repository.py`):** Generic, reusable **async** repository helpers (e.g. `async def get_by_id(session, Model, id)`, `list_all(session, Model)`, `add(session, entity)`, `delete_by_id(session, Model, id)`). Resource repositories `await` these where possible and add only resource-specific queries.
- **Base templates (`_base/templates/`):** One shared layout (e.g. `layout.html`). Add partials (form_errors, csrf, etc.) only when you have a concrete use case and real content; avoid placeholder files.

## Avoiding redundancy and unnecessary code
- **Single source of truth:** Do not duplicate values. E.g. get `database_url` from settings only; do not re-export it as `DATABASE_URL` elsewhere unless a tool (e.g. Alembic) strictly requires it.
- **One entry point per concept:** Prefer one way to obtain something (e.g. `get_settings()` or `settings`, not both unless Depends needs the callable). Document the preferred one.
- **YAGNI (You Aren’t Gonna Need It):** Do not add code “for later.” No placeholder partials, stub files, or “might be useful” helpers. Add form_errors, CSRF, or a base factory when a real feature needs them.
- **Lean tests:** Test behavior, not framework. Prefer one or two focused tests per concern; merge tests that only assert the same thing in different ways. Avoid testing that a library does what it says (e.g. that a model has fields defined in code).
- **Minimal exports:** Only export what other modules use. Drop `__all__` entries and module-level names that nothing imports.

## FastAPI Best Practices
- **Routers:** Use `APIRouter(prefix="/<resource>", tags=["<Resource>"])` per resource; include in `app` in `src/main.py`. Route handlers are `async def`.
- **Dependency injection:** Use `Depends()` for async DB session (e.g. `get_session` yielding `AsyncSession`), config, and reusable logic. Define a single async session dependency in `src/ext/db.py` and inject it into routes that need it.
- **Request/response:** Use Pydantic models (or SQLModel) for request body and `response_model=` on routes. Prefer explicit schemas in `models.py` over returning raw ORM objects when the shape differs from the DB.
- **Status codes:** Set explicit `status_code` where it matters (e.g. `201` on create, `404` when not found, `204` on delete).
- **Thin routes:** Route handlers should: validate input (via Pydantic), `await` logic/repository, return response. No business or DB logic in the route body.
- **Exceptions:** Use HTTPException for API errors; optionally a single exception handler for domain errors (e.g. “not found”) that maps to 404/400.

## Domain Logic Rules
- **Income:** Fixed or variable incoming funds.
- **Debts:** Categorized (Food, Rent, etc.) and linked to Payment Methods (Pix, Credit, Debit, Cash).
- **Recurrence:** Debts must support a boolean `is_recurrent` flag.

## Working with Resources
When asked to create a new feature:
1. Align with **Product & UX** (AGENT.md): which user story or requirement it satisfies; keep flows and screens within the described MVP.
2. Identify if it's a new resource or an extension of an existing one.
3. Ensure `models.py` in the resource folder is imported in the central `src/ext/db.py` or `metadata` for Alembic to see it.
4. Check for code smells (Primitive Obsession, Long Methods) and for redundancy (duplicate exports, placeholder files, unnecessary factories) before finishing.

### Adding a new resource
1. Create `src/resources/<name>/` with `models.py`, `logic.py`, `repository.py`, `routes.py`, `templates/`, and `tests/`.
2. Define DB models (SQLModel, `table=True`) inheriting from the base model in `_base/models.py` where appropriate; add request/response schemas in `models.py`. Put all DB access in `repository.py` (use base repository helpers from `_base/repository.py` for generic CRUD). Put pure business functions in `logic.py`. Add a factory only if the resource needs one (overrides, fixtures, or construction from dict). Templates extend the base layout from `_base/templates/`; add partials only when needed.
3. Register the router in `src/main.py`; import the new models in `src/ext/db.py` (or metadata) so Alembic picks them up.
4. Add migration: `uv run alembic revision --autogenerate -m "add <name>"` then `uv run alembic upgrade head`.

### Adding an HTMX endpoint
1. Add an `async def` route in the resource’s `routes.py`; `await` a function from `logic.py` (no business logic in the route).
2. Return a small HTML fragment (e.g. from `templates/`) for `hx-swap`; prefer fragments over full-page responses.

## Out of Scope (MVP)
Do not add unless explicitly requested: **auth / login**, **multi-tenant**, **REST API for mobile**, **Open Banking / external APIs**. Keep the MVP focused on incomes and debts.

## Commits.
- We will use the semantic and atomic commit rules, each commit will have a prefix such as chore, feat, test, fix, doc...
