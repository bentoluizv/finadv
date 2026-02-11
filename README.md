# FinAdv: Functional Financial Advisor

A minimalist, high-performance financial tracking system built with a hypermedia-first (HTMX) approach and functional domain logic.

## 🛠 Tech Stack
- **Runtime:** Python 3.14 (using `uv`)
- **Web:** FastAPI + HTMX (Server-Side Rendering)
- **Data:** SQLModel (SQLAlchemy + Pydantic) & Alembic
- **Tooling:** Ruff (Linter/Formatter), Ty (Static Typing)

## 🏗 Architecture:
- `/src/resources/`: Self-contained domain modules (Models, Logic, Routes, Templates).
- `/src/ext/`: Infrastructure and third-party integrations (DB, Open Finance, AI).
