# TASKS – Social Media Content Planner

---

# 🧠 HOW TO USE THIS FILE

- Execute tasks phase by phase
- Complete ALL tasks in a phase before moving forward
- Mark tasks as done ✅
- Do not skip steps
- Always test after each phase

---

# 📦 PHASE 0: PROJECT SETUP

## Goal
Initialize project structure and environment

### Tasks
- [ ] Create project folder structure
- [ ] Create required files:
  - app.py
  - planner.py
  - templates/
  - static/
  - data/content.xlsx
- [ ] Install dependencies:
  - Flask
  - pandas
  - openpyxl
- [ ] Create empty Excel file with columns:
  - ID, Title, Platform, Type, Date, Status

### Validation
- [ ] Flask app runs successfully
- [ ] No import errors

---

# ⚙️ PHASE 1: CORE BACKEND (DATA HANDLING)

## Goal
Implement Excel-based data operations

### Tasks
- [ ] Create function: load_data()
- [ ] Create function: save_data()
- [ ] Create function: add_content()
- [ ] Create function: get_all_content()
- [ ] Create function: filter_content()
- [ ] Create function: update_status()

### Validation
- [ ] Data is correctly saved in Excel
- [ ] Data persists after restart
- [ ] Functions return correct results

---

# 🌐 PHASE 2: BASIC FLASK APP

## Goal
Set up routing and base app

### Tasks
- [ ] Initialize Flask app
- [ ] Create base route `/`
- [ ] Setup template rendering
- [ ] Create base layout (base.html)

### Validation
- [ ] App runs on localhost
- [ ] Homepage loads without errors

---

# ➕ PHASE 3: ADD CONTENT FEATURE

## Goal
Allow user to add new content

### Tasks
- [ ] Create `/add` route (GET + POST)
- [ ] Create form UI:
  - Title
  - Platform
  - Type
  - Date
  - Status
- [ ] Connect form to add_content()
- [ ] Add form validation

### Validation
- [ ] Form submits correctly
- [ ] Data appears in Excel
- [ ] No duplicate ID issues

---

# 📋 PHASE 4: VIEW CONTENT

## Goal
Display all content entries

### Tasks
- [ ] Create `/content` route
- [ ] Fetch data from planner.py
- [ ] Display in table format
- [ ] Add columns:
  - Title
  - Platform
  - Type
  - Date
  - Status

### Validation
- [ ] Table displays all data
- [ ] No crashes with empty data

---

# 🔍 PHASE 5: FILTER & SEARCH

## Goal
Filter content dynamically

### Tasks
- [ ] Add filter inputs:
  - Platform dropdown
  - Date picker
  - Status dropdown
- [ ] Modify backend to handle filters
- [ ] Update UI dynamically

### Validation
- [ ] Filters return correct results
- [ ] Multiple filters work together

---

# 🔄 PHASE 6: UPDATE STATUS

## Goal
Update content status

### Tasks
- [ ] Add update button in table
- [ ] Create `/update-status` route
- [ ] Pass content ID
- [ ] Update Excel entry

### Validation
- [ ] Status updates correctly
- [ ] Changes persist in Excel

---

# 📅 PHASE 7: DASHBOARD

## Goal
Create overview page

### Tasks
- [ ] Create dashboard route `/`
- [ ] Add stats:
  - Total posts
  - Planned posts
  - Posted posts
- [ ] Add upcoming posts section

### Validation
- [ ] Stats are accurate
- [ ] Upcoming posts show correctly

---

# ⏳ PHASE 8: UPCOMING POSTS

## Goal
Highlight near-term content

### Tasks
- [ ] Filter next 3 days
- [ ] Display on dashboard
- [ ] Highlight visually

### Validation
- [ ] Correct posts displayed
- [ ] No incorrect date handling

---

# 📆 PHASE 9: WEEKLY CALENDAR

## Goal
Show weekly schedule

### Tasks
- [ ] Create `/calendar` route
- [ ] Filter next 7 days
- [ ] Group posts by date
- [ ] Display in table/calendar format

### Validation
- [ ] Data grouped correctly
- [ ] Dates sorted properly

---

# 🎨 PHASE 10: UI IMPROVEMENT

## Goal
Make UI look professional

### Tasks
- [ ] Add navbar
- [ ] Add cards for dashboard
- [ ] Style tables
- [ ] Add status badges:
  - Planned → Yellow
  - Posted → Green

### Validation
- [ ] UI looks clean and consistent
- [ ] All pages aligned with DESIGN.md

---

# ⭐ PHASE 11: BONUS FEATURES

## Goal
Add extra polish

### Tasks
- [ ] Add content suggestions feature
- [ ] Add quick stats
- [ ] Add empty state UI (no data message)

### Validation
- [ ] Suggestions show correctly
- [ ] No UI breakage

---

# 🧪 PHASE 12: TESTING

## Goal
Ensure system works end-to-end

### Tasks
- [ ] Test all features manually
- [ ] Test edge cases:
  - Empty input
  - Invalid date
- [ ] Fix bugs

### Validation
- [ ] No crashes
- [ ] All features functional

---

# 🚀 PHASE 13: FINAL CLEANUP

## Goal
Prepare for submission/demo

### Tasks
- [ ] Clean code (remove unused parts)
- [ ] Add comments
- [ ] Organize folder structure
- [ ] Ensure readability

### Validation
- [ ] Code is clean and understandable
- [ ] Ready for viva/demo

---

# 🎯 FINAL CHECKLIST

- [ ] Add content works
- [ ] View content works
- [ ] Filter works
- [ ] Update status works
- [ ] Dashboard works
- [ ] Calendar works
- [ ] UI looks professional