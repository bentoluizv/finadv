# FinAdv — Design System & UX Style Guide

This is the single source of truth for visual design and UX patterns in FinAdv. Every template, component, and htmy function must follow this guide. When in doubt, choose the simpler option.

---

## 1. Brand Identity

| Property | Value |
|----------|-------|
| **Name** | FinAdv |
| **Tagline** | Your personal financial adviser |
| **Logomark** | Two-letter monogram "FA" in a small rounded square |
| **Voice** | Calm, direct, precise — no jargon, no marketing language |
| **Tone** | Informative and neutral; never alarmist, never playful |

**Principle:** Every screen should answer one question clearly. Remove anything that does not serve that question.

---

## 2. Color Palette

Tokens are defined in `src/static/main.css` as Tailwind `@theme` variables. Use the token name in utility classes (e.g. `bg-brand-600`, `text-neutral-900`).

### Brand — Emerald

| Token | Hex | Usage |
|-------|-----|-------|
| `brand-50` | `#ecfdf5` | Light tinted backgrounds (e.g. success callout fill) |
| `brand-100` | `#d1fae5` | Hover state on light backgrounds |
| `brand-600` | `#059669` | Primary action — buttons, active links, focus rings |
| `brand-700` | `#047857` | Button hover state |
| `brand-800` | `#065f46` | Button active/pressed state |

### Neutral — Slate (dark surface)

The app uses a dark surface. Slate values increase from light to dark.

| Token | Hex | Usage |
|-------|-----|-------|
| `neutral-50` | `#f8fafc` | Body text on dark surfaces |
| `neutral-100` | `#f1f5f9` | Secondary body text |
| `neutral-200` | `#e2e8f0` | Muted labels, captions |
| `neutral-500` | `#64748b` | Placeholder text, timestamps, disabled states |
| `neutral-700` | `#334155` | Borders, dividers on dark surfaces |
| `neutral-900` | `#0f172a` | Deep backgrounds (used as `slate-950` in practice) |

> Because Tailwind ships `slate-*` natively, you may use `slate-950` / `slate-900` / `slate-800` for surface layers and `slate-100` / `slate-300` for text. Reserve `neutral-*` tokens for explicit cross-context references in DESIGN.md documentation.

### Status Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `success` | `#16a34a` | Paid badge, positive balance |
| `warning` | `#d97706` | Upcoming / due-soon badge |
| `danger` | `#dc2626` | Delete actions, overdue, negative balance |
| `info` | `#2563eb` | Informational callouts |

**Rule:** Never use color alone to convey meaning. Always pair a status color with a text label or an icon with an `aria-label`.

### WCAG Contrast Pairs

