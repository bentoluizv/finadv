# FinAdv — Product Roadmap

**Project:** FinAdv — Personal Financial Advisor
**Team:** Solo developer
**Cadence:** 2-week sprints · ~8 productive dev days per sprint
**Start:** 21 Feb 2026
**Estimated completion:** Oct 2026

---

## Roadmap Summary

| Phase | Name | Sprint(s) | Dev Days | Target |
|-------|------|-----------|----------|--------|
| 1 | Core CRUD — Incomes & Debts | 1 | 8 | Mar 6, 2026 |
| 2 | Overview Dashboard | 2 | 6 | Mar 20, 2026 |
| 3 | User-managed Categories | 3 | 8 | Apr 3, 2026 |
| 4 | Bank CSV Import | 4–5 | 14 | May 1, 2026 |
| 5 | Charts & Trends | 6 | 6 | May 15, 2026 |
| 6 | Budget Goals & Savings | 7 | 8 | May 29, 2026 |
| 7 | Auth / Login | 8 | 8 | Jun 12, 2026 |
| 8 | Notifications & Alerts | 9 | 8 | Jun 26, 2026 |
| 9 | Multi-user | 10–11 | 10 | Jul 24, 2026 |
| 10 | Households & Shared Expenses | 12–13 | 14 | Aug 21, 2026 |
| 11 | Open Banking | 14–15 | 12 | Sep 18, 2026 |
| 12 | Ad-hoc Expense Splitting | 16–17 | 10 | Oct 16, 2026 |

**Total estimated effort:** ~112 dev days across 17 sprints (~8 months).

Dates are targets, not commitments. Sprint boundaries may shift; re-estimate at the start of each phase.

---

## Phase 1 — Core CRUD: Incomes & Debts

**Milestone:** Sprint 1 · **Target:** Mar 6, 2026 · **Effort:** 8 dev days
**Dependencies:** None — this is the foundation.

### Goal

Give the user a fast, reliable way to manually record every income and every debt. Lists are filtered by calendar month so the user always starts in the current period without extra navigation.

### Use Cases

#### UC-1.1 — Add an income

As a user, I want to add an income entry so that I can track money I received.

**Fields:** source (required, free text), type (required: Fixed | Variable), amount (required, positive decimal), date (required, defaults to today), description (optional free text).

**Acceptance criteria:**
- Form is accessible from the Incomes list page.
- Source, type, amount, and date are required; form shows a clear inline error for each missing or invalid field without a full-page reload.
- Amount must be a positive number; negative or zero values are rejected.
- On success, the new income appears in the list for its month without a full-page reload.

#### UC-1.2 — Edit an income

As a user, I want to edit an existing income entry so that I can correct mistakes.

**Acceptance criteria:**
- Edit form is pre-filled with the current values.
- Same validation rules as create.
- On save, the list row updates in place (HTMX swap).

#### UC-1.3 — Delete an income

As a user, I want to delete an income entry so that I can remove records added in error.

**Acceptance criteria:**
- Delete requires a confirmation step (inline confirmation, not a modal dialog).
- On confirm, the row is removed from the list without a full-page reload.

#### UC-1.4 — Add a debt

As a user, I want to add a debt entry so that I can track money I spent or owe.

**Fields:** amount (required, positive decimal), payment method (required: Pix | Credit | Debit | Cash), date (required, defaults to today), is_recurrent (bool, default false), due_date (optional), description (optional free text).

**Acceptance criteria:**
- Same validation rules as income: required fields checked inline.
- `due_date`, if provided, must be a valid date (can be in the past or future).
- `is_recurrent` defaults to unchecked; user can toggle it.
- On success, new debt appears in the list for its month.

#### UC-1.5 — Edit a debt

As a user, I want to edit a debt so that I can correct any field including recurrence and due date.

**Acceptance criteria:**
- Same as UC-1.2 for income.

#### UC-1.6 — Delete a debt

As a user, I want to delete a debt so that I can remove entries added in error.

**Acceptance criteria:**
- Same as UC-1.3 for income.

#### UC-1.7 — Mark a debt as paid / unpaid

As a user, I want to toggle a debt's paid status from the list so that I can track which obligations are settled without leaving the page.

**Acceptance criteria:**
- Toggle button or checkbox is visible on every debt row.
- Toggling updates the row instantly (HTMX swap); no full-page reload.
- Paid debts are visually distinguished (e.g. muted or strikethrough) but remain in the list.
- Paid and unpaid debts are both counted in the monthly balance.

