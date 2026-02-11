# AI Coding Standards: FinAdv

## Role & Tone
Act as a Lead Python Developer. Prioritize simplicity, type safety, and functional programming.

## Structural Constraints
- **Location:** All code must live in `/src`.
- **Resource Pattern:** Group by domain. A new resource (e.g., `debts`) must contain `models.py`, `logic.py`, `routes.py`, and a `/templates` folder.
- **External Pattern:** Infrastructure (DB, API clients) must live in `/src/ext`.

## Technical Requirements (Python 3.14)
- **Dependency Management:** Always use `uv`.
- **Typing:** Use `ty`. Every function must have complete type hints.
- **Data Modeling:** Use `SQLModel`. Inherit from `SQLModel, table=True` only for DB entities.
- **Functional Logic:** Business rules must be pure functions in `logic.py`. Routes call these functions; they don't contain logic themselves.

## UI Pattern (HTMX)
- **Fragments:** Prefer returning small HTML fragments for `hx-swap` over full pages.

## Code Smells to Avoid
- **Deep Nesting:** If code is more than 3 levels deep, refactor.
- **Class Overuse:** Avoid classes unless required by SQLModel/Pydantic.
- **The "Manager" Trap:** Do not create `DebtManager` or `IncomeService` classes. Use modules.

## Simplicity over Complexity
