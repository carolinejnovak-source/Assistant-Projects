import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from auth import login_required, APP_USERNAME, APP_PASSWORD

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
            "url": "https://clinic-demographics.onrender.com",
            "description": "Population density, income, insurance coverage, CPT 36475 volume, and Fair Health benchmarks for all clinic locations.",
            "status": "live",
        },
        {
            "name": "VIP Lease Review",
            "url": "https://lease-review.onrender.com",
            "description": "Upload a lease and get a full 60-point review against VIP Medical Group standards — plus a redlined Word document with tracked changes ready for your attorney.",
            "status": "live",
        },
    ]
    return render_template("index.html", projects=projects)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
