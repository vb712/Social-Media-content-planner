# Social Media Content Planner

A simple Flask-based social media planning app that stores content in an Excel workbook. The app helps you plan posts, track status, review upcoming content, manage links and notes, and generate AI-powered next-post suggestions.

## What the app does

- Add new content ideas and scheduled posts
- View all content in a table-based content list
- Filter by platform, date, status, and search text
- Update content status through the workflow
- Attach reference links and posted links
- View upcoming posts and a weekly calendar
- Export filtered content to CSV
- Review analytics for platform, status, and weekly activity
- Use quick add from the dashboard
- Switch between light and dark mode
- Generate next-post ideas with Google Gemini
- Bulk update content status
- Print the weekly calendar

## Tech Stack

- Python 3
- Flask
- pandas
- openpyxl
- HTML, CSS, and Jinja2 templates
- Bootstrap 5
- Google Gemini API for AI suggestions

## Project Structure

- `app.py` handles Flask routes, page rendering, form submission, CSV export, analytics, quick add, bulk updates, and Gemini suggestions.
- `planner.py` contains the business logic and Excel storage helpers.
- `data/content.xlsx` is the main database file.
- `templates/` contains the pages and Jinja macros.
- `static/style.css` contains the custom UI design system and dark mode styles.
- `requirements.txt` lists the Python packages needed to run the app.
- `.env` stores local secrets such as the Gemini API key.

## Architecture

The app follows a simple split between web routing and business logic.

- Flask routes in `app.py` receive requests, validate form data, and decide which template to render.
- `planner.py` reads and writes the Excel workbook, keeps the schema consistent, and provides helper functions for filtering, statistics, calendar generation, and recent-post lookups.
- Templates in `templates/` are responsible for presentation only.
- The dashboard and content list use helper data from `planner.py` so the UI stays thin and easy to maintain.
- AI suggestions are generated in `app.py` by sending recent content context to Google Gemini and rendering the returned ideas on the dashboard.

## Data Model

Each content row is stored in Excel with these columns:

- `ID`
- `Title`
- `Platform`
- `Type`
- `Date`
- `Status`
- `Notes`
- `ReferenceLink`
- `PostedLink`

### Status workflow

The app supports this content flow:

- `Draft`
- `Approval Pending`
- `Approved`
- `Planned`
- `Posted`

## Installation

### 1. Clone or open the project

Open the folder that contains the Flask app.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install flask pandas openpyxl
```

If you want to use the Gemini feature, also make sure outbound HTTPS access is available.

### If you send the project to a friend as a zip

Send these items in the zip:

- `app.py`
- `planner.py`
- `requirements.txt`
- `templates/`
- `static/`
- `data/`
- `README.md`
- `.env` only if you want Gemini suggestions to work on their machine

Optional but useful:

- `data/content.xlsx` if you want them to get your current content data

You do not need to send:

- `.venv/`
- `__pycache__/`
- `*.pyc`

If `data/content.xlsx` is missing, the app will create it automatically the first time it runs.

### Steps for your friend to run it

1. Unzip the project folder.
2. Open a terminal in the project root.
3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate it:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```bat
.\.venv\Scripts\activate.bat
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

6. If you want Gemini suggestions, create a `.env` file and add:

```env
GEMINI_API_KEY=your_api_key_here
```

7. Start the app:

```bash
python app.py
```

8. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

### 4. Configure the Gemini API key

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=your_api_key_here
```

The app loads this automatically on startup.

If you do not add a Gemini key, the rest of the app still works normally and the AI suggestions card will show a helpful message.

## Running the app

Start the Flask app with:

```bash
python app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Features and How They Work

### Dashboard

The dashboard shows:

- high-level stats
- upcoming posts for the next 3 days
- recent posts
- a quick add panel
- a Gemini-powered suggestion card

The dashboard starts in dark mode by default. The user can switch themes with the toggle in the navigation bar, and the selection is stored in local storage.

### Add Content

The Add Content page saves a full content entry into the Excel workbook. It includes:

- title
- platform
- content type
- date
- status
- notes
- reference link
- posted link

Implementation:

