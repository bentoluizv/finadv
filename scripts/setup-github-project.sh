#!/usr/bin/env bash
# Creates the FinAdv GitHub Project and all phase issues.
# Requirements: gh CLI authenticated (gh auth status), remote origin set.
set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_TITLE="FinAdv MVP"
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)

if [[ -z "$REPO" ]]; then
  echo "ERROR: no GitHub remote found. Run 'gh repo create' or push to GitHub first."
  exit 1
fi

OWNER=$(echo "$REPO" | cut -d'/' -f1)

echo "Repo  : $REPO"
echo "Owner : $OWNER"
echo ""

# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------
echo "==> Creating labels..."

create_label() {
  local name="$1" color="$2" desc="$3"
  if gh label list --repo "$REPO" --json name -q '.[].name' | grep -qx "$name"; then
    echo "  label '$name' already exists, skipping"
  else
    gh label create "$name" --repo "$REPO" --color "$color" --description "$desc"
    echo "  created label '$name'"
  fi
}

create_label "phase-1"  "0075ca" "Phase 1: Core CRUD"
create_label "phase-2"  "e4e669" "Phase 2: Overview dashboard"
create_label "phase-3"  "d93f0b" "Phase 3: User-managed Categories"
create_label "chore"    "ededed" "Setup, tooling, infrastructure"

# ---------------------------------------------------------------------------
# GitHub Project
# ---------------------------------------------------------------------------
echo ""
echo "==> Creating GitHub Project..."

# gh project create has a bug in some CLI versions (undeclared $query var).
# Use gh api graphql directly instead.
OWNER_ID=$(gh api user --jq .node_id)

