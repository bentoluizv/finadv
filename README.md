# FinAdv — Personal Financial Advisor

> Track where your money comes from and where it goes — personal finances, shared household expenses, trends, and bank sync in one place.

FinAdv is a personal finance web app built to grow with you: start by logging incomes and debts manually, import from your bank's CSV export, visualize trends, set budget goals, and sync automatically via Open Banking — all in a fast, keyboard-friendly interface.

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

**Prerequisites:** Python 3.14, [uv](https://astral.sh/uv), Docker, and `libnss3-tools` (for browser CA trust: `sudo apt install libnss3-tools -y`).

```bash
git clone <repo-url>
cd finadv
uv sync
```

All settings have working defaults defined in `src/ext/settings.py` — no configuration is required to get started. If you need to override a value (e.g. point to a different database), create a `.env` file in the project root:

```bash
# .env — optional, gitignored
DATABASE_URL=sqlite+aiosqlite:///./data/finadv.db
SQL_ECHO=true
```

## Docker dev environment

The local stack (app + Caddy HTTPS) runs with:

```bash
uv run task dev
```

### One-time setup per machine

This only needs to be done once per developer machine to establish DNS, browser trust, and kernel networking for `https://finadv.local`.

**Step 1 — Increase the UDP receive buffer (required for HTTP/3)**

Caddy uses QUIC (HTTP/3) on port 443 UDP. The default Linux kernel buffer is too small and causes a warning in Caddy's logs. Set it once and persist across reboots:

```bash
echo 'net.core.rmem_max=7500000' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=7500000' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**Step 2 — Add the local domain to `/etc/hosts`**

Check if it is already there:

```bash
grep finadv /etc/hosts
```

If the line is missing, add it:

```bash
echo "127.0.0.1 finadv.local" | sudo tee -a /etc/hosts
```

**Step 3 — Start the stack**

```bash
uv run task dev
```

Wait until you see this line in the output before continuing:

```
Application startup complete.
```

**Step 4 — Copy Caddy's CA certificate to the host**

Open a second terminal and run:

```bash
docker compose cp \
    caddy:/data/caddy/pki/authorities/local/root.crt \
    /usr/local/share/ca-certificates/caddy-local-ca.crt \
  && sudo update-ca-certificates
```

This installs Caddy's local CA into the OS trust store so `curl` and system tools accept `https://finadv.local`.

**Step 5 — Trust the CA in your browser**

Chrome, Chromium, and Edge use an NSS database separate from the OS store:

```bash
mkdir -p $HOME/.pki/nssdb
certutil -d sql:$HOME/.pki/nssdb -N --empty-password 2>/dev/null || true
certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n "Caddy Local CA" \
  -i /usr/local/share/ca-certificates/caddy-local-ca.crt
```

Firefox does not use the NSS database on disk. Instead, go to:
Settings → Privacy & Security → Certificates → View Certificates → Authorities → Import
and select `/usr/local/share/ca-certificates/caddy-local-ca.crt`.

**Step 6 — Restart the browser and open the app**

Fully close and reopen the browser (not just a new tab — the NSS database is loaded at browser startup). Then open:

[https://finadv.local](https://finadv.local)

You should see a valid padlock with no certificate warning.

---

The `db_data` Docker volume persists the SQLite database across restarts. To wipe it intentionally:

```bash
docker compose down -v
```

---

## Developer commands

| Task | Command |
|------|---------|
| Start Docker dev stack | `uv run task dev` |
| Stop Docker dev stack | `uv run task dev-down` |
| Tail app logs | `uv run task dev-logs` |
| Watch and rebuild CSS | `uv run task tailwind_watch` |
| Lint + type-check | `uv run task check` |
| Tests | `uv run pytest` |
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
| Docker build | Verifies the Dockerfile builds successfully on every PR |
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

See **[ROADMAP.md](ROADMAP.md)** for the full description of each phase.