#### UC-1.8 — Filter lists by month

As a user, I want to see only the incomes and debts for the selected calendar month so that I can review one period at a time without noise from other months.

**Acceptance criteria:**
- Lists default to the current calendar month on page load.
- Previous/next month navigation is always visible.
- Switching months updates the list without a full-page reload.
- The selected month is clearly labelled (e.g. "March 2026").

#### UC-1.9 — Navigate between sections

As a user, I want persistent navigation links so that I can move between Overview, Incomes, and Debts from any screen.

**Acceptance criteria:**
- Navigation is present in the shared layout on every page.
- Active section is highlighted.

### Functional Requirements

- CRUD for Income: create, list (month-filtered), edit, delete.
- CRUD for Debt: create, list (month-filtered), edit, delete, mark paid/unpaid.
- Month navigation: previous / next controls; defaults to current month.
- Inline validation on all forms; no full-page error reloads.
- HTMX partial updates for create, edit, delete, and paid toggle.

### Non-functional Requirements

- **Performance:** List pages load in under 500 ms for up to 200 records per month.
- **Accessibility:** All form fields have visible labels; error messages are associated with their field; tab order is logical.
- **Responsiveness:** Usable on screens from 375 px wide (mobile) upward.
- **Simplicity:** No pagination needed at this scale; all records for the month on one page.
- **Reliability:** No data loss on validation failure; form state is preserved on error.

---

## Phase 2 — Overview Dashboard

**Milestone:** Sprint 2 · **Target:** Mar 20, 2026 · **Effort:** 6 dev days
**Dependencies:** Phase 1.

### Goal

Give the user a single screen that answers "how am I doing this month?" without having to mentally add up the income and debt lists.

### Use Cases

#### UC-2.1 — View monthly balance

As a user, I want to see my total income, total debts, and net balance for the selected month so that I know immediately if I am in the positive or negative.

**Acceptance criteria:**
- Balance card shows: Total Income, Total Debts, Net (income minus debts).
- Both paid and unpaid debts count toward total debts.
- Net is displayed with a clear visual indicator (positive = green, negative = red).
- Defaults to current month; month selector allows navigation.

#### UC-2.2 — View combined transaction list

As a user, I want to see all incomes and debts for the selected month in one chronological list so that I can review the flow of money for that period.

**Acceptance criteria:**
- Incomes and debts are sorted by date descending.
- Each row clearly indicates whether it is an income or a debt (colour, icon, or label).
- Clicking or tapping a row navigates to the edit form for that record.

#### UC-2.3 — View recurrent debts

As a user, I want a dedicated section showing all recurrent debts regardless of the selected month so that I always know my fixed monthly obligations.

**Acceptance criteria:**
- Shows all debts where `is_recurrent = true`.
- Not filtered by selected month — always shows the full list.
- Each row shows amount, description, and payment method.

#### UC-2.4 — View upcoming debts

As a user, I want to see debts with a future due date that are not yet paid so that I can plan ahead and avoid missed payments.

**Acceptance criteria:**
- Shows debts where `due_date > today` and `paid = false`.
- Sorted by `due_date` ascending (most urgent first).
- Each row shows amount, description, and due date.

### Functional Requirements

- Month selector on the overview page; defaults to current month.
- Balance card: total income, total debts, net — recalculated on month change without full reload.
- Combined list: all incomes + debts for selected month, sorted by date descending.
- Recurrent section: all `is_recurrent=true` debts, not month-filtered.
- Upcoming section: `due_date > today` and `paid=false`, sorted by due_date ascending.

### Non-functional Requirements

- **Performance:** All four sections load in a single request; no sequential waterfall.
- **Clarity:** Visual distinction between income rows and debt rows must be unambiguous without relying on colour alone (use labels or icons too).
- **Responsiveness:** Balance card and sections stack cleanly on mobile.

---

## Phase 3 — User-managed Categories

**Milestone:** Sprint 3 · **Target:** Apr 3, 2026 · **Effort:** 8 dev days
**Dependencies:** Phase 1.

### Goal

Let the user label their records so they can see patterns ("most of my debts are Food and Rent") and prepare for budgeting in Phase 6.

### Use Cases

#### UC-3.1 — Manage income categories

As a user, I want to create, rename, and delete income categories so that I can define the labels relevant to my income sources.

**Acceptance criteria:**
- CRUD for IncomeCategory: name (required, unique).
- Deleting a category sets `category_id = NULL` on all affected incomes; incomes are never deleted.
- Category list page is accessible from navigation.