| Foreground | Background | Ratio | Use |
|------------|------------|-------|-----|
| `slate-50` (#f8fafc) | `slate-950` (#020617) | ~19:1 | Body text on main surface |
| `emerald-400` (#34d399) | `slate-950` (#020617) | ~9:1 | Active nav links, accent text |
| `emerald-600` (#059669) | `white` (#ffffff) | ~4.6:1 | Primary button label |
| `white` (#ffffff) | `emerald-600` (#059669) | ~4.6:1 | Primary button text |
| `slate-300` (#cbd5e1) | `slate-900` (#0f172a) | ~7:1 | Inactive nav links |
| `white` (#ffffff) | `danger` (#dc2626) | ~5.1:1 | Danger button text |

All pairs meet WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text and UI components).

---

## 3. Typography

**Font stack:** System font stack — no web fonts loaded. Fast, readable, native.

```
font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
             "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Scale

| Class | Size | Weight | Line-height | Usage |
|-------|------|--------|-------------|-------|
| `text-xs` | 12 px | 400 | 1.5 | Timestamps, footer, helper text |
| `text-sm` | 14 px | 400 | 1.5 | Table cells, nav links, badges |
| `text-base` | 16 px | 400 | 1.5 | Body copy, form labels, inputs |
| `text-lg` | 18 px | 600 | 1.4 | Section headings, card titles |
| `text-xl` | 20 px | 600 | 1.3 | Page headings (`<h1>`) |
| `text-2xl` | 24 px | 700 | 1.2 | Dashboard summary numbers |

**Rules:**
- `<h1>`: one per page, `text-xl font-semibold`.
- `<h2>`: section headers, `text-lg font-semibold`.
- `<h3>`: sub-sections, `text-base font-medium`.
- Never skip heading levels.
- Monetary values in summary cards: `text-2xl font-bold tabular-nums`.

---

## 4. Spacing

Base unit: **4 px** (Tailwind's `1` = 4 px).

| Step | px | Common use |
|------|----|-----------|
| `1` | 4 | Icon gap, tight inline spacing |
| `2` | 8 | Badge padding, compact items |
| `3` | 12 | Button padding (vertical) |
| `4` | 16 | Button padding (horizontal), card padding |
| `6` | 24 | Section gap, form field gap |
| `8` | 32 | Card gap, major section separation |

---

## 5. Layout

| Property | Value | Tailwind |
|----------|-------|---------|
| Max content width | 1024 px | `max-w-5xl` |
| Page padding (x) | 16 px | `px-4` |
| Page padding (y) | 24 px | `py-6` |
| Header height | ~48 px | `py-3` top bar |
| Gap between page sections | 16 px | `gap-4` on `<main>` |

**Breakpoints used:** Mobile-first. Minimum supported viewport: 375 px. Use `sm:` for ≥640 px adjustments.

---

## 6. Component Patterns

### 6.1 Buttons

Every button must have a visible label. Icon-only buttons must have `aria-label`.

#### Primary

```html
<button
  type="submit"
  class="rounded bg-emerald-600 px-4 py-2 text-sm font-medium text-white
         hover:bg-emerald-700 active:bg-emerald-800
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-emerald-400 focus-visible:ring-offset-2
         focus-visible:ring-offset-slate-950
         disabled:opacity-50 disabled:cursor-not-allowed"
>
  Save
</button>
```

#### Secondary (outline)

```html
<button
  type="button"
  class="rounded border border-slate-600 px-4 py-2 text-sm font-medium text-slate-300
         hover:border-slate-400 hover:text-slate-100
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-emerald-400 focus-visible:ring-offset-2
         focus-visible:ring-offset-slate-950"
>
  Cancel
</button>
```

#### Ghost (text only)

```html
<button
  type="button"
  class="rounded px-2 py-1 text-sm text-slate-400
         hover:text-slate-100
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-emerald-400 focus-visible:ring-offset-2
         focus-visible:ring-offset-slate-950"
>
  View
</button>
```

#### Danger

```html
<button
  type="button"
  class="rounded bg-red-600 px-4 py-2 text-sm font-medium text-white
         hover:bg-red-700 active:bg-red-800
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-red-400 focus-visible:ring-offset-2
         focus-visible:ring-offset-slate-950"
>
  Delete
</button>
```

---

### 6.2 Form Inputs

Every input **must** have a `<label>` associated via `for`/`id`. Use `aria-required="true"` for required fields. Use `aria-describedby` to link to an error message element.

```html
<div class="flex flex-col gap-1">
  <label for="amount" class="text-sm font-medium text-slate-200">
    Amount <span aria-hidden="true" class="text-red-400">*</span>
  </label>
  <input
    id="amount"
    name="amount"
    type="number"
    step="0.01"
    min="0.01"
    required
    aria-required="true"
    aria-describedby="amount-error"
    class="rounded border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-100
           placeholder-slate-500
           focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500
           aria-[invalid=true]:border-red-500 aria-[invalid=true]:ring-red-500"
    placeholder="0.00"
  />
  <!-- Shown only when validation fails; hidden with class="hidden" otherwise -->
  <p id="amount-error" role="alert" class="text-xs text-red-400 hidden">
    Amount must be a positive number.
  </p>
</div>
```

**Rules:**
- Required fields: add `required`, `aria-required="true"`, and a visible `*` indicator. Place a legend near the form top: `<p class="text-xs text-slate-500">Fields marked * are required.</p>`.
- Invalid state: add `aria-invalid="true"` to the input when it fails validation; `aria-describedby` already links to the error message element.
- Error messages: use `role="alert"` so screen readers announce them immediately; toggle `hidden` class to show/hide.
- Select elements follow the same label pattern.
- Textarea follows the same label pattern.

#### Select

```html
<div class="flex flex-col gap-1">
  <label for="type" class="text-sm font-medium text-slate-200">Type</label>
  <select
    id="type"
    name="type"
    class="rounded border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-100
           focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
  >
    <option value="fixed">Fixed</option>
    <option value="variable">Variable</option>
  </select>
</div>
```

#### Checkbox

```html
<div class="flex items-center gap-2">
  <input
    id="is_recurrent"
    name="is_recurrent"
    type="checkbox"
    class="h-4 w-4 rounded border-slate-600 bg-slate-800 text-emerald-600
           focus:ring-2 focus:ring-emerald-500 focus:ring-offset-slate-950"
  />
  <label for="is_recurrent" class="text-sm text-slate-200">Recurrent</label>
</div>
```

---

### 6.3 Status Badges

Badges must always include a text label — never use color alone.

```html
<!-- Paid -->
<span class="inline-flex items-center gap-1 rounded-full bg-emerald-950 px-2 py-0.5
             text-xs font-medium text-emerald-400">
  Paid
</span>

<!-- Unpaid -->
<span class="inline-flex items-center gap-1 rounded-full bg-slate-800 px-2 py-0.5
             text-xs font-medium text-slate-400">
  Unpaid
</span>

<!-- Upcoming (due soon, unpaid) -->
<span class="inline-flex items-center gap-1 rounded-full bg-amber-950 px-2 py-0.5
             text-xs font-medium text-amber-400">
  Upcoming
</span>

<!-- Recurrent -->
<span class="inline-flex items-center gap-1 rounded-full bg-blue-950 px-2 py-0.5
             text-xs font-medium text-blue-400">
  Recurrent
</span>
```

---

### 6.4 Table Rows

Use `<table>` with proper `<thead>` / `<tbody>`. Every column must have a `<th scope="col">` header. Row actions (edit, delete) must have `aria-label` that includes the row context.

```html
<table class="w-full text-sm text-left">
  <thead class="border-b border-slate-800 text-xs text-slate-500 uppercase tracking-wide">
    <tr>
      <th scope="col" class="pb-2 pr-4">Date</th>
      <th scope="col" class="pb-2 pr-4">Source</th>
      <th scope="col" class="pb-2 pr-4 text-right">Amount</th>
      <th scope="col" class="pb-2"><span class="sr-only">Actions</span></th>
    </tr>
  </thead>
  <tbody class="divide-y divide-slate-800">
    <tr class="hover:bg-slate-900/50">
      <td class="py-3 pr-4 text-slate-400">Jan 15</td>
      <td class="py-3 pr-4 text-slate-100">Salary</td>
      <td class="py-3 pr-4 text-right font-medium tabular-nums text-slate-100">R$ 5,000.00</td>
      <td class="py-3 text-right">
        <button
          type="button"
          aria-label="Edit Salary income from Jan 15"
          class="text-slate-500 hover:text-slate-100 focus-visible:outline-none
                 focus-visible:ring-2 focus-visible:ring-emerald-400 rounded-sm"
        >Edit</button>
      </td>
    </tr>
  </tbody>
</table>
```

---

### 6.5 Alert / Flash Messages

```html
<!-- Success -->
<div role="alert" class="rounded border border-emerald-800 bg-emerald-950 px-4 py-3
                          text-sm text-emerald-300">
  Income saved successfully.
</div>

<!-- Error -->
<div role="alert" class="rounded border border-red-800 bg-red-950 px-4 py-3
                          text-sm text-red-300">
  Something went wrong. Please try again.
</div>

<!-- Info -->
<div role="status" class="rounded border border-blue-800 bg-blue-950 px-4 py-3
                           text-sm text-blue-300">
  No records for this month yet.
</div>
```

---

## 7. Interaction Rules

- **HTMX partial updates:** Use `hx-target` + `hx-select` to swap only the changed region — never trigger a full-page reload for list mutations (create, delete, update, mark paid).
- **Inline row feedback:** After a successful create or delete, swap the affected `<tbody>` row or the full table; do not reload the page.
- **Form submission:** `hx-post` on the form; on success return the updated partial; on validation failure return the form fragment with `aria-invalid` states and error messages populated.
- **Optimistic UI:** Do not use. Always wait for server confirmation before showing the updated state.
- **HTMX announcements:** After a successful mutation, include a populated `#sr-announcer` fragment in the response (e.g. `<div id="sr-announcer" ...>Debt saved.</div>`) so screen readers announce the outcome. The `aria-live="polite"` and `aria-atomic="true"` attributes on that element ensure it is read aloud.

---

## 8. Accessibility — WCAG 2.1 AA

This section is the implementation reference. All patterns listed here are required on every screen. The WCAG success criteria numbers are noted for traceability.

### 8.1 Landmark Regions (SC 1.3.6, 2.4.1)

Every page must use semantic HTML5 landmark elements:

| Element | Role | Note |
|---------|------|------|
| `<header>` | `banner` | Site header; one per page |
| `<nav>` | `navigation` | Must have `aria-label` when more than one `<nav>` exists |
| `<main>` | `main` | One per page; target of skip link |
| `<footer>` | `contentinfo` | Site footer |

Do not use `role="main"` on `<main>` — the element already carries the implicit role.

### 8.2 Skip Navigation (SC 2.4.1)

The skip link is the **first focusable element** in `<body>`, visually hidden until focused, and links to `id="content"` on `<main>`. Pattern is already in `layout.html`. Every child template inherits it automatically.

### 8.3 Page Title (SC 2.4.2)

Every page must have a unique, descriptive `<title>`. Use the `{% block title %}` in `layout.html`:

```html
{% block title %}Incomes — FinAdv{% endblock %}
```

Format: `{Page Name} — FinAdv`. The overview page may use just `FinAdv`.

### 8.4 Active Navigation (SC 2.4.8)

The active nav link must have `aria-current="page"`. Routes pass an `active_page` string to the template context (values: `"overview"`, `"incomes"`, `"debts"`; extended in later phases). Pattern is in `layout.html`.

```python
# In a route handler (example):
return templates.TemplateResponse('incomes/list.html', {
    'request': request,
    'active_page': 'incomes',
    ...
})
```

### 8.5 Focus Management (SC 2.4.3, 2.4.7)

- All interactive elements (`<a>`, `<button>`, `<input>`, `<select>`, `<textarea>`) must have a visible `focus-visible` ring using:
  ```
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400
  focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950
  ```
- Do not use `outline: none` without a custom focus indicator.
- Tab order must follow reading order. Do not use positive `tabindex` values.
- After an HTMX partial swap that removes the focused element, move focus to the logical next element (e.g. the table or a status message). Use `htmx:afterSwap` or `autofocus` on the first field of a newly swapped-in form.

### 8.6 Form Accessibility (SC 1.3.1, 3.3.1, 3.3.2)

| Requirement | Implementation |
|-------------|----------------|
| Label every input | `<label for="id">` + matching `id` on the control |
| Required fields | `required` + `aria-required="true"` + visible `*` marker |
| Invalid state | `aria-invalid="true"` on the failing input |
| Error message | `role="alert"` element; link with `aria-describedby` on the input |
| Fieldset groups | Wrap related checkboxes/radios in `<fieldset>` with `<legend>` |
| No placeholder-only labels | Always use `<label>`; placeholder is supplementary only |

### 8.7 Icon-only Controls (SC 1.1.1, 4.1.2)

Any button or link whose visible label is only an icon must have an accessible name:

```html
<!-- Option A: aria-label on the button -->
<button type="button" aria-label="Delete Salary income">
  <!-- SVG icon -->
</button>

<!-- Option B: visually hidden text -->
<button type="button">
  <span aria-hidden="true"><!-- SVG --></span>
  <span class="sr-only">Delete Salary income</span>
</button>
```

The `aria-hidden="true"` on decorative SVGs prevents double-reading.

### 8.8 HTMX Live Announcements (SC 4.1.3)

The `#sr-announcer` `<div>` in `layout.html` has `role="status"`, `aria-live="polite"`, `aria-atomic="true"`. After any mutation:

1. Include a replacement `#sr-announcer` fragment in the HTMX response with a brief human-readable message.
2. HTMX's `hx-swap-oob="true"` attribute on the fragment ensures it is updated independently of the main swap target.

Example response fragment:
```html
<div id="sr-announcer" role="status" aria-live="polite" aria-atomic="true"
     class="sr-only" hx-swap-oob="true">
  Debt "Rent" marked as paid.
</div>
```

### 8.9 Color and Contrast (SC 1.4.3, 1.4.11)

- Body text: minimum 4.5:1 contrast against its background.
- Large text (≥18 pt / ≥14 pt bold) and UI components (buttons, inputs, badges): minimum 3:1.
- All contrast pairs in section 2 (Color Palette) are verified against WCAG 2.1 AA.
- Use the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) when adding new color combinations.

### 8.10 Meaningful Sequence and Reflow (SC 1.3.2, 1.4.10)

- DOM order must match visual reading order.
- At 375 px width all content must be accessible without horizontal scrolling.
- Tables that cannot reflow may use `overflow-x-auto` on a wrapper; do not hide columns on mobile.

### 8.11 Language (SC 3.1.1)

The `<html>` element has `lang="en"`. When the UI is localised to Portuguese, change to `lang="pt-BR"`.

---

## 9. Checklist for New Screens

Use this checklist before considering any screen done:

- [ ] `{% block title %}` set with a unique, descriptive page title
- [ ] `active_page` passed to context so the correct nav link has `aria-current="page"`
- [ ] All `<h1>` / `<h2>` / `<h3>` follow heading hierarchy; one `<h1>` per page
- [ ] Every form input has an associated `<label>`
- [ ] Required inputs have `required` + `aria-required="true"`
- [ ] Error messages use `role="alert"` and `aria-describedby`
- [ ] All interactive elements have a `focus-visible` ring
- [ ] Icon-only buttons have `aria-label` or `<span class="sr-only">`
- [ ] `#sr-announcer` fragment included in HTMX mutation responses
- [ ] Color contrast meets 4.5:1 for text, 3:1 for UI components
- [ ] Screen is usable at 375 px viewport width
- [ ] Tab order matches visual reading order
