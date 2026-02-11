# Agent Instructions: Financial Advisor

## Current Project State
Building the MVP for tracking Incomes and Debts (Sporadic/Recurrent).

## Terminal & Tooling Protocol
- **Installation:** `uv add <package>`
- **Execution:** `uv run fastapi dev src/main.py`
- **Quality Control:** - `uv run ruff check src --fix`
  - `uv run ty`
- **Database Migrations:**
  1. Update `src/resources/<resource>/models.py`.
  2. `uv run alembic revision --autogenerate -m "description"`
  3. `uv run alembic upgrade head`

## Domain Logic Rules
- **Income:** Fixed or variable incoming funds.
- **Debts:** Categorized (Food, Rent, etc.) and linked to Payment Methods (Pix, Credit, Debit, Cash).
- **Recurrence:** Debts must support a boolean `is_recurrent` flag.

## Working with Resources
When asked to create a new feature:
1. Identify if it's a new resource or an extension of an existing one.
2. Ensure `models.py` in the resource folder is imported in the central `src/ext/db.py` or `metadata` for Alembic to see it.
3. Check for code smells (Primitive Obsession, Long Methods) before finishing.

## Commits.
- We will use the semantic and atomic commit rules, each commit will have a prefix such as chore, feat, test, fix, doc...
