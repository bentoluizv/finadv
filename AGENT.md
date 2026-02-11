# Agent Instructions: Financial Advisor

Coding standards and structure: see **`.cursorrules`**.

## Current Project State
Building the MVP for tracking Incomes and Debts (Sporadic/Recurrent).

## Project Layout
- **Entry point:** `src/main.py` (mounts routers, creates app).
- **Base resource:** `src/resources/_base/` — reusable building blocks for all resources. Not a domain resource (no routes mounted). Contains shared models, repository helpers, and templates (see below).
- **Resources:** `src/resources/<name>/` — each has `models.py`, `logic.py`, `repository.py`, `routes.py`, `templates/`, and `tests/` (tests for that resource only). Domain resources inherit or use the base where appropriate.
- **Infrastructure:** `src/ext/` — e.g. `db.py` (engine, session), future API clients. All models used by Alembic must be imported there (or in a central metadata). Shared test fixtures (e.g. test client, base DB fixture) live in `src/ext/` or project-root `conftest.py`.

## Tools & Dependencies (pyproject.toml)
- **Runtime:** Python ≥3.14; **uv** (package manager and runner).
- **Web:** **FastAPI** (API + server; `[all]` includes Jinja2, static files, etc.); **fasthx** (HTMX integration for FastAPI); **htmy** (HTML templating).
- **Data:** **SQLModel** (ORM + Pydantic models); **Alembic** (DB migrations); **pydantic** (validation/settings); **orjson** (fast JSON); **python-ulid** (ULID identifiers).
- **Dev / quality:** **ruff** (lint + format); **ty** (static type checker); **pytest** (tests); **taskipy** (task runner from pyproject); **pytailwindcss** (Tailwind CSS build); **ignr** (CLI to fetch .gitignore templates from gitignore.io).

## Terminal & Tooling Protocol
- **Installation:** `uv add <package>`
- **Execution:** `uv run fastapi dev src/main.py`
- **Quality Control:** `uv run ruff check src --fix`; `uv run ty`
- **Database Migrations:**
  1. Update `src/resources/<resource>/models.py`.
  2. `uv run alembic revision --autogenerate -m "description"`
  3. `uv run alembic upgrade head`

## Environment & Config
- Prefer env vars and **pydantic-settings** (or a single settings module in `src/ext/`). Do not hardcode secrets or DB URLs.
- Use a conventional name for the DB: e.g. `DATABASE_URL` or `SQLITE_PATH`. Document in README or here if you introduce one.

## Testing
- **Run:** `uv run pytest`
- **Location:** Inside each resource: `src/resources/<name>/tests/` (e.g. `test_logic.py`, `test_repository.py`, `test_routes.py`). Tests live next to the code they cover, same as models, routes, and logic.
- **Fixtures:** Resource-specific fixtures in that resource’s `tests/conftest.py`; shared fixtures (DB session, test client) in `src/ext/conftest.py` or project-root `conftest.py`.

## Static Assets
- **CSS:** Tailwind via **pytailwindcss** — run its watch/build as needed; keep built assets in a single known directory (e.g. `static/` under `src` or project root) and serve via FastAPI static mount.

## Standard Patterns

### Repository
- **Purpose:** Abstract all database access for a resource in one place so logic and routes stay free of session/query details.
- **Location:** `src/resources/<name>/repository.py`.
- **Content:** Functions that take a session (or dependency) and perform CRUD/queries (e.g. `get_by_id(session, id)`, `list_all(session)`, `add(session, entity)`, `delete(session, id)`). Return domain models or None; raise or return Result-style for errors if you prefer.
- **Usage:** Routes and logic call repository functions; they do not build raw SQL or use `session.query` directly outside the repository.

### Factory
- **Purpose:** Centralize creation of domain entities with defaults (e.g. for new records or test data), so construction logic is not scattered.
- **Location:** `src/resources/<name>/factory.py` or factory functions in `models.py` (e.g. `build_debt(...)`).
- **Content:** Functions that return new model instances (e.g. with ULID, defaults, or required fields). Use for creating test fixtures and for building entities before passing to repository.
- **Usage:** Tests and routes use the factory instead of manually instantiating with many kwargs.

