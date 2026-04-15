from flask import Flask, render_template, request, redirect, url_for, Response
import os
import json
import urllib.request
import urllib.error
from planner import (
    add_content, get_all_content, filter_content,
    update_status, delete_content, get_content_by_id, update_content,
    get_stats, get_upcoming_posts, get_weekly_calendar, get_content_suggestions,
    get_analytics, bulk_update_status, update_posted_link, get_recent_posts
)

app = Flask(__name__)


def _load_local_env():
    """Load key/value pairs from .env into process env if not already set."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


_load_local_env()


def render_home(ai_suggestions=None, ai_error=None):
    stats = get_stats()
    upcoming = get_upcoming_posts(days=3)
    suggestions = get_content_suggestions()
    recent_posts = get_recent_posts(limit=3)
    quick_added = request.args.get("quick_added") == "1"
    return render_template(
        "home.html",
        stats=stats,
        upcoming=upcoming,
        suggestions=suggestions,
        recent_posts=recent_posts,
        quick_added=quick_added,
        ai_suggestions=ai_suggestions or [],
        ai_error=ai_error,
    )


@app.context_processor
def inject_today():
    from datetime import datetime
    return {"today_str": datetime.today().strftime("%Y-%m-%d")}


@app.route("/")
def home():
    return render_home()


def _call_gemini_for_suggestions(prompt_text):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return [], "Set GEMINI_API_KEY in your environment to use AI suggestions."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    body = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return [], f"Gemini API error: {e.code}"
    except urllib.error.URLError:
        return [], "Network error while contacting Gemini API."
    except Exception:
        return [], "Unexpected error while generating suggestions."

    text_parts = []
    candidates = payload.get("candidates", [])
    for cand in candidates:
        content = cand.get("content", {})
        for part in content.get("parts", []):
            txt = part.get("text", "").strip()
            if txt:
                text_parts.append(txt)

    if not text_parts:
        return [], "No suggestion text returned by Gemini."

    merged = "\n".join(text_parts)
    lines = [line.strip(" -•\t") for line in merged.splitlines() if line.strip()]
    cleaned = [line for line in lines if len(line) > 3]
    return cleaned[:3], None


@app.route("/get-ai-suggestions", methods=["POST"])
def get_ai_suggestions():
    recent = get_recent_posts(limit=3)
    stats = get_stats()

    recent_summary = []
    for index, row in enumerate(recent, start=1):
        recent_summary.append(
            f"{index}. {row.get('Title', '')} | Platform: {row.get('Platform', '')} | Type: {row.get('Type', '')} | Status: {row.get('Status', '')} | Date: {row.get('Date', '')}"
        )

    latest_post = recent[0] if recent else None
    latest_context = "No recent post available."
    if latest_post:
        latest_context = (
            f"Latest post: {latest_post.get('Title', '')} on {latest_post.get('Platform', '')} "
            f"as a {latest_post.get('Type', '')} with status {latest_post.get('Status', '')}."
        )

    prompt_text = (
        "You are a social media strategist. Create exactly 3 independent next-post suggestions, one for each recent post listed below. "
        "Suggestion 1 must follow recent post 1, suggestion 2 must follow recent post 2, and suggestion 3 must follow recent post 3. "
        "Keep each suggestion on the same platform as its matching recent post. Do not reuse LinkedIn unless the matching recent post is on LinkedIn. "
        "If recent post 2 is Facebook, suggestion 2 must be for Facebook. If a recent post is about personal loans, keep its related topic and format aligned to that post. "
        "Return each suggestion as a single line in this format: Platform: Idea (Format).\n\n"
        f"Current status counts: Draft={stats.get('draft', 0)}, Pending={stats.get('pending', 0)}, "
        f"Approved={stats.get('approved', 0)}, Planned={stats.get('planned', 0)}, Posted={stats.get('posted', 0)}\n"
        f"{latest_context}\n"
        "Recent posts to match one-to-one:\n"
        + ("\n".join(recent_summary) if recent_summary else "- No recent posts")
    )

    ai_suggestions, ai_error = _call_gemini_for_suggestions(prompt_text)
    return render_home(ai_suggestions=ai_suggestions, ai_error=ai_error)


@app.route("/add", methods=["GET", "POST"])
def add():
    message = None
    if request.method == "POST":
        title = request.form["title"]
        platform = request.form["platform"]
        content_type = request.form["type"]
        date = request.form["date"]
        status = request.form["status"]
        notes = request.form.get("notes", "")
        reference_link = request.form.get("reference_link", "")
        posted_link = request.form.get("posted_link", "")

        add_content(title, platform, content_type, date, status, notes, reference_link, posted_link)
        message = "Content added successfully!"

    return render_template("add.html", message=message)


@app.route("/content")
def content_list():
    platform = request.args.get("platform", "")
    date = request.args.get("date", "")
    status = request.args.get("status", "")
    search = request.args.get("search", "")

    filters = {"platform": platform, "date": date, "status": status, "search": search}

    if platform or date or status or search:
        content = filter_content(
            platform=platform or None,
            date=date or None,
            status=status or None,
            search=search or None
        )
    else:
        content = get_all_content()

    return render_template("content.html", content=content, filters=filters)


@app.route("/update-status", methods=["POST"])
def update():
    content_id = request.form["id"]
    new_status = request.form["status"]
    update_status(content_id, new_status)
    return redirect(url_for("content_list"))


@app.route("/edit/<int:content_id>", methods=["GET", "POST"])
def edit(content_id):
    if request.method == "POST":
        update_content(
            content_id,
            request.form["title"],
            request.form["platform"],
            request.form["type"],
            request.form["date"],
            request.form["status"],
            request.form.get("notes", ""),
            request.form.get("reference_link", ""),
            request.form.get("posted_link", ""),
        )
        return redirect(url_for("content_list"))

    item = get_content_by_id(content_id)
    if not item:
        return redirect(url_for("content_list"))
    return render_template("edit.html", item=item)


@app.route("/delete", methods=["POST"])
def delete():
    content_id = request.form["id"]
    delete_content(content_id)
    return redirect(url_for("content_list"))


@app.route("/calendar")
def calendar():
    weekly = get_weekly_calendar()
    return render_template("calendar.html", calendar=weekly)


@app.route("/quick-add", methods=["POST"])
def quick_add():
    title = request.form.get("title", "").strip()
    platform = request.form.get("platform", "")
    date = request.form.get("date", "")
    content_type = request.form.get("type", "Post")
    notes = request.form.get("notes", "")
    reference_link = request.form.get("reference_link", "")

    if title and platform and date:
        add_content(title, platform, content_type, date, "Draft", notes, reference_link, "")

    return redirect(url_for("home", quick_added=1))


@app.route("/set-post-link", methods=["POST"])
def set_post_link():
    content_id = request.form.get("id", "")
    posted_link = request.form.get("posted_link", "")
    if content_id:
        update_posted_link(content_id, posted_link)
    return redirect(url_for("content_list"))


@app.route("/analytics")
def analytics():
    data = get_analytics()
    return render_template("analytics.html", analytics=data)


@app.route("/export")
def export_csv():
    platform = request.args.get("platform", "")
    date = request.args.get("date", "")
    status = request.args.get("status", "")
    search = request.args.get("search", "")

    if platform or date or status or search:
        rows = filter_content(
            platform=platform or None,
            date=date or None,
            status=status or None,
            search=search or None,
        )
    else:
        rows = get_all_content()

    import pandas as pd
    df = pd.DataFrame(rows)
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=smcp_content_export.csv"},
    )


@app.route("/bulk-update", methods=["POST"])
def bulk_update():
    ids = request.form.getlist("ids")
    new_status = request.form.get("status", "")
    if ids and new_status:
        bulk_update_status(ids, new_status)
    return redirect(url_for("content_list"))


if __name__ == "__main__":
    app.run(debug=True)
