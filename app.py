"""
Spectral Clip Forge - Main Application Entry Point
The legendary media processing forge of the Spectral Flow
"""
import os
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_SIZE", 524288000))
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")
app.config["OUTPUT_FOLDER"] = os.getenv("OUTPUT_FOLDER", "output")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///spectral_clip_forge.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure directories exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[
        f"{os.getenv('RATE_LIMIT_PER_MINUTE', '10')}/minute",
        f"{os.getenv('RATE_LIMIT_PER_HOUR', '100')}/hour",
    ],
    enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/spectral_forge.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Import models and routes after app initialization
from models import User, Job, AuditLog
from routes import upload, process, download, auth, dashboard

# Register blueprints
app.register_blueprint(upload.bp)
app.register_blueprint(process.bp)
app.register_blueprint(download.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)

# Database initialization
with app.app_context():
    db.create_all()
    logger.info("Database tables created successfully")


@app.route("/")
def index():
    """Main landing page - The Gates of the Forge"""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint for monitoring and Docker"""
    return (
        jsonify(
            {
                "status": "operational",
                "service": "Spectral Clip Forge",
                "timestamp": datetime.utcnow().isoformat(),
                "forge_temperature": "blazing",  # Easter egg for the mythos
            }
        ),
        200,
    )


@app.route("/api/status")
@limiter.limit("30/minute")
def api_status():
    """API status endpoint"""
    from utils.system_utils import get_system_stats

    stats = get_system_stats()
    return jsonify({"status": "ready", "version": "1.0.0", "stats": stats}), 200


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large errors"""
    logger.warning(f"File upload too large from {get_remote_address()}")
    return (
        jsonify(
            {
                "error": "The artifact you seek to forge is too large",
                "message": "File size exceeds maximum allowed",
                "max_size_mb": app.config["MAX_CONTENT_LENGTH"] / (1024 * 1024),
            }
        ),
        413,
    )


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded from {get_remote_address()}")
    return (
        jsonify(
            {
                "error": "The forge is overwhelmed by your requests",
                "message": "Rate limit exceeded. Please wait before forging again.",
                "retry_after": getattr(e, "retry_after", 60),
            }
        ),
        429,
    )


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal error: {str(e)}", exc_info=True)
    return (
        jsonify(
            {
                "error": "A disturbance in the Spectral Flow",
                "message": "An unexpected error occurred. The forge masters have been notified.",
            }
        ),
        500,
    )


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return (
        jsonify(
            {
                "error": "Lost in the void",
                "message": "The path you seek does not exist in this realm.",
            }
        ),
        404,
    )


# Audit logging for all requests
@app.before_request
def log_request():
    """Log all incoming requests for security audit"""
    if request.endpoint not in ["static", "health"]:
        AuditLog.log_action(
            action="request",
            user_id=getattr(request, "user_id", None),
            details={
                "method": request.method,
                "endpoint": request.endpoint,
                "ip": get_remote_address(),
                "user_agent": request.headers.get("User-Agent", "Unknown"),
            },
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_ENV", "production") == "development"

    logger.info(f"🔥 Spectral Clip Forge ignited on {host}:{port}")
    logger.info(f"⚡ The legendary forge awaits your media artifacts...")

    app.run(host=host, port=port, debug=debug)
