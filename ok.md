# SMCP — Social Media Content Planner
## Upgrade Plan: Branding + New Statuses + New Features

---

# 1. BRANDING

## App Name
- **Full**: Social Media Content Planner
- **Short**: SMCP
- **Usage**: Navbar shows "SMCP" with full name on hover/tooltip

## Navbar Branding
- Logo: Styled "SMCP" text badge with primary color (#4F46E5) background, white text, rounded
- Tagline below logo (desktop only): "Plan. Create. Post." in muted text, 11px
- Navbar links: Dashboard | Add Content | Content List | Calendar | Analytics

## Homepage Hero Section
- Large heading: "Social Media Content Planner"
- Subheading: "Plan, organize, and track your content across all platforms."
- Quick action buttons: "Add Content" (primary) + "View Calendar" (secondary)
- Sits above the stat cards

## Footer
- Simple one-liner: "SMCP v1.0 — Built for creators who plan ahead."
- Muted text, centered, 12px

---

# 2. NEW STATUSES

## Current
| Status | Color |
|--------|-------|
| Planned | Amber (#F59E0B) |
| Posted | Green (#22C55E) |

## New Status Workflow

```
Draft → Approval Pending → Approved → Planned → Posted
```

| Status | Badge Color | Background | Text Color | Meaning |
|--------|------------|------------|------------|---------|
| Draft | Gray | #F3F4F6 | #374151 | Initial idea, not finalized |
| Approval Pending | Purple | #EDE9FE | #5B21B6 | Sent for review/approval |
| Approved | Blue | #DBEAFE | #1E40AF | Approved, ready to schedule |
| Planned | Amber | #FEF3C7 | #92400E | Scheduled with a date |
| Posted | Green | #D1FAE5 | #065F46 | Published/live |

## Changes Required

### planner.py
- No logic changes needed — status is a string field, any value works
- Update `get_stats()` to count all 5 statuses

### templates/add.html
- Update status dropdown to include all 5 options
- Default selection: "Draft"

### templates/content.html
- Add badge classes for Draft, Approval Pending, Approved
- Update status filter dropdown to include all 5 options
- Update action buttons: show next logical status transition
  - Draft → "Send for Approval"
  - Approval Pending → "Approve"
  - Approved → "Schedule"
  - Planned → "Mark Posted"
  - Posted → "Revert to Planned"

### static/style.css
- Add 3 new badge classes: `.badge-draft`, `.badge-pending`, `.badge-approved`

### Dashboard stat cards
- Change from 3 cards to a 5-column row (or 2 rows of 3)
- Show count for each status

---

# 3. NEW FEATURES

## Priority: HIGH (Core Value)

### 3a. Delete Content
- **What**: Red trash icon button in Action column on Content List
- **Why**: Users need to remove outdated or wrong entries
- **How**:
  - Add `delete_content(content_id)` to planner.py
  - Add `POST /delete` route in app.py
  - Confirmation prompt before delete (JS confirm dialog)
- **Files**: planner.py, app.py, content.html

### 3b. Edit Content
- **What**: Pencil icon button in Action column, opens pre-filled form
- **Why**: Users need to update title, date, platform without deleting and re-adding
- **How**:
  - Add `get_content_by_id(content_id)` to planner.py
  - Add `update_content(content_id, data)` to planner.py
  - Add `GET/POST /edit/<id>` route in app.py
  - Create edit.html (reuse add.html form with pre-filled values)
- **Files**: planner.py, app.py, templates/edit.html

### 3c. Search by Title
- **What**: Text search input in the filter bar on Content List
- **Why**: When content grows, users need to find posts by name quickly
- **How**:
  - Add search input field in content.html filter bar
  - Update `filter_content()` to accept `search` keyword parameter
  - Use case-insensitive partial match: `df[df["Title"].str.contains(search, case=False)]`
- **Files**: planner.py, content.html, app.py

### 3d. Notes/Description Field
- **What**: Optional text area when adding content for caption drafts, hashtags, links
- **Why**: Planners need to attach the actual post copy to the schedule
- **How**:
  - Add "Notes" column to Excel schema
  - Add textarea to add.html and edit.html
  - Show as expandable row or tooltip in content table
- **Files**: planner.py, add.html, edit.html, content.html, data/content.xlsx

---

## Priority: MEDIUM (Analytics & Insight)

### 3e. Analytics Page
- **What**: New `/analytics` route with visual stats
- **Why**: Users want to see patterns — which platform gets most content, status distribution
- **How**:
  - Add `get_analytics()` to planner.py returning:
    - Posts per platform (dict)
    - Posts per status (dict)
    - Posts per week (dict)
    - Most active platform
  - Create analytics.html with:
    - Platform breakdown (horizontal bar using CSS, no JS library needed)
    - Status distribution (progress bars)
    - Weekly posting frequency
  - Add "Analytics" link to navbar
- **Files**: planner.py, app.py, templates/analytics.html, base.html

### 3f. Export to CSV
- **What**: "Export CSV" button on Content List page
- **Why**: Users may need data outside the app (for reports, sharing with teams)
- **How**:
  - Add `GET /export` route that returns CSV file download
  - Use `df.to_csv()` with Flask's `send_file()`
  - Button styled as secondary, placed next to filter bar
- **Files**: app.py, content.html

### 3g. Platform Color Coding
- **What**: Colored dots or subtle background tints per platform in tables
- **Why**: Quick visual scanning — Instagram = pink, Twitter = blue, etc.
- **How**:
  - Add CSS classes: `.platform-instagram`, `.platform-twitter`, etc.
  - Small colored dot before platform name in tables
  - Colors:
    - Instagram: #E1306C
    - Twitter: #1DA1F2
    - LinkedIn: #0A66C2
    - Facebook: #1877F2
    - YouTube: #FF0000
- **Files**: style.css, content.html, home.html, calendar.html

### 3h. Due Date Warnings
- **What**: Visual indicators for posts that are overdue or due today
- **Why**: Prevents missed posting deadlines
- **How**:
  - In templates, compare post date with today
  - Overdue (past date + status Planned/Approved): red highlight row
  - Due today: amber highlight
  - Add small "Overdue" or "Due Today" label next to date
- **Files**: content.html, home.html, style.css (add `.row-overdue`, `.row-due-today`)

---

## Priority: LOW (Polish & Delight)

### 3i. Quick Add from Dashboard
- **What**: Compact inline form on dashboard to add content without navigating away
- **Why**: Reduces friction — one-step adding from the main page
- **How**:
  - Add collapsible card on dashboard with minimal form (Title, Platform, Date)
  - Posts with default status "Draft"
  - Success: refresh dashboard to show updated stats
- **Files**: home.html, app.py

### 3j. Bulk Status Update
- **What**: Checkboxes on content table + "Update Selected" dropdown
- **Why**: When multiple posts need status change (e.g., approve all pending)
- **How**:
  - Add checkboxes column in content table
  - Add "Bulk Actions" dropdown above table (Change status, Delete selected)
  - JS to collect selected IDs, POST to `/bulk-update`
  - Add `bulk_update_status(ids, status)` to planner.py
- **Files**: planner.py, app.py, content.html

### 3k. Dark Mode Toggle
- **What**: Toggle button in navbar to switch light/dark theme
- **Why**: Comfort for users working at night, modern SaaS standard
- **How**:
  - Add CSS variables for dark palette under `[data-theme="dark"]`
  - Toggle sets `data-theme` attribute on body via JS
  - Save preference in localStorage
  - Dark palette: Background #111827, Card #1F2937, Text #F9FAFB, Border #374151
- **Files**: style.css, base.html

### 3l. Print Calendar
- **What**: "Print" button on calendar page
- **Why**: Teams that pin weekly schedules on office boards
- **How**:
  - Add `@media print` styles in CSS
  - Hide navbar, buttons, non-essential UI in print
  - Button triggers `window.print()`
- **Files**: style.css, calendar.html

---

# 4. UPDATED DASHBOARD LAYOUT

```
┌─────────────────────────────────────────────────────┐
│  SMCP — Social Media Content Planner                │
│  Plan, organize, and track your content.            │
│  [Add Content]  [View Calendar]                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐          │
│  │Draft│ │Pend.│ │Appr.│ │Plan.│ │Post.│           │
│  │  3  │ │  2  │ │  4  │ │  5  │ │  8  │           │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘          │
│                                                     │
│  ┌──────────────────────┐ ┌──────────────┐          │
│  │  Upcoming Posts (3d)  │ │ Suggestions  │          │
│  │  ┌─────────────────┐ │ │              │          │
│  │  │ Title  Plat Date│ │ │ - Tip 1      │          │
│  │  │ ...              │ │ │ - Tip 2      │          │
│  │  └─────────────────┘ │ │ - Tip 3      │          │
│  └──────────────────────┘ └──────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐           │
│  │  Quick Add (collapsible)             │           │
│  │  [Title] [Platform v] [Date] [Add]   │           │
│  └──────────────────────────────────────┘           │
└─────────────────────────────────────────────────────┘
```

---

# 5. UPDATED NAVBAR

```
┌──────────────────────────────────────────────────────┐
│ [SMCP]  Dashboard  Add Content  Content List  Calendar  Analytics │
└──────────────────────────────────────────────────────┘
```

---

# 6. IMPLEMENTATION ORDER

Recommended sequence to avoid breaking the app:

| Step | Feature | Risk | Depends On |
|------|---------|------|------------|
| 1 | New statuses (5 statuses) | LOW | None |
| 2 | Branding (SMCP, hero, footer) | LOW | None |
| 3 | Delete content | LOW | None |
| 4 | Edit content | LOW | None |
| 5 | Search by title | LOW | None |
| 6 | Platform color coding | LOW | None |
| 7 | Due date warnings | LOW | None |
| 8 | Notes field | MEDIUM | Modifies Excel schema |
| 9 | Export CSV | LOW | None |
| 10 | Analytics page | LOW | None |
| 11 | Quick add from dashboard | LOW | None |
| 12 | Dark mode | LOW | None |
| 13 | Bulk status update | MEDIUM | JS required |
| 14 | Print calendar | LOW | None |

---

# 7. FILES AFFECTED SUMMARY

| File | Changes |
|------|---------|
| planner.py | New functions: delete, edit, get_by_id, analytics, bulk_update, search |
| app.py | New routes: /delete, /edit, /analytics, /export, /bulk-update |
| base.html | SMCP branding, footer, Analytics nav link, dark mode toggle |
| home.html | Hero section, 5 stat cards, quick add form |
| add.html | 5 status options, Notes textarea |
| content.html | New badges, action buttons, search input, delete button, edit link, checkboxes, export button |
| calendar.html | Print button, due date highlights |
| style.css | 3 new badge classes, platform colors, dark mode, print styles, overdue/due-today highlights |
| templates/edit.html | New file — edit form |
| templates/analytics.html | New file — analytics page |
| data/content.xlsx | Add Notes column (step 8 only) |

---

# 8. RULES

- Test after each step before moving to next
- Never modify Excel column structure without migrating existing data
- Keep all changes backward-compatible with existing data
- No JavaScript libraries — vanilla JS only where needed
- No breaking changes to existing routes
- Follow DESIGN.md color system for all new UI elements