#### UC-3.2 — Manage debt categories

As a user, I want to create, rename, and delete debt categories separately from income categories so that each domain has its own label set.

**Acceptance criteria:**
- Same rules as UC-3.1 but for DebtCategory and Debt records.
- IncomeCategory and DebtCategory are independent; deleting one does not affect the other.

#### UC-3.3 — Assign a category to an income

As a user, I want to optionally pick an income category when creating or editing an income so that I can keep my records organized.

**Acceptance criteria:**
- Category picker shown on income create and edit forms.
- Selection is optional; leaving it blank is valid.
- Selected category name is shown on the income list row and in the overview combined list.

#### UC-3.4 — Assign a category to a debt

As a user, I want to optionally pick a debt category when creating or editing a debt.

**Acceptance criteria:**
- Same as UC-3.3 but for debt categories and debt forms.

### Functional Requirements

- CRUD for IncomeCategory and DebtCategory (separate resources).
- Nullable `category_id` FK on Income and Debt.
- Deleting a category nullifies the FK on all affected records (no cascade delete of records).
- Category name visible on list rows and overview combined list.
- Optional category picker on all Income and Debt create/edit forms.
- Navigation updated: Categories management link added.

### Non-functional Requirements

- **Data integrity:** Deleting a category must never delete financial records; only the FK is nullified.
- **UX:** Category picker should be a dropdown or searchable select, not a free-text field.
- **Simplicity:** No colour coding or icons per category in this phase (Phase 5 charts can add that).

---

## Phase 4 — Bank CSV Import

**Milestone:** Sprints 4–5 · **Target:** May 1, 2026 · **Effort:** 14 dev days
**Dependencies:** Phase 1 (records exist to diff against).

### Goal

Eliminate manual data entry by letting the user upload a CSV from their bank. The app parses it, compares it against existing records for that month, and asks for approval before writing anything.

### Use Cases

#### UC-4.1 — Upload a bank CSV

As a user, I want to upload a CSV file from my bank app so that the app can read my transactions for a selected month.

**Acceptance criteria:**
- Upload form accepts a CSV file and a month/year selection.
- App auto-detects the bank format from the CSV headers; if unrecognised, a clear error is shown and nothing is processed.
- Supported formats at launch: Nubank, Inter, Itaú.

#### UC-4.2 — Review the import diff

As a user, I want to see exactly what will be created, updated, or skipped before anything is written so that I stay in control of my data.

**Diff states:**

| State | Meaning | Default |
|-------|---------|---------|
| New | Transaction not in the app | Include (pre-checked) |
| Matched | Transaction already exists, identical | Skip (greyed out) |
| Changed | Transaction exists but differs | Include (pre-checked, shows old vs new) |
| Manual-only | Record in app, not in CSV | Keep, flagged informational |

**Acceptance criteria:**
- Matched rows are collapsed by default; user can expand to verify.
- "Approve all new" button pre-checks all New rows.
- Changed rows show the old value and the new value side by side.
- Manual-only rows are clearly labelled "manually added — not in CSV".

#### UC-4.3 — Approve and apply the import

As a user, I want to confirm the approved rows so that the app writes only what I have reviewed.

**Acceptance criteria:**
- Only checked rows are written on submission.
- New rows create Income (credit) or Debt (debit) records.
- Changed rows update the matched record.
- Matched and manual-only rows are untouched.
- A summary is shown after import: X created, Y updated, Z skipped.

#### UC-4.4 — Re-import the same file

As a user, I want to upload the same CSV file a second time without getting duplicates so that I can safely re-import if I am not sure the first attempt worked.

**Acceptance criteria:**
- All rows from the first import appear as Matched.
- Zero records are created or updated on a clean re-import.

### Functional Requirements

- File upload endpoint accepting CSV.
- Bank auto-detection by CSV column headers.
- Parser per bank (Nubank, Inter, Itaú) — each is a pure function producing a list of normalised Movements.
- Movement: `bank_ref` (sha256 of date + amount + description), `date`, `amount`, `direction` (Credit | Debit), `description`, `bank`.
- Diff logic: compare Movements against existing Incomes + Debts for the selected month using `bank_ref` as deduplication key.
- Approval panel as HTMX fragment; no write until user submits.
- Bulk create/update on approval submission.
- Import accessible from navigation.

### Non-functional Requirements

