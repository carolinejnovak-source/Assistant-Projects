import os
import markdown as md_lib
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory, Markup
from auth import login_required, APP_USERNAME, APP_PASSWORD

SETUP_GUIDE_PASSWORD = os.environ.get("SETUP_GUIDE_PASSWORD", "Crap4Days!")
SETUP_GUIDE_USERNAME = os.environ.get("SETUP_GUIDE_USERNAME", "CarolineJNovak")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vtc-assistant-projects-secret-2024")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username.lower() == APP_USERNAME.lower() and password.lower() == APP_PASSWORD.lower():
            session["logged_in"] = True
            session["username"] = username
            next_url = request.args.get("next", "/")
            return redirect(next_url)
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    projects = [
        {
            "name": "Clinic Demographics Analyzer",
            "url": "https://mikala.vipmedicalgroup.ai/clinic-demographics/",
            "description": "Population density, income, insurance coverage, CPT 36475 volume, and Fair Health benchmarks for all clinic locations.",
            "status": "live",
        },
        {
            "name": "VIP Lease Review",
            "url": "https://mikala.vipmedicalgroup.ai/lease-review/",
            "description": "Upload a lease and get a full 60-point review against VIP Medical Group standards — plus a redlined Word document with tracked changes ready for your attorney.",
            "status": "live",
        },
        {
            "name": "Scheduling",
            "url": "https://mikala.vipmedicalgroup.ai/scheduling/",
            "description": "Calendly-style booking page for Dr. Caroline Novak — share a link, let people pick a 30-min slot, and auto-generate Google Meet invites.",
            "status": "live",
        },
        {
            "name": "Compliance Orchestrator",
            "url": "https://compliance-orchestrator.onrender.com",
            "description": "Compliance workflow management and orchestration tool.",
            "status": "live",
        },
        {
            "name": "Mikala Spending",
            "url": "https://mikala-spending.onrender.com",
            "description": "Monthly cost tracker for all Mikala-related subscriptions — Render, Hostinger, GitHub, SlyNumber, and Anthropic token spend.",
            "status": "live",
        },
        {
            "name": "VIP Provider Training Hub",
            "url": "https://vip-provider-training.onrender.com",
            "description": "Collaborative medical policy repository and provider training resource hub — built with Friday.",
            "status": "live",
        },
    ]
    return render_template("index.html", projects=projects)


def _setup_guide_auth_required(f):
    """Decorator: require setup-guide–specific login."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("setup_guide_auth"):
            return redirect(url_for("setup_guide_login", next=request.url))
        return f(*args, **kwargs)
    return decorated


@app.route("/setup-guide/login", methods=["GET", "POST"])
def setup_guide_login():
    error = None
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "").strip()
        if u.lower() == SETUP_GUIDE_USERNAME.lower() and p == SETUP_GUIDE_PASSWORD:
            session["setup_guide_auth"] = True
            next_url = request.args.get("next") or url_for("setup_guide")
            return redirect(next_url)
        error = "Invalid username or password."
    return render_template("setup_guide_login.html", error=error)


@app.route("/setup-guide/logout")
def setup_guide_logout():
    session.pop("setup_guide_auth", None)
    return redirect(url_for("setup_guide_login"))


@app.route("/setup-guide")
@_setup_guide_auth_required
def setup_guide():
    guide_path = os.path.join(os.path.dirname(__file__), "SETUP_GUIDE.md")
    try:
        with open(guide_path, "r", encoding="utf-8") as f:
            raw_md = f.read()
        html_content = Markup(md_lib.markdown(raw_md, extensions=["fenced_code", "tables", "toc"]))
    except FileNotFoundError:
        html_content = Markup("<p>Setup guide not found.</p>")
    has_pdf = os.path.isfile(os.path.join(os.path.dirname(__file__), "AI_Assistant_Setup_Guide.pdf"))
    return render_template("setup_guide.html", content=html_content, has_pdf=has_pdf)


@app.route("/setup-guide/pdf")
@_setup_guide_auth_required
def setup_guide_pdf():
    directory = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(directory, "AI_Assistant_Setup_Guide.pdf", as_attachment=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
