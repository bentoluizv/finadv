# FinAdv: Functional Financial Advisor

A minimalist financial tracking system for incomes and debts: FastAPI, HTMX, and functional domain logic. Single-user MVP—track where money comes from and where it goes.

## Prerequisites

- Python 3.14
- [uv](https://astral.sh/uv)

## Setup

```bash
git clone <repo-url>
cd finadv
uv sync
```

Configure via environment (e.g. `.env`); use pydantic-settings. No hardcoded secrets or DB URLs.

## Running the app

- **Dev server:** `uv run fastapi dev src/main.py`
- **CSS:** `uv run task tailwind` (one-off) or `uv run task tailwind_watch` (watch). Assets from `src/static/` served at `/static/`.

## Developer workflow

| Action | Command |
|--------|---------|
| Lint + type-check | `uv run task check` |
| Lint only | `uv run task ruff` |
| Type-check only | `uv run task ty` |
| Tests | `uv run pytest` |
| Tailwind build | `uv run task tailwind` |
| Tailwind watch | `uv run task tailwind_watch` |

Run **`uv run task check`** after editing Python under `src`; fix issues before committing.

**Migrations (after model changes):**

1. Update `src/resources/<resource>/models.py`; ensure models are imported for Alembic.
2. `uv run alembic revision --autogenerate -m "description"`
3. `uv run alembic upgrade head`

**Add dependency:** `uv add <pkg>` or `uv add --dev <pkg>`.

## Architecture

Code lives under **`src/`**.

| Path | Purpose |
|------|---------|
| `src/resources/<name>/` | Domain resource: `models.py`, `repository.py`, `logic.py`, `routes.py`, `templates/`, `tests/` |
| `src/resources/_base/` | Shared base model, repository helpers, layout; no routes |
| `src/ext/` | DB, settings, shared fixtures |
| `src/static/` | Built CSS and static assets |

**Layers:** models → repository → logic → routes → templates → tests. Routes only validate, call logic/repository, and return; no DB or business logic in routes. All DB access in `repository.py`; all I/O async.

Details and patterns: **AGENT.md**.

## Testing

- **Location:** `src/resources/<name>/tests/` next to the code; shared tests in project `tests/`.
- **Focus:** Behavior and outcomes; avoid testing the framework. One main concern per test; use shared fixtures from `conftest.py`.
- **Async:** Use `async def` tests; asyncio mode is set in `pyproject.toml`.

Run: `uv run pytest` (optionally `-v` or a path).

## Code quality

- **Ruff:** Single quotes, 2-space indent, 88-char line length. Rule sets: E, F, I, UP, B, C4, SIM (see AGENT.md).
- **Commits:** Semantic, atomic; prefix: `chore`, `feat`, `test`, `fix`, `doc`, etc.

## More

- **AGENT.md** — Product/UX, layout, Ruff details, patterns, adding resources, migrations, commits.
- **.cursorrules** — Coding standards for AI-assisted editing.

## Tech stack

- **Runtime:** Python 3.14, uv  
- **Web:** FastAPI, HTMX (fasthx), htmy  
- **Data:** SQLModel, Alembic, pydantic-settings  
- **Quality:** Ruff, Ty, pytest, taskipy  
- **CSS:** Tailwind (pytailwindcss) → `src/static/output.css`