- `app.py` handles the form submission.
- `planner.py:add_content()` appends the row to Excel and assigns the next ID.

### Content List

The content list shows all saved content in a table.

It supports:

- filtering by platform, date, status, and search text
- editing a row
- deleting a row
- changing status quickly
- setting or opening a posted link when content is posted

Implementation:

- `planner.py:filter_content()` handles filtering.
- `planner.py:update_status()` changes the workflow state.
- `planner.py:update_posted_link()` stores the post URL.
- `templates/content.html` renders the action controls and compact badges.

### Notes and Links

The app stores extra planning data in the workbook:

- `Notes` for reminders, hooks, or internal planning details
- `ReferenceLink` for source material or inspiration
- `PostedLink` for the live published URL

Implementation:

- `planner.py` keeps these fields in the schema.
- `templates/add.html` and `templates/edit.html` expose the fields in the UI.

### Calendar

The weekly calendar groups content by day for the next 7 days.

Implementation:

- `planner.py:get_weekly_calendar()` builds a date-keyed calendar object.
- `templates/calendar.html` renders the weekly view.
- The print support is handled with dedicated CSS print styles.

### Upcoming Posts

The dashboard uses the next 3 days of scheduled content to highlight urgent work.

Implementation:

- `planner.py:get_upcoming_posts(days=3)` filters the Excel rows by date.
- Overdue and due-today styling is handled in the templates and CSS.

### Quick Add

The dashboard quick add form is a fast path for creating a draft without opening the full add page.

Implementation:

- `app.py:/quick-add` saves the row with status `Draft`.
- The dashboard shows a confirmation message after submission.

### CSV Export

The app can export the current filtered list as CSV.

Implementation:

- `app.py:/export` applies the same filters used by the content list.
- The response is returned as a downloadable CSV file.

### Analytics

The analytics page shows summary data from the Excel workbook.

Implementation:

- `planner.py:get_analytics()` calculates platform counts, status counts, and weekly activity.
- `app.py:/analytics` renders the analytics page.

### Bulk Status Update

The app supports changing many rows at once.

Implementation:

- `planner.py:bulk_update_status()` updates multiple content IDs.
- `app.py:/bulk-update` receives the selected IDs and target status.

### Dark Mode

Dark mode is the default theme.

Implementation:

- `templates/base.html` initializes the page with `data-theme="dark"` unless a saved theme exists.
- `static/style.css` defines both theme palettes.
- The toggle button updates local storage so the chosen theme persists.

### AI Suggestions

The dashboard has a `Get Suggestions` button that sends the latest content context to Google Gemini.

Implementation:

- `app.py:/get-ai-suggestions` gathers the latest 3 posts and builds the prompt.
- The prompt tells Gemini to generate exactly 3 independent ideas.
- The response is cleaned and truncated before rendering.
- The API key is loaded from `.env`.

## Excel Storage Notes

The workbook is created automatically if it does not exist.

- Main file: `data/content.xlsx`
- The schema is normalized whenever the file is loaded or saved
- Missing columns are added automatically
- Empty values are filled with blank strings for text fields

## Design Notes

The UI is intentionally simple and table-driven, with a dark SaaS-style look.

- Bootstrap handles layout responsiveness
- Custom CSS controls the theme, spacing, badges, cards, and tables
- Platform icons are shown as compact visual chips
- Status badges are small and readable
- The dashboard keeps the most important actions near the top

## Common Files to Know

- `app.py` for routes and AI integration
- `planner.py` for all Excel and business logic
- `templates/base.html` for shared layout and theme handling
- `templates/home.html` for the dashboard
- `templates/content.html` for the content table
- `static/style.css` for the visual system

## Troubleshooting

- If the app does not start, confirm that the virtual environment is activated.
- If Excel is locked in another program, close the workbook before saving from the app.
- If Gemini suggestions do not work, confirm that `.env` exists and `GEMINI_API_KEY` is set.
- If the page still looks light on first load, clear browser local storage for the site so the new default theme can be applied.

## Next Steps

- Add sample content rows if you want a prefilled workbook.
- Expand analytics with charts if you want more reporting.
- Add more workflow states or content fields if your planning process grows.
