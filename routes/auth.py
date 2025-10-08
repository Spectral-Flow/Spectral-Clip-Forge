"""
Authentication Route Blueprint
Guard the gates of the forge (optional OAuth)
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for
from app import db, limiter, logger
from models import User, AuditLog
from datetime import datetime
import os

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "false").lower() == "true"


@bp.route("/register", methods=["POST"])
@limiter.limit("3/hour")
def register():
    """
    Register a new user
    Join the ranks of the forge masters
    """
    if not OAUTH_ENABLED:
        return (
            jsonify(
                {"error": "Authentication disabled", "message": "User registration is not enabled"}
            ),
            403,
        )

    try:
        data = request.json
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        # Validate input
        if not username or not email or not password:
            return (
                jsonify(
                    {
                        "error": "Incomplete ritual",
                        "message": "Username, email, and password required",
                    }
                ),
                400,
            )

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Name claimed", "message": "Username already exists"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Identity known", "message": "Email already registered"}), 400

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Log registration
        AuditLog.log_action(
            "user_register", user_id=user.id, details={"username": username, "email": email}
        )

        logger.info(f"New user registered: {username}")

        return (
            jsonify({"success": True, "message": "Welcome to the forge", "user": user.to_dict()}),
            201,
        )

    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return jsonify({"error": "Ritual failed", "message": "Could not register user"}), 500


@bp.route("/login", methods=["POST"])
@limiter.limit("5/minute")
def login():
    """
    Login with username/password
    Enter the forge
    """
    if not OAUTH_ENABLED:
        return (
            jsonify({"error": "Authentication disabled", "message": "User login is not enabled"}),
            403,
        )

    try:
        data = request.json
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return (
                jsonify(
                    {"error": "Incomplete credentials", "message": "Username and password required"}
                ),
                400,
            )

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            # Log failed attempt
            AuditLog.log_action("login_failed", details={"username": username})
            return jsonify({"error": "Gates remain closed", "message": "Invalid credentials"}), 401

        if not user.is_active:
            return jsonify({"error": "Access revoked", "message": "Account is disabled"}), 403

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Set session
        session["user_id"] = user.id
        session["username"] = user.username

        # Log successful login
        AuditLog.log_action("login_success", user_id=user.id)

        logger.info(f"User logged in: {username}")

        return (
            jsonify(
                {"success": True, "message": "The gates open before you", "user": user.to_dict()}
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({"error": "Entry denied", "message": "Login failed"}), 500


@bp.route("/logout", methods=["POST"])
def logout():
    """
    Logout current user
    Depart from the forge
    """
    if not OAUTH_ENABLED:
        return jsonify({"error": "Authentication disabled"}), 403

    user_id = session.get("user_id")
    if user_id:
        AuditLog.log_action("logout", user_id=user_id)

    session.clear()

    return jsonify({"success": True, "message": "May the Spectral Flow guide you"}), 200


@bp.route("/me", methods=["GET"])
def get_current_user():
    """
    Get current authenticated user
    Know thyself
    """
    if not OAUTH_ENABLED:
        return jsonify({"authenticated": False, "message": "Authentication not enabled"}), 200

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"authenticated": False}), 200

    user = User.query.get(user_id)

    if not user:
        session.clear()
        return jsonify({"authenticated": False}), 200

    return jsonify({"authenticated": True, "user": user.to_dict()}), 200