- **Correctness:** Parser must correctly handle each bank's encoding (Itaú uses Latin-1), date formats, and sign conventions for credits/debits.
- **Safety:** Nothing is written until the user explicitly approves; the diff step is mandatory, not optional.
- **Idempotency:** Re-importing the same file must produce zero changes.
- **Testability:** Each bank parser is a pure function testable in isolation with sample CSV fixtures.
- **UX:** Diff panel must be scannable at a glance; avoid walls of text.

---

## Phase 5 — Charts & Trends

**Milestone:** Sprint 6 · **Target:** May 15, 2026 · **Effort:** 6 dev days
**Dependencies:** Phase 1, Phase 3 (category breakdown requires categories).

### Goal

Turn accumulated data into visual summaries. After several months of data — especially with CSV import feeding it — charts answer questions the raw numbers cannot: "am I spending more than last month?", "where does most of my money go?"

### Use Cases

#### UC-5.1 — View monthly balance trend

As a user, I want to see a chart of my net balance per month for the last 12 months so that I can understand if my financial position is improving or worsening over time.

**Acceptance criteria:**
- Bar or line chart showing net balance (income minus debts) per month.
- Current month highlighted.
- Negative months visually distinct (e.g. different colour or direction).

#### UC-5.2 — View income vs debts trend

As a user, I want to see income and total debts side by side per month so that I can identify months where spending outpaced earnings.

**Acceptance criteria:**
- Grouped bar or line chart with two series: Income and Debts.
- Covers the last 12 months.
- Clear legend.

#### UC-5.3 — View spending by category

As a user, I want to see a breakdown of my debt spending by category for the selected month so that I know where most of my money goes.

**Acceptance criteria:**
- Donut or horizontal bar chart.
- Debts without a category grouped under "Uncategorised".
- Selecting a different month updates the chart without a full-page reload.

### Functional Requirements

- Charts rendered server-side (SVG) or via a lightweight CDN chart library (no build step added).
- No new database tables.
- Charts integrated into or linked from the Overview page.
- Month selector controls the category breakdown chart.

### Non-functional Requirements

- **No SPA framework:** Charts must not require React, Vue, or any bundled JS framework.
- **Accessibility:** Charts must include a text alternative (e.g. a data table below the chart) for screen readers.
- **Performance:** Chart data computed server-side; client receives ready-to-render data.

---

## Phase 6 — Budget Goals & Savings

**Milestone:** Sprint 7 · **Target:** May 29, 2026 · **Effort:** 8 dev days
**Dependencies:** Phase 3 (budget goals are per category), Phase 5 (progress shown alongside charts).

### Goal

Move from passive observation to active guidance. The user sets targets and the app tracks whether they are on track.

### Use Cases

#### UC-6.1 — Set a monthly spending limit per category

As a user, I want to define a maximum monthly spend for a debt category so that I have a budget to aim for.

**Acceptance criteria:**
- Budget goal: category (required), monthly limit amount (required, positive).
- One goal per category.
- Accessible from the Categories management page.

#### UC-6.2 — Track spending vs budget

As a user, I want to see how much I have spent vs my budget limit for each category in the current month so that I can adjust behaviour before the month ends.

**Acceptance criteria:**
- Progress indicator (bar or percentage) shown per category where a budget goal exists.
- Shown on the Overview and on the category detail page.
- Indicator turns visually urgent when spend reaches 80% of the limit; critical at 100%.

#### UC-6.3 — Set a monthly savings target

As a user, I want to set a monthly savings goal so that the app can show me whether I am building reserves.

**Acceptance criteria:**
- Savings goal: monthly target amount (required, positive).
- One savings goal total (not per category).

#### UC-6.4 — Track savings progress

As a user, I want to see my actual savings (net balance, if positive) vs my savings target for the current month so that I know if I am on track.

**Acceptance criteria:**
- Savings progress shown on the Overview alongside the balance card.
- If net balance is negative, actual savings is shown as zero (not negative savings).

### Functional Requirements

- `BudgetGoal` table: `category_id` (FK to DebtCategory, nullable if category deleted), `monthly_limit`.
- `SavingsGoal` table: `monthly_target`.
- CRUD for budget goals (per category); CRUD for savings goal (one record).
- Spending vs budget computed at request time from existing Debt records.
- Savings progress computed from monthly net balance.

### Non-functional Requirements

- **Data integrity:** Deleting a category must not delete its budget goal; goal becomes unlinked (category shown as "Deleted category").
- **Clarity:** Progress indicators must be immediately understandable without a legend or explanation.

---

## Phase 7 — Auth / Login