PROJECT_JSON=$(gh api graphql -f query='
  mutation($ownerId: ID!, $title: String!) {
    createProjectV2(input: {ownerId: $ownerId, title: $title}) {
      projectV2 { id number url }
    }
  }' -f ownerId="$OWNER_ID" -f title="$PROJECT_TITLE")

PROJECT_NUMBER=$(echo "$PROJECT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['createProjectV2']['projectV2']['number'])")
PROJECT_URL=$(echo "$PROJECT_JSON"    | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['createProjectV2']['projectV2']['url'])")

echo "  Project: $PROJECT_URL  (number: $PROJECT_NUMBER)"

echo "  Linking project to repo $REPO..."
gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$REPO"
echo "  Linked."

# ---------------------------------------------------------------------------
# Helper: create issue + add to project
# ---------------------------------------------------------------------------
add_issue() {
  local title="$1" label="$2" body="$3"
  echo ""
  echo "  Issue: $title"
  local url
  url=$(gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --label "$label" \
    --body "$body")
  gh project item-add "$PROJECT_NUMBER" --owner "$OWNER" --url "$url" > /dev/null
  echo "  -> $url"
}

# ---------------------------------------------------------------------------
# Phase 1 — Core CRUD
# ---------------------------------------------------------------------------
echo ""
echo "==> Phase 1 — Core CRUD"

add_issue \
  "chore: base project structure and DB setup" \
  "chore" \
"Set up the foundational pieces required by all resources.

**Tasks:**
- \`src/main.py\`: create FastAPI app, mount routers, serve static files
- \`src/ext/db.py\`: async SQLite engine via \`create_async_engine\`, \`get_session\` dependency yielding \`AsyncSession\`
- \`src/resources/_base/models.py\`: \`BaseTable\` with \`id\` (ULID str), \`created_at\`, \`updated_at\`
- \`src/resources/_base/repository.py\`: generic async helpers — \`get_by_id\`, \`list_all\`, \`add\`, \`delete_by_id\`
- \`src/resources/_base/templates/layout.html\`: shared layout with navigation (Overview, Incomes, Debts)
- Alembic: \`alembic/env.py\` configured for async SQLite; run \`alembic upgrade head\`
- \`pyproject.toml\`: taskipy tasks \`check\` (ruff + ty), \`ruff\`, \`ty\`; Tailwind build task
- \`tests/conftest.py\`: shared \`client\` (TestClient) and async \`session\` fixtures

**Acceptance criteria:**
- \`uv run task check\` passes with no errors
- \`uv run fastapi dev src/main.py\` starts without errors
- \`uv run alembic upgrade head\` runs cleanly"

add_issue \
  "feat: income CRUD" \
  "phase-1" \
"Implement full CRUD for Income entries.

**Model fields:**
- \`id\`: ULID string (from BaseTable)
- \`amount\`: Decimal (required)
- \`source\`: str (required, e.g. 'Salary')
- \`type\`: enum \`Fixed | Variable\` (required)
- \`date\`: date (required, defaults to today)
- \`description\`: str (optional)
- \`created_at\`, \`updated_at\`: from BaseTable

**Implementation order (TDD):**
1. \`tests/test_logic.py\` or \`tests/test_repository.py\` first
2. \`models.py\` (Income, IncomeCreate, IncomeRead)
3. \`repository.py\` (get_by_id, list_by_month, add, update, delete)
4. \`logic.py\` if business rules are needed
5. \`routes.py\` + templates

**Acceptance criteria:**
- Can create an income via form (source, type, amount, date, optional description)
- Income list shows current month entries by default; user can navigate to prev/next month
- Can edit any field of an existing income
- Can delete an income (inline HTMX removal of the row)
- Validation errors shown inline (amount required and positive, date valid, source and type required)"

add_issue \
  "feat: debt CRUD and paid/unpaid toggle" \
  "phase-1" \
"Implement full CRUD for Debt entries with inline paid/unpaid toggle.

**Model fields:**
- \`id\`: ULID string (from BaseTable)
- \`amount\`: Decimal (required)
- \`date\`: date (required, defaults to today)
- \`payment_method\`: enum \`Pix | Credit | Debit | Cash\` (required, hardcoded — no user management)
- \`is_recurrent\`: bool (default False)
- \`due_date\`: date (optional — if in future and paid=False the debt is 'upcoming')
- \`paid\`: bool (default False)
- \`description\`: str (optional)
- \`created_at\`, \`updated_at\`: from BaseTable

**Implementation order (TDD):**
1. Tests first (logic: upcoming rule, balance counting)
2. \`models.py\`, \`repository.py\` (list_by_month, list_recurrent, list_upcoming, toggle_paid)
3. \`routes.py\` + templates

**Acceptance criteria:**
- Can create a debt via form with all fields
- Debt list shows current month entries by default; navigable by month
- Can mark a debt paid or unpaid from the list row (HTMX inline update, no full-page reload)
- Can edit and delete a debt
- Validation errors shown inline
- \`due_date\` only accepted if it is a valid date; no constraint on future/past at creation time"

# ---------------------------------------------------------------------------
# Phase 2 — Overview dashboard
# ---------------------------------------------------------------------------
echo ""
echo "==> Phase 2 — Overview dashboard"

add_issue \
  "feat: overview dashboard" \
  "phase-2" \
"Build the read-only Overview page that gives a monthly financial picture.

**Route:** \`GET /\` (home) — full page, then HTMX fragments for month navigation.

**Sections:**
1. **Month selector** — defaults to current calendar month; prev/next navigation swaps the content area via HTMX
2. **Balance card** — for the selected month: total income, total debts (paid + unpaid both count), net = income − debts
3. **Combined list** — all incomes and debts for the selected month, sorted by date descending, visually distinguished (income vs debt)
4. **Recurrent debts** — all debts with \`is_recurrent=True\`, not month-filtered, sorted by amount descending
5. **Upcoming debts** — debts where \`due_date\` is in the future and \`paid=False\`, sorted by due_date ascending

**Implementation notes:**
- No new DB tables; pull data from the incomes and debts repositories
- Balance logic lives in \`src/resources/overview/logic.py\`
- Route is thin: call logic, return data, let htmy component render

**Acceptance criteria:**
- Month selector visible; switching month updates balance card and combined list without full reload
- Balance card shows three values: income total, debt total, net (signed)
- Combined list clearly distinguishes incomes from debts (label, color, or icon)
- Recurrent debts section always visible regardless of selected month
- Upcoming section shows only future + unpaid debts; disappears if none exist
- All amounts formatted consistently (currency, 2 decimal places)"

# ---------------------------------------------------------------------------
# Phase 3 — Categories
# ---------------------------------------------------------------------------
echo ""
echo "==> Phase 3 — User-managed Categories"

add_issue \
  "feat: income categories CRUD" \
  "phase-3" \
"Add user-managed income categories and wire them into the Income model.

**New model — IncomeCategory:**
- \`id\`: ULID string (from BaseTable)
- \`name\`: str (required, unique)
- \`created_at\`, \`updated_at\`: from BaseTable

**Changes to Income:**
- Add \`category_id\`: str | None (nullable FK to IncomeCategory)

**Acceptance criteria:**
- Can create, rename, and delete income categories from a management page
- Deleting a category sets \`category_id=NULL\` on all affected incomes (no cascade delete of incomes)
- Income create/edit form shows an optional category picker (dropdown of existing categories)
- Category name shown on income list rows (empty/dash if none assigned)
- Navigation includes a link to Categories (or a combined Categories page)"

add_issue \
  "feat: debt categories CRUD" \
  "phase-3" \
"Add user-managed debt categories and wire them into the Debt model.

**New model — DebtCategory:**
- \`id\`: ULID string (from BaseTable)
- \`name\`: str (required, unique)
- \`created_at\`, \`updated_at\`: from BaseTable

**Changes to Debt:**
- Add \`category_id\`: str | None (nullable FK to DebtCategory)

**Acceptance criteria:**
- Can create, rename, and delete debt categories from a management page
- Deleting a category sets \`category_id=NULL\` on all affected debts (no cascade delete of debts)
- Debt create/edit form shows an optional category picker (dropdown of existing categories)
- Category name shown on debt list rows (empty/dash if none assigned)
- IncomeCategory and DebtCategory are separate tables and separate management pages"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "==> All done!"
echo ""
echo "Project : $PROJECT_URL"
echo "Issues  : $(gh issue list --repo "$REPO" --json number,title --jq '.[] | "#\(.number) \(.title)"')"
