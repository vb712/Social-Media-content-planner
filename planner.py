# planner.py — Business logic for Social Media Content Planner

import pandas as pd
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "content.xlsx")
REQUIRED_COLUMNS = [
    "ID", "Title", "Platform", "Type", "Date", "Status", "Notes", "ReferenceLink", "PostedLink"
]


def load_data():
    """Read content.xlsx and return a DataFrame."""
    if not os.path.exists(EXCEL_PATH):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        df.to_excel(EXCEL_PATH, index=False)
        return df

    df = pd.read_excel(EXCEL_PATH)
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[REQUIRED_COLUMNS]
    for text_col in ["Notes", "ReferenceLink", "PostedLink"]:
        if text_col in df.columns:
            df[text_col] = df[text_col].fillna("")
    return df


def save_data(df):
    """Write DataFrame back to content.xlsx."""
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[REQUIRED_COLUMNS]
    df.to_excel(EXCEL_PATH, index=False)


def add_content(title, platform, content_type, date, status, notes="", reference_link="", posted_link=""):
    """Add a new row with auto-generated ID."""
    df = load_data()

    if df.empty:
        new_id = 1
    else:
        new_id = int(df["ID"].max()) + 1

    new_row = pd.DataFrame([{
        "ID": new_id,
        "Title": title,
        "Platform": platform,
        "Type": content_type,
        "Date": date,
        "Status": status,
        "Notes": notes or "",
        "ReferenceLink": reference_link or "",
        "PostedLink": posted_link or "",
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    return new_id


def get_all_content():
    """Return all rows as a list of dicts."""
    df = load_data()
    for text_col in ["Notes", "ReferenceLink", "PostedLink"]:
        df[text_col] = df[text_col].fillna("")
    return df.to_dict(orient="records")


def filter_content(platform=None, date=None, status=None, search=None):
    """Return filtered rows based on criteria."""
    df = load_data()

    if platform:
        df = df[df["Platform"] == platform]
    if date:
        df = df[df["Date"] == date]
    if status:
        df = df[df["Status"] == status]
    if search:
        df = df[df["Title"].str.contains(search, case=False, na=False)]

    for text_col in ["Notes", "ReferenceLink", "PostedLink"]:
        df[text_col] = df[text_col].fillna("")
    return df.to_dict(orient="records")


def update_status(content_id, new_status):
    """Update the status of a specific entry by ID."""
    df = load_data()
    mask = df["ID"] == int(content_id)

    if mask.any():
        df.loc[mask, "Status"] = new_status
        save_data(df)
        return True
    return False


def get_content_by_id(content_id):
    """Return a single content entry by ID."""
    df = load_data()
    mask = df["ID"] == int(content_id)
    if mask.any():
        row = df[mask].iloc[0].to_dict()
        for text_col in ["Notes", "ReferenceLink", "PostedLink"]:
            if pd.isna(row.get(text_col, "")):
                row[text_col] = ""
        return row
    return None


def update_content(
    content_id,
    title,
    platform,
    content_type,
    date,
    status,
    notes="",
    reference_link="",
    posted_link="",
):
    """Update all fields of a content entry by ID."""
    df = load_data()
    mask = df["ID"] == int(content_id)
    if mask.any():
        df.loc[mask, "Title"] = title
        df.loc[mask, "Platform"] = platform
        df.loc[mask, "Type"] = content_type
        df.loc[mask, "Date"] = date
        df.loc[mask, "Status"] = status
        df.loc[mask, "Notes"] = notes or ""
        df.loc[mask, "ReferenceLink"] = reference_link or ""
        df.loc[mask, "PostedLink"] = posted_link or ""
        save_data(df)
        return True
    return False


def update_posted_link(content_id, posted_link):
    """Update only the posted link for a content row."""
    df = load_data()
    mask = df["ID"] == int(content_id)
    if mask.any():
        df.loc[mask, "PostedLink"] = posted_link or ""
        save_data(df)
        return True
    return False


def delete_content(content_id):
    """Delete a content entry by ID."""
    df = load_data()
    mask = df["ID"] == int(content_id)
    if mask.any():
        df = df[~mask]
        save_data(df)
        return True
    return False


def get_stats():
    """Return dashboard statistics."""
    df = load_data()
    total = len(df)
    if df.empty:
        return {"total": 0, "draft": 0, "pending": 0, "approved": 0, "planned": 0, "posted": 0}
    return {
        "total": total,
        "draft": len(df[df["Status"] == "Draft"]),
        "pending": len(df[df["Status"] == "Approval Pending"]),
        "approved": len(df[df["Status"] == "Approved"]),
        "planned": len(df[df["Status"] == "Planned"]),
        "posted": len(df[df["Status"] == "Posted"]),
    }


def get_upcoming_posts(days=3):
    """Return posts scheduled within the next N days."""
    from datetime import datetime, timedelta

    df = load_data()
    if df.empty:
        return []

    today = datetime.today().date()
    end_date = today + timedelta(days=days)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    upcoming = df[(df["Date"] >= today) & (df["Date"] <= end_date)]
    upcoming = upcoming.sort_values("Date")

    result = upcoming.to_dict(orient="records")
    for row in result:
        if row["Date"]:
            row["Date"] = row["Date"].strftime("%Y-%m-%d")
    return result


def get_weekly_calendar():
    """Return posts for the next 7 days grouped by date."""
    from datetime import datetime, timedelta

    df = load_data()
    today = datetime.today().date()

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    calendar = {}
    for i in range(7):
        day = today + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_label = day.strftime("%A, %b %d")
        if not df.empty:
            day_posts = df[df["Date"] == day].to_dict(orient="records")
        else:
            day_posts = []
        calendar[day_str] = {"label": day_label, "posts": day_posts}

    return calendar


def get_content_suggestions():
    """Return simple content suggestions based on gaps."""
    df = load_data()
    suggestions = []

    all_platforms = ["Instagram", "Twitter", "LinkedIn", "Facebook", "YouTube"]

    if df.empty:
        suggestions.append("Start by adding your first post!")
        suggestions.append("Try scheduling content for Instagram or LinkedIn.")
        return suggestions

    used_platforms = df["Platform"].unique().tolist()
    missing = [p for p in all_platforms if p not in used_platforms]
    if missing:
        suggestions.append(f"You haven't posted on {', '.join(missing[:2])} yet. Consider expanding!")

    planned = len(df[df["Status"] == "Planned"])
    if planned == 0:
        suggestions.append("No planned posts! Schedule some upcoming content.")
    elif planned > 5:
        suggestions.append(f"You have {planned} planned posts. Time to start posting!")

    from datetime import datetime, timedelta
    today = datetime.today().date()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    next_3 = df[(df["Date"] >= today) & (df["Date"] <= today + timedelta(days=3))]
    if len(next_3) == 0:
        suggestions.append("No posts in the next 3 days. Plan ahead!")

    if not suggestions:
        suggestions.append("You're on track! Keep up the great work.")

    return suggestions


def get_recent_posts(limit=5):
    """Return most recent posts by date, newest first."""
    df = load_data()
    if df.empty:
        return []

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date", ascending=False)
    recent = df.head(limit).copy()
    recent["Date"] = recent["Date"].dt.strftime("%Y-%m-%d")

    for text_col in ["Notes", "ReferenceLink", "PostedLink"]:
        if text_col in recent.columns:
            recent[text_col] = recent[text_col].fillna("")

    return recent.to_dict(orient="records")


def get_analytics():
    """Return simple analytics snapshots for platform, status, and weekly activity."""
    df = load_data()
    if df.empty:
        return {
            "platform_counts": {},
            "status_counts": {},
            "weekly_counts": {},
            "most_active_platform": "-",
            "max_platform_count": 0,
            "max_status_count": 0,
            "max_weekly_count": 0,
        }

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    platform_counts = df["Platform"].value_counts().to_dict()
    status_counts = df["Status"].value_counts().to_dict()

    dated = df.dropna(subset=["Date"]).copy()
    if dated.empty:
        weekly_counts = {}
    else:
        dated["Week"] = dated["Date"].dt.to_period("W-SUN").astype(str)
        weekly_counts = dated["Week"].value_counts().sort_index().to_dict()

    most_active_platform = max(platform_counts, key=platform_counts.get) if platform_counts else "-"

    return {
        "platform_counts": platform_counts,
        "status_counts": status_counts,
        "weekly_counts": weekly_counts,
        "most_active_platform": most_active_platform,
        "max_platform_count": max(platform_counts.values()) if platform_counts else 0,
        "max_status_count": max(status_counts.values()) if status_counts else 0,
        "max_weekly_count": max(weekly_counts.values()) if weekly_counts else 0,
    }


def bulk_update_status(ids, new_status):
    """Update status for multiple content IDs."""
    if not ids:
        return 0

    valid_ids = [int(i) for i in ids if str(i).strip().isdigit()]
    if not valid_ids:
        return 0

    df = load_data()
    mask = df["ID"].isin(valid_ids)
    updated = int(mask.sum())
    if updated:
        df.loc[mask, "Status"] = new_status
        save_data(df)
    return updated