**Milestone:** Sprint 8 · **Target:** Jun 12, 2026 · **Effort:** 8 dev days
**Dependencies:** Phases 1–6 complete (auth gates all existing routes).

### Goal

Protect the app so data is only accessible by the owner. Enable access from any device. Required before Phases 8–11.

### Use Cases

#### UC-7.1 — Log in

As the app owner, I want to log in with email and password so that my financial data is not accessible to anyone who opens the URL.

**Acceptance criteria:**
- Login page is the first screen for unauthenticated users.
- Invalid credentials show a clear error; no hint as to which field was wrong.
- Successful login redirects to the Overview.
- Session cookie is secure, HTTP-only, and persists across browser restarts.

#### UC-7.2 — Log out

As a user, I want to log out so that my session is cleared on shared or public devices.

**Acceptance criteria:**
- Logout link in the navigation.
- Logout invalidates the session immediately and redirects to login.

#### UC-7.3 — Access the app from a second device

As a user, I want to log in from my phone or another computer so that I am not tied to a single machine.

**Acceptance criteria:**
- Same credentials work on any device.
- Sessions are independent; logging out on one device does not affect the other.

### Functional Requirements

- Login page: email + password form.
- No open registration — single user; credentials configured via environment variables or a one-time setup command (e.g. `uv run task create-user`).
- All existing routes redirect to `/login` if no valid session.
- Session management: secure cookie with configurable expiry.
- Logout endpoint clears the session.

### Non-functional Requirements

- **Security:** Passwords stored as bcrypt hashes; never in plain text. Session cookies are HTTP-only and Secure.
- **No lockout risk:** If credentials are forgotten, they can be reset via environment variable or CLI command — no admin UI needed in this phase.
- **Simplicity:** No OAuth, no magic links, no 2FA in this phase.

---

## Phase 8 — Notifications & Alerts

**Milestone:** Sprint 9 · **Target:** Jun 26, 2026 · **Effort:** 8 dev days
**Dependencies:** Phase 7 (auth; user has an email address). Phase 6 (budget goals exist to alert on).

### Goal

Proactively inform the user before problems occur — a debt due tomorrow they forgot about, or a category budget about to be exceeded.

### Use Cases

#### UC-8.1 — Configure upcoming debt reminders

As a user, I want to set how many days before a debt's due date I should receive a reminder so that I can pay on time.

**Acceptance criteria:**
- Setting: number of days before `due_date` to notify (e.g. 3 days).
- Applies to all debts with a `due_date` that are not yet paid.
- Can be disabled.

#### UC-8.2 — Receive an upcoming debt reminder

As a user, I want to receive an email reminder when a debt's due date is approaching so that I do not miss payments.

**Acceptance criteria:**
- Email sent on the configured day(s) before `due_date`.
- Email shows: debt description, amount, due date.
- Not sent if the debt is already marked paid.
- Not sent again if already sent for the same debt and trigger day.

#### UC-8.3 — Configure budget-limit alerts

As a user, I want to be notified when my spending in a category reaches a set percentage of my budget limit so that I can adjust before I overspend.

**Acceptance criteria:**
- Setting: percentage threshold (e.g. notify at 80% and at 100%).
- Applies to all categories that have a budget goal.
- Can be disabled per threshold.

#### UC-8.4 — Receive a budget-limit alert

As a user, I want to receive an email alert when I hit a budget threshold so that I am aware and can act.

**Acceptance criteria:**
- Email sent when the threshold is crossed for the current month.
- Email shows: category, amount spent, budget limit, percentage used.
- Not sent again for the same category, threshold, and month if already sent.

#### UC-8.5 — View delivery log

As a user, I want to see a log of sent alerts so that I can verify what was sent and when.

**Acceptance criteria:**
- Delivery log page shows: date sent, alert type, summary message.
- Accessible from settings or a dedicated Alerts section.

### Functional Requirements

- `AlertRule` table: type (UpcomingDebt | BudgetLimit), configuration (days or percentage), enabled flag.
- `AlertDelivery` table: rule_id, sent_at, reference (debt_id or category_id + month).
- Background task or scheduled job checks for triggers and sends emails.
- SMTP configuration via environment variables (host, port, user, password, from address).
- Idempotency: deduplication on (rule, reference, period) — same alert not sent twice.

### Non-functional Requirements

- **Reliability:** Failed email delivery is logged; no silent failures.
- **Privacy:** Email content contains only the user's own data.
- **Simplicity:** No push notifications, no SMS in this phase — email only.

