# FinAdv — Personal Financial Advisor

> Track where your money comes from and where it goes — personal finances, shared household expenses, trends, and bank sync in one place.

FinAdv is a personal finance web app built to grow with you: start by logging incomes and debts manually, import from your bank's CSV export, visualize trends, set budget goals, sync automatically via Open Banking, manage shared household expenses, and split any one-off expense with friends — all in a fast, keyboard-friendly interface.

---

## Tech stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.14, [uv](https://astral.sh/uv) |
| Web | FastAPI, HTMX (fasthx), htmy |
| Data | SQLModel, Alembic, pydantic-settings |
| Styling | Tailwind CSS (pytailwindcss) |
| Quality | Ruff, Ty, pytest |

---

## Getting started

**Prerequisites:** Python 3.14 and [uv](https://astral.sh/uv).

```bash
git clone <repo-url>
cd finadv
uv sync
```

Copy `.env.example` to `.env` (if provided) and set `DATABASE_URL`. The app uses SQLite by default — no database server required.

Apply migrations:

```bash
uv run alembic upgrade head
```

Build Tailwind CSS:

```bash
uv run task tailwind
```

Start the dev server:

```bash
uv run fastapi dev src/main.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Developer commands

| Task | Command |
|------|---------|
| Dev server | `uv run fastapi dev src/main.py` |
| Lint + type-check | `uv run task check` |
| Tests | `uv run pytest` |
| CSS build | `uv run task tailwind` |
| CSS watch | `uv run task tailwind_watch` |
| Add dependency | `uv add <pkg>` |

**After model changes:**

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

---

## Git workflow

This project follows a simple trunk-based flow. `main` is always deployable; all work happens on short-lived feature branches merged via pull request.

**Branch naming — match the commit prefix:**

| Prefix | When to use |
|--------|-------------|
| `feat/` | New feature |
| `fix/` | Bug fix |
| `chore/` | Tooling, dependencies, config |
| `docs/` | Documentation only |
| `test/` | Tests only |
| `refactor/` | Refactoring without behaviour change |

**Standard flow:**

```bash
# 1. Start from an up-to-date main
git checkout main
git pull origin main

# 2. Create a branch
git checkout -b feat/income-crud

# 3. Work, commit atomically
git add .
git commit -m "feat: add income creation endpoint"

# 4. Push and open a PR
git push -u origin feat/income-crud
gh pr create --fill
```

**Pull request expectations:**

- CI must pass (lint, type-check, tests) before merging.
- One logical change per PR — keep diffs small and focused.
- PR title follows the same semantic prefix as commits (`feat:`, `fix:`, etc.).
- Merge strategy: **merge commit** (preserves full branch history).
- Never force-push to `main`.

**Automated checks on every PR and push to main:**

| Check | What it runs |
|-------|-------------|
| Lint & type-check | `uv run task ruff` + `uv run task ty` |
| Tests | `uv run pytest --tb=short -q` |
| Migrations | `alembic upgrade head` → `downgrade base` → `upgrade head` (round-trip) |
| AI code review | CodeRabbit — reviews diff against architecture rules, coding standards, TDD requirements, and phase alignment |

CodeRabbit is configured in `.coderabbit.yaml`. To activate it, install the [CodeRabbit GitHub App](https://github.com/apps/coderabbit-ai) on the repository (free for public repos).

---

## Project layout

```
src/
  main.py                   # App entry point; mounts all routers
  resources/
    _base/                  # Shared base model, repository helpers, layout
    incomes/                # Income resource: models, logic, repository, routes, templates, tests
    debts/                  # Debt resource: same structure
  ext/                      # Infrastructure: DB engine, settings, shared fixtures
  static/                   # Built CSS and static assets
```

Full architecture, patterns, coding standards, and TDD workflow: **[AGENT.md](AGENT.md)**.

---

## Roadmap

| Phase | Name | Status |
|-------|------|--------|
| 1 | Core CRUD — Incomes & Debts | **current** |
| 2 | Overview Dashboard | planned |
| 3 | User-managed Categories | planned |
| 4 | Bank CSV Import | planned |
| 5 | Charts & Trends | planned |
| 6 | Budget Goals & Savings | planned |
| 7 | Auth / Login | planned |
| 8 | Notifications & Alerts | planned |
| 9 | Multi-user | planned |
| 10 | Households & Shared Expenses | planned |
| 11 | Open Banking | planned |
| 12 | Ad-hoc Expense Splitting | planned |

See **[ROADMAP.md](ROADMAP.md)** for the full description of each phase.
