# Agent Instructions: Financial Advisor

Coding standards and structure: see **`.cursorrules`**.

## Current Project State
Building across eleven planned phases:
- **Phase 1 (current):** Core CRUD for Incomes and Debts with lean data models and month-based list filtering.
- **Phase 2:** Overview dashboard — monthly balance, combined list, recurrent debts summary, and upcoming (future due-date) debts.
- **Phase 3:** User-managed Categories — separate category tables for incomes and debts; optional FK on each record.
- **Phase 4:** Bank CSV import — parse Nubank, Inter, and Itaú CSV exports into Incomes and Debts with a diff-and-approval panel.
- **Phase 5:** Charts & Trends — visualize monthly net balance, income vs debt over time, and spending by category.
- **Phase 6:** Budget Goals & Savings — set monthly spending limits per category and savings targets; track progress.
- **Phase 7:** Auth / Login — single-user email+password login; enables multi-device access and is a prerequisite for phases 8–12.
- **Phase 8:** Notifications & Alerts — proactive reminders for upcoming debts and budget-exceeded alerts.
- **Phase 9:** Multi-user — multiple independent accounts on the same installation; all existing data is scoped per user.
- **Phase 10:** Households & Shared Expenses — users form households, add shared expenses with custom per-member splits; each member's personal balance includes their share.
- **Phase 11:** Open Banking — auto-sync transactions via Brazil's Open Finance APIs; reuses the Phase 4 diff-and-approval panel.

See the **Roadmap** section for acceptance criteria per phase.

## Product & UX: How the app works

**Purpose:** FinAdv helps a single user act as their own financial adviser by tracking **incomes** and **debts** in one place, so they can see where money comes from and where it goes — including recurrent monthly obligations and upcoming bills.

**User:** One person managing their personal finances. Phase 7 (auth) enables multi-device for the same person. Phase 9 opens the installation to multiple independent users. Phase 10 introduces households — groups of users who share recurring expenses.

**How the user interacts:** Web app in the browser. Server-rendered pages with HTMX for partial updates (no SPA). Actions are: navigate (links), submit forms (add/edit/delete income or debt), filter by month, mark debts paid. Prefer small, focused screens and inline feedback (e.g. swap a row after create/delete/pay) instead of full-page reloads where it makes sense.

**Data models:**

