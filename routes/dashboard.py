"""
Dashboard Route Blueprint
View your legendary creations
"""
from flask import Blueprint, render_template, session, redirect, url_for
from app import db, logger
from models import User, Job
import os

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "false").lower() == "true"


@bp.route("/")
def index():
    """
    User dashboard
    The hall of forged artifacts
    """
    if not OAUTH_ENABLED:
        # If auth is disabled, show public dashboard
        return render_template("dashboard.html", user=None, jobs=[])

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("index"))

    user = User.query.get(user_id)

    if not user:
        session.clear()
        return redirect(url_for("index"))

    # Get user's jobs
    jobs = Job.query.filter_by(user_id=user.id).order_by(Job.created_at.desc()).limit(20).all()

    return render_template("dashboard.html", user=user, jobs=jobs)


@bp.route("/contributors")
def contributors():
    """
    Contributors page with Eternis-33 Bible link
    The forge masters and their legends
    """
    return render_template("contributors.html")
