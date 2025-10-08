"""
Upload Route Blueprint
Where media artifacts enter the forge
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import app, db, limiter, logger
from models import Job, AuditLog
import os
import uuid
from utils.file_validator import validate_file, scan_for_malware
from utils.file_utils import get_file_info

bp = Blueprint("upload", __name__, url_prefix="/api/upload")

ALLOWED_EXTENSIONS = set(
    os.getenv("ALLOWED_EXTENSIONS", "mp4,mov,avi,mkv,mp3,wav,flac,m4a").split(",")
)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/", methods=["POST"])
@limiter.limit("5/minute")
def upload_file():
    """
    Upload a media file for processing
    The first step in the legendary transformation
    """
    try:
        # Check if file is present
        if "file" not in request.files:
            return (
                jsonify({"error": "No artifact provided", "message": "No file was uploaded"}),
                400,
            )

        file = request.files["file"]

        # Check if filename is present
        if file.filename == "":
            return jsonify({"error": "Nameless artifact", "message": "No file selected"}), 400

        # Validate file extension
        if not allowed_file(file.filename):
            return (
                jsonify(
                    {
                        "error": "Forbidden artifact type",
                        "message": f'File type not allowed. Accepted: {", ".join(ALLOWED_EXTENSIONS)}',
                    }
                ),
                400,
            )

        # Generate secure filename and job ID
        original_filename = secure_filename(file.filename)
        job_id = str(uuid.uuid4())
        file_ext = original_filename.rsplit(".", 1)[1].lower()
        filename = f"{job_id}.{file_ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save file
        file.save(filepath)
        logger.info(f"File uploaded: {filename} (original: {original_filename})")

        # Get file info
        file_info = get_file_info(filepath)

        # Validate file (check if it's actually a valid media file)
        is_valid, validation_error = validate_file(filepath, file_ext)
        if not is_valid:
            os.remove(filepath)
            return jsonify({"error": "Corrupted artifact", "message": validation_error}), 400

        # Malware scan (if enabled)
        if os.getenv("CLAMAV_ENABLED", "false").lower() == "true":
            is_safe, scan_error = scan_for_malware(filepath)
            if not is_safe:
                os.remove(filepath)
                logger.warning(f"Malware detected in file: {filename}")
                AuditLog.log_action("malware_detected", details={"filename": filename})
                return (
                    jsonify({"error": "Tainted artifact", "message": "File failed security scan"}),
                    400,
                )

        # Get processing options from request
        target_formats = request.form.getlist("formats") or ["tiktok", "shorts", "reels"]
        options = {
            "watermark": request.form.get("watermark", "true").lower() == "true",
            "effects": request.form.get("effects", "spectral"),
            "subtitles": request.form.get("subtitles", "false").lower() == "true",
            "caption_style": request.form.get("caption_style", "neon"),
        }

        # Create job record
        job = Job(
            id=job_id,
            filename=original_filename,
            file_size=file_info["size"],
            file_type=file_ext,
            status="pending",
        )
        job.set_target_formats(target_formats)
        job.set_options(options)

        db.session.add(job)
        db.session.commit()

        # Log the upload
        AuditLog.log_action(
            "file_upload",
            details={"job_id": job_id, "filename": original_filename, "size": file_info["size"]},
        )

        # Queue processing task
        from tasks.video_processor import process_video

        process_video.delay(job_id, filepath)

        logger.info(f"Job {job_id} created and queued for processing")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Your artifact enters the forge",
                    "job_id": job_id,
                    "filename": original_filename,
                    "status": "pending",
                    "formats": target_formats,
                }
            ),
            202,
        )

    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return (
            jsonify({"error": "Forge malfunction", "message": "An error occurred during upload"}),
            500,
        )


@bp.route("/validate", methods=["POST"])
def validate_upload():
    """
    Pre-validate file before upload (check size, type, etc.)
    """
    try:
        filename = request.json.get("filename", "")
        filesize = request.json.get("size", 0)

        if not filename:
            return jsonify({"valid": False, "message": "Filename required"}), 400

        if not allowed_file(filename):
            return (
                jsonify(
                    {
                        "valid": False,
                        "message": f'File type not allowed. Accepted: {", ".join(ALLOWED_EXTENSIONS)}',
                    }
                ),
                400,
            )

        max_size = app.config["MAX_CONTENT_LENGTH"]
        if filesize > max_size:
            return (
                jsonify(
                    {
                        "valid": False,
                        "message": f"File too large. Maximum: {max_size / (1024*1024):.0f}MB",
                    }
                ),
                400,
            )

        return jsonify({"valid": True, "message": "The artifact is worthy of the forge"}), 200

    except Exception as e:
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        return jsonify({"valid": False, "message": "Validation failed"}), 500
