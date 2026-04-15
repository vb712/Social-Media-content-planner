# DESIGN SYSTEM – Social Media Content Planner

## 🎯 Design Goal
Create a modern SaaS-style dashboard UI that feels clean, minimal, and professional.
Inspired by Notion, Linear, and Stripe dashboards.

---

# 🎨 Color System

## Primary Colors
- Primary: #4F46E5 (Indigo)
- Secondary: #22C55E (Green)
- Accent: #F59E0B (Amber)

## Neutral Colors
- Background: #F9FAFB
- Card: #FFFFFF
- Border: #E5E7EB
- Text Primary: #111827
- Text Secondary: #6B7280

## Status Colors
- Planned: #F59E0B (Amber)
- Posted: #22C55E (Green)
- Upcoming: #3B82F6 (Blue)

---

# ✍️ Typography

- Font Family: Inter, sans-serif
- Heading:
  - H1: 24px, bold
  - H2: 20px, semi-bold
- Body: 14px regular
- Small text: 12px

---

# 📐 Spacing System

- Base unit: 8px
- Padding:
  - Small: 8px
  - Medium: 16px
  - Large: 24px

---

# 🧩 Components

## 1. Navbar
- Fixed top
- White background
- Contains:
  - Logo (left)
  - Navigation links (Dashboard, Add Content, Content List)
- Height: 60px
- Border-bottom: 1px solid #E5E7EB

---

## 2. Cards
- Background: white
- Border-radius: 12px
- Padding: 16px
- Shadow: subtle

Used for:
- Stats
- Upcoming posts
- Dashboard widgets

---

## 3. Buttons

### Primary Button
- Background: #4F46E5
- Text: white
- Border-radius: 8px

### Secondary Button
- Border: 1px solid #E5E7EB
- Background: white

---

## 4. Tables

- Full width
- Header:
  - Background: #F3F4F6
  - Bold text
- Row hover: light grey
- Border bottom for rows

---

## 5. Status Badges

- Planned → Yellow background
- Posted → Green background
- Rounded pill shape
- Small padding

---

## 6. Forms

- Input fields:
  - Border: 1px solid #E5E7EB
  - Border-radius: 8px
  - Padding: 8px
- Labels above inputs

---

# 🖥️ Page Layouts

## Dashboard
- Top: 3 stat cards
  - Total Posts
  - Upcoming Posts
  - Posted Content
- Below:
  - Upcoming posts table

---

## Add Content Page
- Centered form
- Max width: 500px
- Clean vertical layout

---

## Content List Page
- Filters at top
- Table below

---

## Calendar View
- Simple weekly table
- Group by date

---

# 🎯 UX Rules

- Keep everything minimal
- Avoid clutter
- Use whitespace generously
- Always align elements properly
- No heavy animations

---

# ⚡ Design Principles

- Clean > Fancy
- Readable > Decorative
- Fast > Complex

---

# 🧠 AI Instruction

When generating UI:
- Always use cards for grouping
- Always use consistent spacing (8px grid)
- Prefer simple layouts over complex ones
- Keep everything responsive