- **Income** — `amount` (required), `source` (required, e.g. "Salary"), `type` (required: Fixed | Variable), `date` (required, defaults to today), `description` (optional). Phase 3 adds: `category_id` (FK to IncomeCategory, nullable).
- **Debt** — `amount` (required), `date` (required, defaults to today), `payment_method` (required: Pix | Credit | Debit | Cash — hardcoded enum), `is_recurrent` (bool, default False), `due_date` (optional — if in the future and `paid=False` the debt is "upcoming"), `paid` (bool, default False), `description` (optional). Phase 3 adds: `category_id` (FK to DebtCategory, nullable).
- **IncomeCategory** (Phase 3) — `name` (required). User-managed. Separate from DebtCategory.
- **DebtCategory** (Phase 3) — `name` (required). User-managed. Separate from IncomeCategory.
- **BudgetGoal** (Phase 6) — `category_id` (FK to DebtCategory, nullable), `amount` (monthly limit), `user_id` (Phase 10 adds FK).
- **SavingsGoal** (Phase 6) — `amount` (monthly target), `user_id` (Phase 10 adds FK).
- **Household** (Phase 10) — `name` (required). A named group of users.
- **HouseholdMember** (Phase 10) — `household_id`, `user_id`. A user can belong to multiple households.
- **HouseholdExpense** (Phase 10) — `household_id`, `amount` (full expense), `description`, `date`, `payment_method`. Added by any member.
- **ExpenseShare** (Phase 10) — `expense_id`, `user_id`, `amount` (this member's share). Shares must sum to the full expense amount. Each share flows into the member's personal balance as a Debt equivalent.

**What the app does — by phase:**

- **Phase 1 — Incomes & Debts:** Full CRUD for each. Lists default to the current calendar month; user can navigate months. Can mark a debt as paid/unpaid inline.
- **Phase 2 — Overview:** Dashboard for the selected month. Balance card (total income minus total debts = net). Combined chronological list (incomes + debts for selected month). Recurrent debts section (all `is_recurrent=True` debts, not month-filtered). Upcoming section (debts with `due_date` in the future and `paid=False`).
- **Phase 3 — Categories:** CRUD pages for IncomeCategory and DebtCategory. Income and Debt forms gain an optional category picker from their respective list. Category shown on list rows and detail views. Deleting a category sets affected records' `category_id` to NULL (no cascade delete).
- **Phase 4 — Bank CSV Import:** User uploads a CSV exported from their bank app (Nubank, Inter, or Itaú) for a selected month. The app detects the bank format, parses rows into a normalized Movement representation, diffs against existing Incomes and Debts for that month, and presents an approval panel before writing anything. Debits become Debts; credits become Incomes. Deduplication is key-based (stable hash of date + amount + description). Manual entries not present in the CSV are flagged informational but kept.
- **Phase 5 — Charts & Trends:** Visual summaries built from existing Income and Debt data. Monthly net balance over time (bar or line chart), income vs debt trend, and spending breakdown by category for the selected period. No new data model required.
- **Phase 6 — Budget Goals & Savings:** User sets monthly spending limits per category (e.g. "max R$600 on Food") and savings targets (e.g. "save R$500/month"). Overview and category views show progress vs targets. New `BudgetGoal` and `SavingsGoal` tables per user.
- **Phase 7 — Auth / Login:** Single-user email+password authentication. Session management. Prerequisite for Phases 8–11. Enables accessing the app from multiple devices with the same account.
- **Phase 8 — Notifications & Alerts:** Upcoming debt reminders (e.g. "rent due in 3 days") and budget-exceeded alerts (e.g. "you hit 90% of your Food budget"). Requires Phase 7 auth to have a destination (email). Alert rules are configurable per user.
- **Phase 9 — Multi-user:** A `user_id` is added to all existing records (Income, Debt, Category, Goal). Multiple people can register and each sees only their own data. Requires Phase 7 auth as foundation.
- **Phase 10 — Households & Shared Expenses:** Users form named households. Any member can add a `HouseholdExpense` with a custom split across members (`ExpenseShare`). The household view shows the full expense and all shares. Each member's personal overview includes their share as part of their balance. A user can belong to multiple households.
- **Phase 11 — Open Banking:** Auto-sync transactions via Brazil's Open Finance APIs. Replaces manual CSV upload with scheduled or on-demand bank sync. Reuses the Phase 4 diff-and-approval panel. Requires Phase 7 auth for per-user OAuth tokens.

**Functional requirements:**

- CRUD for **incomes**: create, list (month filter, default current month), edit, delete.
- CRUD for **debts**: create, list (month filter, default current month), edit, delete, mark paid/unpaid.
- **Overview** (Phase 2): month selector; balance summary; combined chronological list; recurrent debts section; upcoming debts section.
- **Categories** (Phase 3): separate CRUD for IncomeCategory and DebtCategory; optional category field on incomes and debts.
- **Bank CSV Import** (Phase 4): upload a bank CSV for a selected month; auto-detect bank format; parse into Movements; diff against existing records; approval panel before write.
- **Charts & Trends** (Phase 5): monthly net balance chart, income vs debt trend, spending by category breakdown.
- **Budget Goals & Savings** (Phase 6): set and track monthly spending limits per category; set and track savings targets.
- **Auth / Login** (Phase 7): email+password login; session management; multi-device support.
- **Notifications & Alerts** (Phase 8): upcoming debt reminders; budget-exceeded alerts; configurable rules per user.
- **Multi-user** (Phase 9): user registration; all data scoped per `user_id`; each user sees only their own records.
- **Households & Shared Expenses** (Phase 10): create/manage households; add shared expenses with custom per-member splits; household view and personal balance both reflect shares.
- **Open Banking** (Phase 11): bank sync via Open Finance APIs; diff-and-approval panel reused from Phase 4.
- Navigation from the layout to: Overview (home), Incomes, Debts. Phase 3 adds: Categories. Phase 4 adds: Import. Phase 10 adds: Households.
- Validation and clear error messages on all forms (required fields, valid amounts, valid dates).

**Non-functional requirements:**
- **Simplicity:** Few screens and concepts; no unnecessary features.
- **Clarity:** Labels understandable at a glance (e.g. "Recurrent", "Upcoming", "Fixed", "Variable").
- **Responsive:** Usable on small screens (mobile-friendly layout).
- **Accessibility:** Every screen must meet WCAG 2.1 AA. Required patterns: skip-to-content link, `aria-current="page"` on the active nav item, `<label>` associated with every input, `aria-required` / `aria-invalid` / `aria-describedby` for form validation errors, `aria-live="polite"` region for HTMX partial updates, `aria-label` on icon-only controls, and a visible `focus-visible` ring on all interactive elements. See `DESIGN.md` for the full reference.
- **Performance:** Fast responses; HTMX updates only the changed part where appropriate.

**User stories:**

*Phase 1:*
- As a user, I want to **add an income** (source, type, amount, date, optional note) so I can track what I earn.
- As a user, I want to **add a debt** (amount, payment method, date, recurrent flag, optional due date, optional note) so I can track what I owe or spend.
- As a user, I want to **list incomes and debts by month** (current month by default, navigable) so I can review one period at a time.
- As a user, I want to **edit or delete** any income or debt entry so I can fix mistakes.
- As a user, I want to **mark a debt as paid or unpaid** so I can track what is settled.
- As a user, I want to **navigate** between Overview, Incomes, and Debts from any screen.

*Phase 2:*
- As a user, I want to see a **monthly balance** (income minus debts = net) so I know if I am in the positive for that month.
- As a user, I want to see a **combined list** of all incomes and debts for the selected month in chronological order.
- As a user, I want to see all my **recurrent debts** in a dedicated section so I always know my fixed monthly obligations.
- As a user, I want to see **upcoming debts** (future due dates, unpaid) so I can plan ahead and avoid surprises.

*Phase 3:*
- As a user, I want to **create and manage income categories** (e.g. Salary, Freelance) so I can label where my money comes from.
- As a user, I want to **create and manage debt categories** (e.g. Food, Rent, Health) so I can label my expenses.
- As a user, I want to **assign a category** when adding or editing an income or debt so I can keep things organized.

*Phase 4:*
- As a user, I want to **upload my bank's CSV export** for a given month so I do not have to enter transactions manually.
- As a user, I want to **see a diff of what will be added or changed** before the import writes anything, so I stay in control.
- As a user, I want **existing records to be matched and skipped** when I re-import the same file, so I never get duplicates.
- As a user, I want **manually-added records** that are not in the CSV to be kept and flagged informational in the diff panel.

*Phase 5:*
- As a user, I want to see my **monthly net balance trend** over time so I can understand if my finances are improving.
- As a user, I want to see a **breakdown of spending by category** so I know where most of my money goes.
- As a user, I want to compare **income vs total debts** across months on a chart so I can spot problem months at a glance.

*Phase 6:*
- As a user, I want to **set a monthly spending limit per category** so I have a budget to aim for.
- As a user, I want to **see how close I am to my budget limit** in the category view and overview so I can adjust spending in time.
- As a user, I want to **set a monthly savings target** so the app tracks whether I am building reserves.

*Phase 7:*
- As a user, I want to **log in with email and password** so my data is protected and only I can access it.
- As a user, I want to **access the app from any device** using my account so I am not tied to one machine.

*Phase 8:*
- As a user, I want to **receive a reminder** when a debt is due soon so I do not miss payments.
- As a user, I want to **be alerted when I am close to or over a budget limit** so I can act before the month ends.
- As a user, I want to **configure which alerts I receive** so I only get notifications that are useful to me.

*Phase 9:*
- As a person, I want to **create my own account** so I can use the app independently from other users on the same installation.
- As a user, I want to be sure that **my data is private** and other users cannot see my incomes, debts, or goals.

*Phase 10:*
- As a user, I want to **create a household** and invite others so we can manage shared expenses together.
- As a household member, I want to **add a shared expense** (e.g. rent, utilities) and assign a custom amount to each member so splits reflect reality.
- As a household member, I want to **see all household expenses** in a dedicated view so I know what the group owes collectively.
- As a user, I want my **share of household expenses to appear in my personal balance** so my overview reflects my true financial position.
- As a user, I want to **belong to multiple households** (e.g. partner household and a flatmate household) independently.

*Phase 11:*
- As a user, I want to **connect my bank account** via Open Finance so my transactions are synced automatically.
- As a user, I want to **review and approve synced transactions** before they are saved, so I stay in control of my data.
- As a user, I want to **trigger a sync on demand** or have it happen on a schedule so my data is always up to date.

When implementing a feature, align with the phase it belongs to; do not add flows or screens that are out of scope (see Out of Scope and Roadmap).

## Project Layout
- **Entry point:** `src/main.py` (mounts routers, creates app).
- **Base resource:** `src/resources/_base/` — reusable building blocks for all resources. Not a domain resource (no routes mounted). Contains shared models, repository helpers, and a single layout template (see below). Add partials or shared templates only when a real use case appears.
- **Resources:** `src/resources/<name>/` — each has `models.py`, `logic.py`, `repository.py`, `routes.py`, `templates/`, and `tests/` (tests for that resource only). Domain resources inherit or use the base where appropriate.
- **Infrastructure:** `src/ext/` — e.g. `db.py` (async engine, `get_session` yielding `AsyncSession`), future async API clients. All models used by Alembic must be imported there (or in a central metadata). Shared test fixtures (e.g. test client, async session) live in `src/ext/` or project-root `conftest.py`.

## Tools & Dependencies (pyproject.toml)
- **Runtime:** Python >=3.14; **uv** (package manager and runner).
- **Web:** **FastAPI** (API + server; `[all]` includes Jinja2, static files, etc.); **HTMX** via CDN for partial updates.
- **Data:** **SQLModel** (ORM + Pydantic models); **Alembic** (DB migrations); **pydantic** (validation/settings); **orjson** (fast JSON); **python-ulid** (ULID identifiers).
- **Dev / quality:** **ruff** (lint + format); **ty** (static type checker); **pytest** + **pytest-asyncio** (tests, including async tests); **taskipy** (task runner from pyproject); **pytailwindcss** (Tailwind CSS build); **ignr** (CLI to fetch .gitignore templates from gitignore.io).

## Async-first rule

All request-handling and I/O must be **async**: use `async def` for routes, repository functions, and logic that performs DB or external API calls. Use **AsyncSession** (SQLModel) and async HTTP clients; do not use sync `Session` or blocking I/O in the request path. This keeps the event loop non-blocking and matches FastAPI async usage.

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

### Jinja2 + HTMX — full page and fragments (async routes)
```python
# src/main.py — one shared templates instance used project-wide
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Full page
@app.get('/', response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name='index.html', context={'active_page': 'overview'}
    )

# HTMX fragment (for list rows, tables, form regions)
@router.get('/debts', response_class=HTMLResponse)
async def list_debts(request: Request, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
    debts = await repository.list_all(session, Debt)
    return templates.TemplateResponse(
        request=request, name='debts/list.html', context={'items': debts, 'active_page': 'debts'}
    )
```

**Template context:** Pass a `dict` to `context={...}`. Always include `active_page` so the layout can highlight the active nav link.

Prefer **small HTML fragments** for list rows, tables, and form regions; use full-page templates only for top-level shells (layout + initial content). For dual HTML/JSON endpoints, check `request.headers.get('HX-Request')` and branch accordingly.

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
FastAPI can use orjson for response serialization (faster for large payloads). To enable: set a custom `JSONResponse` that uses `orjson.dumps`, or use FastAPI's built-in orjson support if available for your version. Request bodies are still parsed by FastAPI; use orjson mainly for responses when needed.

## Terminal & Tooling Protocol
- **Installation:** `uv add <package>`
- **Execution:** `uv run fastapi dev src/main.py`
- **Quality Control:** After editing Python files, use `ReadLints` (IDE feedback) then `uv run task check` (runs ruff then ty). See **Ruff (lint and format)** for rule explanations and recommendations.
- **Database Migrations:**
  1. Update `src/resources/<resource>/models.py` and import the new model in `migrations/env.py`.
  2. `uv run alembic revision --autogenerate -m "description"`
  3. `uv run alembic upgrade head`
- **Testing Alembic:** Use the `migrated_db_path` fixture (in `tests/conftest.py`): it runs `alembic upgrade head` against a temporary DB and yields the path. Tests in `tests/test_alembic.py` are atomic (no user action): they use this fixture or a fresh `tmp_path` and run upgrade/downgrade in-process. Run: `uv run pytest tests/test_alembic.py -v`.

## Environment & Config
- Prefer env vars and **pydantic-settings** (or a single settings module in `src/ext/`). Do not hardcode secrets or DB URLs.
- Use a conventional name for the DB: e.g. `DATABASE_URL` or `SQLITE_PATH`. For async SQLModel use `create_async_engine` (e.g. `sqlite+aiosqlite:///...` for SQLite). Document in README or here if you introduce one.

## Testing (TDD, business-logic focus)

Development is test-driven: for each functionality, write the test first, then implement only the code needed to make it pass. Do not add models, DB tables, or resource code without a test that defines the behavior.

- **Run:** `uv run pytest`
- **Location:** Inside each resource: `src/resources/<name>/tests/` (e.g. `test_logic.py`, `test_repository.py`, `test_routes.py`). Tests live next to the code they cover.
- **Focus:** Test business logic (`logic.py`) and repository behavior; avoid testing the framework or trivial glue. We do not test everything — only what defines and protects the functionality we are building.
- **Fixtures:** Resource-specific fixtures in that resource's `tests/conftest.py`; shared fixtures (DB session, test client) in `src/ext/conftest.py` or project-root `conftest.py`.

### Phase execution protocol (all phases)

For **every phase**, work in **minor TDD steps**. Use the phase's step table in [ROADMAP.md](ROADMAP.md) when one exists (e.g. P1.1–P1.13 for Phase 1).

**Per step:**

1. **Test first:** Write the test(s) that define the behaviour; run tests and confirm they fail (red).
2. **Implement:** Add only the code needed to make those tests pass (models → repository/factory if needed → logic → routes → templates, as required by the test).
3. **Verify:** Run `uv run task check` and `uv run pytest`; fix until green.

**After each step:** Ask the user whether to proceed to the next step (do not advance without confirmation).

## Static Assets
- **CSS:** Tailwind via **pytailwindcss** — run its watch/build as needed; keep built assets in a single known directory (e.g. `static/` under `src` or project root) and serve via FastAPI static mount. Use utility classes in templates/htmy components instead of custom CSS files where possible.
- **JS:** Rely on **HTMX** attributes (`hx-get`, `hx-post`, `hx-swap`, etc.) for interactivity. Do not introduce a SPA framework or custom front-end build unless explicitly requested.

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
- **Purpose:** Centralize creation of domain entities when you need overrides (e.g. explicit id/timestamps in tests) or building from a dict. If the model's `default_factory` is enough (e.g. BaseTable already sets id, created_at, updated_at), instantiate the model directly and skip a factory.
- **Location:** `src/resources/<name>/factory.py` or builder functions in `models.py` (e.g. `build_debt(...)`).
- **When to add:** Add a factory when you have repeated construction logic, test fixtures that need controlled ids/timestamps, or creation from external data. Do not add a factory "for consistency" if `Model(**kwargs)` is enough.

### Base resource (`src/resources/_base/`)
Reusable logic and templates shared by all resources. Do not mount routes for `_base`; it is not a domain.

- **Base models (`_base/models.py`):** Shared fields or a base table class that all domain models can inherit (e.g. `id: str` ULID, `created_at`, `updated_at`). Resource models inherit from this base so schema and migrations stay consistent.
- **Base repository (`_base/repository.py`):** Generic, reusable **async** repository helpers (e.g. `async def get_by_id(session, Model, id)`, `list_all(session, Model)`, `add(session, entity)`, `delete_by_id(session, Model, id)`). Resource repositories `await` these where possible and add only resource-specific queries.
- **Base templates (`_base/templates/`):** One shared layout (e.g. `layout.html`). Add partials (form_errors, csrf, etc.) only when you have a concrete use case and real content; avoid placeholder files.

## Avoiding redundancy and unnecessary code
- **Single source of truth:** Do not duplicate values. E.g. get `database_url` from settings only; do not re-export it as `DATABASE_URL` elsewhere unless a tool (e.g. Alembic) strictly requires it.
- **One entry point per concept:** Prefer one way to obtain something (e.g. `get_settings()` or `settings`, not both unless Depends needs the callable). Document the preferred one.
- **YAGNI (You Aren't Gonna Need It):** Do not add code "for later." No placeholder partials, stub files, or "might be useful" helpers. Add form_errors, CSRF, or a base factory when a real feature needs them.
- **Lean tests:** Test behavior, not framework. Prefer one or two focused tests per concern; merge tests that only assert the same thing in different ways. Avoid testing that a library does what it says (e.g. that a model has fields defined in code).
- **Minimal exports:** Only export what other modules use. Drop `__all__` entries and module-level names that nothing imports.

## FastAPI Best Practices
- **Routers:** Use `APIRouter(prefix="/<resource>", tags=["<Resource>"])` per resource; include in `app` in `src/main.py`. Route handlers are `async def`.
- **Dependency injection:** Use `Depends()` for async DB session (e.g. `get_session` yielding `AsyncSession`), config, and reusable logic. Define a single async session dependency in `src/ext/db.py` and inject it into routes that need it.
- **Request/response:** Use Pydantic models (or SQLModel) for request body and `response_model=` on routes. Prefer explicit schemas in `models.py` over returning raw ORM objects when the shape differs from the DB.
- **Status codes:** Set explicit `status_code` where it matters (e.g. `201` on create, `404` when not found, `204` on delete).
- **Thin routes:** Route handlers should: validate input (via Pydantic), `await` logic/repository, return response. No business or DB logic in the route body.
- **Exceptions:** Use HTTPException for API errors; optionally a single exception handler for domain errors (e.g. "not found") that maps to 404/400.

## Domain Logic Rules

**Income:**
- `type` is a fixed enum: `Fixed` (predictable, recurring salary) or `Variable` (one-off or irregular payment).
- `date` is when the income was received; defaults to today.

**Debt:**
- `payment_method` is a fixed enum: `Pix`, `Credit`, `Debit`, `Cash`. No user management needed.
- `is_recurrent=True` means the debt repeats monthly (e.g. rent). Shown in the recurrent section of the Overview regardless of selected month.
- A debt is **upcoming** when `due_date` is a future date and `paid=False`. Shown in the upcoming section of the Overview.
- `paid` can be toggled inline from the debt list or the Overview. Toggling does not affect the balance (paid debts are still counted as expenses for the month).
- `date` is when the expense occurred (or was registered); `due_date` is the payment deadline (optional).

**Balance (Phase 2):**
- Calculated for the selected month: `sum(income.amount) - sum(debt.amount)` where both income.date and debt.date fall within the selected year-month.
- Paid and unpaid debts are both counted in the balance (spending happened regardless of payment status).

**Categories (Phase 3):**
- `IncomeCategory` and `DebtCategory` are separate tables; a category belongs to only one domain.
- `category_id` on Income and Debt is nullable — existing records without a category are valid.
- Deleting a category must set `category_id = NULL` on all affected records (no cascade delete of records).

## Roadmap

### Phase 1 — Core CRUD (current)

**Goal:** Register and manage incomes and debts. Lists filterable by calendar month.

**Atomic steps (TDD, in order):** P1.1 → … → P1.13. For each step, write the test first, then implement. See [ROADMAP.md](ROADMAP.md) Phase 1 for the table and use cases (UC-1.1–UC-1.9). Phase 1 follows the phase execution protocol above; the agent asks before moving to the next step.

**Acceptance criteria (summary):**
- CRUD for Income and Debt; month-filtered lists; month navigation; paid toggle for debts; inline validation; HTMX partial updates.

### Phase 2 — Overview dashboard
**Goal:** Give the user a financial picture of the selected month at a glance. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `overview` (read-only, pulls from incomes + debts repositories).

**Acceptance criteria:**
- Month selector shown on the page; defaults to current month.
- Balance card displays: total income for month, total debts for month, net (income minus debts). Both paid and unpaid debts count.
- Combined list shows all incomes and debts for the selected month, sorted by date descending, with clear visual distinction (income vs debt).
- Recurrent debts section lists all debts with `is_recurrent=True` (not filtered by month), so the user always sees their fixed obligations.
- Upcoming section lists debts where `due_date` is in the future and `paid=False`, sorted by due_date ascending.

### Phase 3 — User-managed Categories
**Goal:** Let the user label incomes and debts with their own categories. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `income_categories`, `debt_categories`. Extensions to `incomes` and `debts`.

**Acceptance criteria:**
- Can create, rename, and delete income categories. Deleting sets `category_id=NULL` on affected incomes.
- Can create, rename, and delete debt categories. Deleting sets `category_id=NULL` on affected debts.
- Income and debt create/edit forms show an optional category picker from the relevant list.
- Category name shown on income and debt list rows.
- Navigation in the layout includes a link to Categories management.

### Phase 4 — Bank CSV Import
**Goal:** Let the user import a monthly CSV exported from their bank app so they do not have to enter transactions manually. The app diffs the parsed data against existing records and asks for approval before writing anything. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `imports` (new — upload, parse, diff, approve). Reads from and writes to `incomes` and `debts` repositories.

**Supported banks (initial):** Nubank, Inter, Itaú.

**Key concept — Movement:**
An intermediate, bank-neutral record produced by each bank parser. Not stored in the DB; used only during the import flow.

```
Movement:
  bank_ref: str        # sha256(date + amount + description) — deduplication key
  date: date
  amount: Decimal
  direction: Credit | Debit   # Credit → Income, Debit → Debt
  description: str
  bank: Bank           # Nubank | Inter | Itau
```

**Bank parsers:**
Each parser is a pure function `parse(file_content: str) -> list[Movement]`. Bank is auto-detected from CSV column headers. No bank-specific logic leaks outside the parser module.

| Bank | Notable format details |
|------|----------------------|
| Nubank | UTF-8; columns: date, category, title, amount (negative = debit) |
| Inter | UTF-8; credit and debit may be in separate columns |
| Itaú | Latin-1 encoded, semicolon-separated, locale date format |

**Import flow:**
1. User selects month and uploads CSV.
2. App detects bank format, parses rows → `list[Movement]`.
3. App queries existing Incomes + Debts for that month and computes a diff.
4. Diff panel (HTMX fragment) is shown — no write yet.
5. User reviews and approves; confirmed rows are bulk-created or updated.

**Diff states:**

| State | Meaning | Default action | UI |
|-------|---------|---------------|-----|
| New | Movement not in app | Include (pre-checked) | Green |
| Matched | Exists, identical | Skip | Gray |
| Changed | Exists, differs | Include, shows old → new | Yellow |
| Manual-only | In app, not in CSV | Keep (informational) | Blue |

**Classification rules (no override in UI):**
- `Credit` → Income. `Debit` → Debt. If the user disagrees, they fix the record manually after import.

**Acceptance criteria:**
- Upload page accepts CSV; detects bank from headers; rejects unrecognised format with a clear error.
- Diff panel shows all four states; matched rows are collapsed by default.
- "Approve all new" shortcut pre-checks all New rows.
- Submitting the approved diff creates new records and updates changed records; Matched and Manual-only records are untouched.
- Re-importing the same file produces zero New or Changed rows (idempotent).
- Navigation in the layout includes a link to Import.

## Working with Resources

Development is test-driven: for each functionality, add a test first (focused on business logic), then the minimal code to pass it. Do not create models, DB tables, or new resource pieces for behavior you are not yet testing.

When asked to create a new feature:
1. Align with **Product & UX** and the **Roadmap** phase it belongs to; do not implement features from a later phase unless asked.
2. Identify if it is a new resource or an extension of an existing one.
3. For each piece of behavior: write the test, then add only the models/repository/logic/routes/templates required by that test. Import new models in `src/ext/db.py` (or metadata) when you add a migration so Alembic sees them.
4. Check for code smells and redundancy (duplicate exports, placeholder files, unnecessary factories) before finishing.

### Adding a new resource (test-first)

1. Create `src/resources/<name>/` and add files only as a testable functionality needs them (typically `tests/` first, then `models.py`, `repository.py`, `logic.py`, `routes.py`, `templates/` as required).
2. For each functionality: write the test, then implement. Define DB models and request/response schemas when a test needs them; put DB access in `repository.py` (use base helpers from `_base/repository.py`), business rules in `logic.py`. Add a factory only when tests or creation flow need it. Add templates when a route or HTMX endpoint needs them.
3. Register the router in `src/main.py` when you add the first route; import the new models in `src/ext/db.py` (or metadata) for Alembic.
4. Add a migration only when you have new or changed models: `uv run alembic revision --autogenerate -m "add <name>"` then `uv run alembic upgrade head`.

### Adding an HTMX endpoint
1. Add an `async def` route in the resource's `routes.py`; `await` a function from `logic.py` (no business logic in the route).
2. Return `templates.TemplateResponse(request=request, name='...', context={...})` with a small HTML fragment for `hx-swap`; prefer fragments over full-page responses.
3. For dual HTML/JSON endpoints, check `request.headers.get('HX-Request')` and return HTML for HTMX requests, JSON otherwise.

### Phase 5 — Charts & Trends
**Goal:** Turn the accumulated Income and Debt data into visual summaries so the user can spot patterns and problem months at a glance. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `overview` extended (read-only; pulls from incomes + debts repositories). No new DB tables needed.

**Acceptance criteria:**
- Monthly net balance chart (income minus debts per month) covering the last 12 months.
- Income vs total debts bar or line chart for the selected period.
- Spending breakdown by category for the selected month (donut or bar chart).
- Charts are rendered server-side (SVG or a lightweight JS chart lib via CDN); no SPA framework introduced.

### Phase 6 — Budget Goals & Savings
**Goal:** Let the user set monthly spending targets per category and savings goals, and track progress against them. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `budget_goals`, `savings_goals` (new). Extensions to `overview`.

**Acceptance criteria:**
- Can create, edit, and delete a monthly spending limit for any DebtCategory.
- Category view and Overview show actual spend vs budget limit for the current month (e.g. progress bar).
- Can create, edit, and delete a monthly savings target (target amount per month).
- Overview shows actual savings (net balance when positive) vs savings target.
- Deleting a category does not delete its budget goal; goal becomes unlinked.

### Phase 7 — Auth / Login
**Goal:** Protect the app with single-user email+password authentication and enable multi-device access. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `auth` (new — login, logout, session). All existing resources become session-gated.

**Acceptance criteria:**
- Login page with email + password. Invalid credentials show a clear error.
- Authenticated session persists across browser restarts (secure cookie).
- All routes redirect to login if no valid session is present.
- Logout clears the session.
- No registration flow — single user, credentials configured via environment variables or a one-time setup command.

### Phase 8 — Notifications & Alerts
**Goal:** Proactively inform the user about upcoming debts and budget limits so they can act before it is too late. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `alerts` (new — rules, delivery log). Requires Phase 7 auth.

**Acceptance criteria:**
- User can configure an upcoming-debt reminder: how many days before `due_date` to be notified.
- User can configure a budget-limit alert: notify when spending reaches X% of the limit for a category.
- Alerts are delivered by email (requires SMTP config in settings).
- User can enable or disable each alert type individually.
- Delivery log shows sent alerts (date, type, message) for reference.

### Phase 9 — Multi-user
**Goal:** Open the installation to multiple independent users, each with their own private data. Prerequisite for Phase 10. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `users` (new — registration, account). `user_id` FK added to all existing resources via migration. Requires Phase 7 auth.

**Acceptance criteria:**
- Registration page: email + password. No invite required (open registration, or admin-controlled via config).
- Each user sees only their own Incomes, Debts, Categories, Goals, and Import history.
- Existing single-user data is migrated to the first registered account.
- Login and session management work per user (Phase 7 foundation reused).
- No user can access or modify another user's records.

### Phase 10 — Households & Shared Expenses
**Goal:** Let users form households, record shared expenses with custom per-member splits, and have each member's share reflected in their personal balance automatically. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `households`, `household_members`, `household_expenses`, `expense_shares` (all new). Requires Phase 9 multi-user.

**Key rules:**
- A user can belong to multiple households.
- Any household member can add a `HouseholdExpense`.
- When adding an expense, the creator assigns a custom `amount` to each member. Shares must sum to the full expense amount.
- Each `ExpenseShare` contributes to the member's personal balance as a debt-equivalent (counted in their monthly total debts).
- Deleting a household expense removes all its shares and withdraws them from members' balances.
- A user leaving a household does not delete past expense shares; historical data is preserved.

**Acceptance criteria:**
- Can create, rename, and delete a household.
- Can invite existing users to a household; invited user must accept.
- Can add a shared expense with a description, date, payment method, full amount, and custom per-member split.
- Validation: shares must sum to the full expense amount before saving.
- Household view lists all expenses with each member's share and payment status.
- Personal overview and balance include the user's expense shares for the selected month.
- Can mark a share as paid (own share only).
- Navigation includes a Households link for users who belong to at least one household.

### Phase 11 — Open Banking
**Goal:** Auto-sync transactions from the user's bank via Brazil's Open Finance APIs, replacing manual CSV uploads. Work in minor TDD steps (from ROADMAP when defined); test first, then implement; ask before next step.

Resources: `bank_connections` (new — OAuth tokens, sync state). Reuses `imports` diff-and-approval logic from Phase 4. Requires Phase 7 auth.

**Acceptance criteria:**
- User can connect a supported bank account via Open Finance OAuth flow.
- User can trigger a manual sync or configure a sync schedule (e.g. daily).
- Synced transactions go through the same diff-and-approval panel as Phase 4 CSV import.
- User can disconnect a bank connection; existing records are kept.
- Supported banks at launch: same initial set as Phase 4 (Nubank, Inter, Itaú) subject to Open Finance API availability.

### Phase 12 — Ad-hoc Expense Splitting
**Goal:** Allow any single expense to be split with any set of people — registered users or named non-users — without requiring a permanent household group.

Resources: `expense_splits`, `split_participants` (new). Requires Phase 9 (multi-user).

**Acceptance criteria:**
- Any Debt can be converted to a split expense; standalone splits are also supported.
- Participants can be registered users (by email) or named non-users (name + optional email).
- Per-participant amounts must sum to the total expense amount; validated server-side.
- Payer sees all participants and their settlement status.
- Registered participants see only their own share and the total; not other participants' amounts.
- Registered participants can mark their own share as paid.
- Payer can mark non-user participants' shares as paid on their behalf.
- Optional email notification to non-user participants on split creation.
- Splits navigation added to layout.

## Out of Scope
Do not add unless explicitly requested: **REST API for mobile**, **charts library beyond what is needed for Phase 5**, **external expense-splitting services (e.g. Splitwise integration)**. Keep work phase-focused; do not implement features from a later phase unless asked.

## Commits
- **Semantic prefixes:** Every commit message starts with one of: `feat`, `fix`, `test`, `refactor`, `chore`, `docs`, `style`, `ci`.
- **Atomic:** One logical change per commit — do not bundle a feature with its migration and a bug fix in the same commit.
- **Imperative mood:** Write the subject line as an instruction, e.g. `feat: add debt creation endpoint` not `added debt creation`.
- **No `--no-verify`:** Never skip pre-commit hooks unless explicitly asked.
- **When to commit:** Only when the user explicitly asks. Do not auto-commit after every change.