---

## Phase 9 — Multi-user

**Milestone:** Sprints 10–11 · **Target:** Jul 24, 2026 · **Effort:** 10 dev days
**Dependencies:** Phase 7 (auth foundation). Required before Phase 10.

### Goal

Open the installation to multiple independent users. Each person's data is fully private. This is the technical prerequisite for household sharing.

### Use Cases

#### UC-9.1 — Register a new account

As a new person, I want to create my own account so that I can use the app independently from other users on the same installation.

**Acceptance criteria:**
- Registration page: email + password (with confirmation).
- Email must be unique across accounts.
- Password minimum length enforced.
- On success, user is logged in and redirected to Overview.
- Registration can be disabled via config (invite-only or admin-controlled mode).

#### UC-9.2 — Access only my own data

As a user, I want to be certain that I can never see or modify another user's records so that my financial data is private.

**Acceptance criteria:**
- All data reads filter by `user_id` from the session.
- Accessing another user's record by URL (e.g. `/incomes/other-user-id`) returns 404.
- No UI exposes other users' data.

### Functional Requirements

- `User` table: email, hashed_password, created_at.
- `user_id` FK added to: Income, Debt, IncomeCategory, DebtCategory, BudgetGoal, SavingsGoal, AlertRule, AlertDelivery, BankImport (all via Alembic migration).
- All repository queries scoped by `user_id`.
- Existing single-user data migrated to the first registered account via a migration script.
- Registration endpoint (can be disabled via `ALLOW_REGISTRATION=false` env var).

### Non-functional Requirements

- **Data isolation:** No query may return records belonging to a different user; enforced at the repository layer, not only the route layer.
- **Migration safety:** Existing data must survive the `user_id` migration; data loss is unacceptable.
- **Performance:** Adding `user_id` filter does not degrade query speed; index on `user_id` per table.

---

## Phase 10 — Households & Shared Expenses

**Milestone:** Sprints 12–13 · **Target:** Aug 21, 2026 · **Effort:** 14 dev days
**Dependencies:** Phase 9 (multi-user — requires multiple accounts and data isolation).

### Goal

Separate personal finances from shared ones. Three flatmates sharing rent, utilities, and groceries can record those expenses once and have each person's share appear in their own personal balance automatically.

### Use Cases

#### UC-10.1 — Create a household

As a user, I want to create a named household so that I have a shared space to record common expenses.

**Acceptance criteria:**
- Household name is required.
- The creator becomes the first member automatically.
- A user can create multiple households.

#### UC-10.2 — Invite a member to a household

As a household member, I want to invite another registered user so that they can see and add household expenses.

**Acceptance criteria:**
- Invitation is sent by entering the invitee's email.
- Invitee receives a notification (in-app or email) and must accept.
- Accepted invitation adds the user to the household.
- Declining leaves the invitee unaffected.

#### UC-10.3 — Add a shared expense

As a household member, I want to add a shared expense and assign a custom amount to each member so that the split reflects our actual agreement.

**Fields:** description (required), date (required, defaults to today), payment method (required), total amount (required), per-member split (custom amount for each member).

**Acceptance criteria:**
- The sum of all per-member amounts must equal the total expense amount; validated before saving.
- Any household member can add an expense.
- On save, each member's share is recorded and flows into their personal monthly balance as a debt-equivalent for that month.

#### UC-10.4 — View household expenses

As a household member, I want to see all shared expenses for the household so that I know the full picture of what the group owes.

**Acceptance criteria:**
- Household view lists all expenses: description, total amount, date, per-member breakdown.
- Payment status per member is visible (paid / unpaid).
- Month filter available.

#### UC-10.5 — Mark my share as paid

As a household member, I want to mark my own share of an expense as paid so that my household mates can see I have settled it.

**Acceptance criteria:**
- Can only mark own share; cannot change another member's status.
- Paid status visible to all members in the household view.

#### UC-10.6 — See household shares in personal balance

As a user, I want my share of household expenses to appear in my personal overview and balance so that my financial picture is complete.

**Acceptance criteria:**
- ExpenseShares for the selected month are included in the user's total debts for that month.
- Shown as a distinct type (e.g. labelled "Household: [household name]") in the combined list.
- Removing a household expense removes the share from the member's balance.

#### UC-10.7 — Leave a household

As a user, I want to leave a household so that future expenses no longer affect my account.

**Acceptance criteria:**
- Leaving does not delete past expense shares; historical data is preserved.
- User no longer receives new expenses from that household after leaving.