### Base resource (`src/resources/_base/`)
Reusable logic and templates shared by all resources. Do not mount routes for `_base`; it is not a domain.

- **Base models (`_base/models.py`):** Shared fields or a base table class that all domain models can inherit (e.g. `id: str` ULID, `created_at`, `updated_at`). Resource models inherit from this base so schema and migrations stay consistent.
- **Base repository (`_base/repository.py`):** Generic, reusable repository helpers (e.g. `get_by_id(session, Model, id)`, `list_all(session, Model)`, `add(session, entity)`, `delete_by_id(session, Model, id)`). Resource repositories call these where possible and add only resource-specific queries.
- **Base templates (`_base/templates/`):** Shared layout and partials (e.g. `layout.html` with head/nav/footer, `form_errors.html`, `csrf.html`). Resource templates extend the base layout or include these partials so UI stays consistent and DRY.

## FastAPI Best Practices
- **Routers:** Use `APIRouter(prefix="/<resource>", tags=["<Resource>"])` per resource; include in `app` in `src/main.py`.
- **Dependency injection:** Use `Depends()` for DB session (e.g. `get_session`), config, and reusable logic. Define a single session dependency in `src/ext/db.py` and inject it into routes that need it.
- **Request/response:** Use Pydantic models (or SQLModel) for request body and `response_model=` on routes. Prefer explicit schemas in `models.py` over returning raw ORM objects when the shape differs from the DB.
- **Status codes:** Set explicit `status_code` where it matters (e.g. `201` on create, `404` when not found, `204` on delete).
- **Thin routes:** Route handlers should: validate input (via Pydantic), call logic/repository, return response. No business or DB logic in the route body.
- **Exceptions:** Use HTTPException for API errors; optionally a single exception handler for domain errors (e.g. “not found”) that maps to 404/400.

## Domain Logic Rules
- **Income:** Fixed or variable incoming funds.
- **Debts:** Categorized (Food, Rent, etc.) and linked to Payment Methods (Pix, Credit, Debit, Cash).
- **Recurrence:** Debts must support a boolean `is_recurrent` flag.

## Working with Resources
When asked to create a new feature:
1. Identify if it's a new resource or an extension of an existing one.
2. Ensure `models.py` in the resource folder is imported in the central `src/ext/db.py` or `metadata` for Alembic to see it.
3. Check for code smells (Primitive Obsession, Long Methods) before finishing.

### Adding a new resource
1. Create `src/resources/<name>/` with `models.py`, `logic.py`, `repository.py`, `routes.py`, `templates/`, and `tests/`.
2. Define DB models (SQLModel, `table=True`) inheriting from the base model in `_base/models.py` where appropriate; add request/response schemas in `models.py`. Put all DB access in `repository.py` (use base repository helpers from `_base/repository.py` for generic CRUD). Put pure business functions in `logic.py`; use a Factory for entity creation. Templates should extend or include base layout/partials from `_base/templates/`.
3. Register the router in `src/main.py`; import the new models in `src/ext/db.py` (or metadata) so Alembic picks them up.
4. Add migration: `uv run alembic revision --autogenerate -m "add <name>"` then `uv run alembic upgrade head`.

### Adding an HTMX endpoint
1. Add the route in the resource’s `routes.py`; call a pure function from `logic.py` (no business logic in the route).
2. Return a small HTML fragment (e.g. from `templates/`) for `hx-swap`; prefer fragments over full-page responses.

## Out of Scope (MVP)
Do not add unless explicitly requested: **auth / login**, **multi-tenant**, **REST API for mobile**, **Open Banking / external APIs**. Keep the MVP focused on incomes and debts.

## Commits.
- We will use the semantic and atomic commit rules, each commit will have a prefix such as chore, feat, test, fix, doc...
