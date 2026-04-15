# Phase 0 — Project Setup (Completed)

## What Was Done

### 1. Folder Structure
Created the following directories:
- `templates/` — HTML templates for Flask
- `static/` — CSS and static assets
- `data/` — Excel storage

### 2. Files Created

| File | Purpose |
|------|---------|
| `app.py` | Flask app with `"/"` route, renders `base.html` |
| `planner.py` | Placeholder for business logic (Phase 1) |
| `templates/base.html` | Base HTML page with Bootstrap 5, Inter font, DESIGN.md colors |
| `data/content.xlsx` | Empty Excel file with columns: ID, Title, Platform, Type, Date, Status |

### 3. Dependencies
Verified installed:
- Flask
- pandas
- openpyxl

---

## How to Test

### Test 1: Run the Flask App
```bash
cd c:/Users/icy/Desktop/mkpb
python app.py
```
- Open browser at `http://127.0.0.1:5000/`
- You should see **"Social Media Content Planner"** heading and **"Welcome! The app is running."** text
- No errors in terminal

### Test 2: Verify Excel File
```bash
python -c "import pandas as pd; df = pd.read_excel('data/content.xlsx'); print(df.columns.tolist()); print('Rows:', len(df))"
```
Expected output:
```
['ID', 'Title', 'Platform', 'Type', 'Date', 'Status']
Rows: 0
```

### Test 3: Verify Imports
```bash
python -c "from app import app; from planner import *; print('All imports OK')"
```
Expected output:
```
All imports OK
```

---

## What's Next — Phase 1: Core Backend

### Goal
Implement Excel-based data operations in `planner.py`

### Functions to Build

| Function | Description |
|----------|-------------|
| `load_data()` | Read content.xlsx and return a DataFrame |
| `save_data(df)` | Write DataFrame back to content.xlsx |
| `add_content(title, platform, type, date, status)` | Add a new row with auto-generated ID |
| `get_all_content()` | Return all rows as a list of dicts |
| `filter_content(platform, date, status)` | Return filtered rows based on criteria |
| `update_status(content_id, new_status)` | Update the status of a specific entry by ID |

### Excel File Path
```
data/content.xlsx
```

### Column Schema
| Column | Type | Example |
|--------|------|---------|
| ID | int | 1, 2, 3 |
| Title | str | "Launch post" |
| Platform | str | "Instagram", "Twitter", "LinkedIn" |
| Type | str | "Reel", "Story", "Post" |
| Date | str (YYYY-MM-DD) | "2026-04-20" |
| Status | str | "Planned", "Posted" |

### Validation Criteria
- Data saves correctly to Excel
- Data persists after app restart
- Functions return correct results
- No crashes with empty Excel file