### Functional Requirements

- New tables: `Household`, `HouseholdMember`, `HouseholdExpense`, `ExpenseShare`.
- Invite flow: in-app notification or email; accept/decline action.
- Validation: sum of shares must equal total expense amount.
- ExpenseShares included in personal balance computation and combined list for the Overview.
- Household navigation link added to layout (visible only to users with at least one household).

### Non-functional Requirements

- **Data integrity:** Deleting a household expense must atomically remove all its shares; no orphaned shares.
- **Privacy:** A user's personal incomes and debts are never visible to household members; only shared expenses are shared.
- **Validation:** Share-sum validation must run server-side; client-side validation is additive, not the sole check.
- **UX:** The split form should make it easy to distribute the total amount across members (e.g. equal-split shortcut, even though custom amounts are stored).

---

## Phase 11 — Open Banking

**Milestone:** Sprints 14–15 · **Target:** Sep 18, 2026 · **Effort:** 12 dev days
**Dependencies:** Phase 7 (auth, for per-user OAuth tokens). Phase 4 (diff-and-approval panel reused).

### Goal

The final step: full automation. Transactions sync directly from the user's bank via Brazil's Open Finance APIs. No CSV downloads, no manual entry. The diff-and-approval panel from Phase 4 is reused so the user remains in control.

### Use Cases

#### UC-11.1 — Connect a bank account

As a user, I want to connect one of my bank accounts via Open Finance so that my transactions can be fetched automatically.

**Acceptance criteria:**
- User initiates the connection from a Bank Connections page.
- OAuth flow redirects to the bank's authorisation page and back.
- On success, the connection is saved (bank name, account reference, token expiry).
- Multiple bank accounts can be connected.

#### UC-11.2 — Sync transactions on demand

As a user, I want to trigger a sync manually so that I can fetch the latest transactions when I want.

**Acceptance criteria:**
- "Sync now" button on the Bank Connections page.
- Fetched transactions go through the Phase 4 diff-and-approval panel.
- User approves before anything is written.

#### UC-11.3 — Automatic scheduled sync

As a user, I want my transactions to sync automatically on a schedule so that my data is kept up to date without manual effort.

**Acceptance criteria:**
- Configurable sync frequency (e.g. daily).
- Synced transactions are queued for review in a pending-approvals inbox.
- User is notified (in-app or email) when new transactions are pending review.

#### UC-11.4 — Disconnect a bank account

As a user, I want to disconnect a bank account so that no further syncs are performed.

**Acceptance criteria:**
- Disconnecting revokes the stored token.
- Existing imported records are kept; no data is deleted.

### Functional Requirements

- `BankConnection` table: `user_id`, `bank` (enum), `account_ref`, `access_token` (encrypted), `refresh_token` (encrypted), `token_expiry`, `sync_schedule`, `last_synced_at`.
- OAuth flow per bank (Nubank, Inter, Itaú) via Brazil's Open Finance standard.
- Token refresh handled automatically before expiry.
- Fetched transactions normalised into the same Movement format as Phase 4.
- Diff-and-approval panel reused from Phase 4 (same logic, different data source).
- Background scheduler for automatic syncs.
- Pending-approvals inbox for auto-synced transactions.

### Non-functional Requirements

- **Security:** OAuth tokens stored encrypted at rest; never logged or exposed in responses.
- **Reliability:** Failed syncs are logged; user is notified of persistent failures.
- **Resilience:** Token expiry and refresh are handled transparently; user is not logged out of Open Banking on token refresh.
- **Compliance:** Open Finance data handling must comply with Brazilian data regulations (LGPD).
- **Graceful degradation:** If a bank's API is unavailable, the connection remains; the user is informed and can retry.

---

## Phase 12 — Ad-hoc Expense Splitting

**Milestone:** Sprints 16–17 · **Target:** Oct 16, 2026 · **Effort:** 10 dev days
**Dependencies:** Phase 9 (multi-user — required to identify registered participants). Phase 10 (households, for context; not strictly required but splitting is a natural extension of shared-expenses thinking).

### Goal

Allow any single expense to be split with any set of people — registered users or not — without requiring a permanent household group. You pay for dinner for four, record it once, and track who owes what. Simple paid/unpaid settlement per person; no money moves through the app.

### How it differs from Phase 10

| | Phase 10 — Households | Phase 12 — Ad-hoc Splitting |
|-|----------------------|----------------------------|
| Group | Fixed household (persistent members) | Any people, defined per expense |
| Frequency | Recurring obligations (rent, utilities) | One-off events (dinner, taxi, trip) |
| Participants | Must be registered users | Registered users OR named non-users |
| Settlement | Per-share paid toggle | Per-share paid toggle |

### Use Cases

#### UC-12.1 — Split an expense with others

As a user, I want to mark any debt as a split expense and assign a share to each participant so that I can track who owes what after a shared event.

**Fields:** participants (one or more — registered users by email, or named non-users by name + optional email), per-participant amount (custom), description of the split (optional, defaults to the expense description).

**Acceptance criteria:**
- Any existing Debt can be converted to a split expense, or a split can be created standalone.
- At least one other participant is required (in addition to the payer).
- Per-participant amounts plus the payer's own share must sum to the total expense amount.
- Validation runs server-side; client-side validation is additive.

#### UC-12.2 — Include non-registered participants

As a user, I want to add someone who does not have a FinAdv account as a participant so that I can track splits with friends outside the app.

**Acceptance criteria:**
- Non-user participants are identified by a name (required) and optional email.
- Their share is tracked locally in the payer's account; they do not have app access.
- If an optional email is provided, a notification email can be sent informing them of the split and their share (optional, controlled by a toggle at split creation time).

#### UC-12.3 — View splits I created (I paid)

As a user, I want to see all expenses I split with others so that I can track who has settled their share.

**Acceptance criteria:**
- Splits list shows: expense description, total amount, date, list of participants and their share/status.
- Filter by status: all / pending / settled.
- A split is fully settled when all participants have marked their share as paid.

#### UC-12.4 — View splits I owe (others paid)

As a registered user, I want to see expenses others split with me so that I know what I owe and can mark my share as paid.

**Acceptance criteria:**
- Incoming splits visible in a dedicated "Owe" section or tab.
- Each shows: who paid, description, total amount, my share, status.
- Can mark own share as paid from this view.

#### UC-12.5 — Mark a share as paid

As a participant (payer or other registered user), I want to mark a share as paid so that the split record reflects settlement.

**Acceptance criteria:**
- Each participant can only change their own share's status.
- The payer can mark any non-user participant's share as paid (since non-users cannot log in).
- Status change is visible to all registered participants in the split immediately.

#### UC-12.6 — Edit or delete a split

As the payer, I want to edit or delete a split expense so that I can correct mistakes.

**Acceptance criteria:**
- Only the payer (creator) can edit or delete the split.
- Editing allows changing amounts and participants; sum-to-total validation re-runs.
- Deleting a split removes it from all participants' views and from the payer's balance.

### Functional Requirements

- `ExpenseSplit` table: `debt_id` (FK to Debt, nullable if standalone split), `created_by_user_id`, `description`, `total_amount`, `date`.
- `SplitParticipant` table: `split_id`, `user_id` (nullable — null for non-users), `name` (for non-users), `email` (optional, for non-users), `amount`, `paid` (bool, default false).
- A Debt can have at most one `ExpenseSplit`.
- Payer's own share is a `SplitParticipant` record with `user_id = payer`.
- Registered participants notified in-app (and optionally by email) when added to a split.
- Optional email notification to non-user participants if email is provided and toggle is on.
- Splits section added to navigation.

### Non-functional Requirements

- **Privacy:** A registered participant sees only their own share and the split total; they cannot see other participants' amounts or statuses.
- **Data integrity:** Deleting the associated Debt must also delete the split and all participant records.
- **Simplicity:** No running balance between users in this phase; no debt netting across multiple splits. That complexity is deferred.
- **Non-user experience:** Non-users receive at most one email per split (on creation); no further app interaction is required from them.

---

## Cross-phase Non-functional Requirements

These apply to all phases and should be verified at every milestone.

- **Code quality:** All Python under `src/` passes `uv run task check` (Ruff lint + Ty type-check) with zero new violations before merge.
- **Test coverage:** Every new business rule and repository function has at least one passing test. No feature ships without a test defining its behaviour.
- **Async-first:** All DB access and I/O is async throughout. No blocking calls in the request path.
- **Migrations:** Every DB model change includes an Alembic migration. Migrations are tested via the `migrated_db_path` fixture.
- **No hardcoded secrets:** All credentials, URLs, and keys come from environment variables via pydantic-settings.
- **Responsive design:** Every new screen is usable on a 375 px wide viewport (mobile minimum).
- **Semantic HTML:** All new UI uses correct HTML elements; forms have associated labels; interactive elements are keyboard-reachable.
