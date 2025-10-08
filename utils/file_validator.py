"""
File Validation Utilities
Ensuring only worthy artifacts enter the forge
"""
import os
import magic
import logging

logger = logging.getLogger(__name__)

# Valid MIME types for media files
VALID_MIME_TYPES = {
    "video": [
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-matroska",
        "video/mpeg",
        "video/webm",
    ],
    "audio": [
        "audio/mpeg",
        "audio/mp4",
        "audio/x-wav",
        "audio/wav",
        "audio/flac",
        "audio/x-flac",
        "audio/aac",
        "audio/ogg",
    ],
}


def validate_file(filepath, expected_ext):
    """
    Validate that a file is actually a valid media file

    Args:
        filepath: Path to file to validate
        expected_ext: Expected file extension

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            return False, "File not found"

        # Check file size (minimum 1KB to avoid empty files)
        file_size = os.path.getsize(filepath)
        if file_size < 1024:
            return False, "File is too small or empty"

        # Check MIME type using python-magic
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(filepath)

        # Determine if it's audio or video
        all_valid_mimes = VALID_MIME_TYPES["video"] + VALID_MIME_TYPES["audio"]

        if file_mime not in all_valid_mimes:
            logger.warning(f"Invalid MIME type: {file_mime} for file {filepath}")
            return False, f"Invalid media file. Detected type: {file_mime}"

        # Additional validation could include:
        # - FFprobe to check if file is actually playable
        # - Duration check
        # - Codec validation

        return True, None

    except Exception as e:
        logger.error(f"File validation error: {str(e)}", exc_info=True)
        return False, f"Validation error: {str(e)}"


def scan_for_malware(filepath):
    """
    Scan file for malware using ClamAV

    Args:
        filepath: Path to file to scan

    Returns:
        tuple: (is_safe, error_message)
    """
    try:
        import clamd

        # Connect to ClamAV daemon
        clamav_host = os.getenv("CLAMAV_HOST", "localhost")
        clamav_port = int(os.getenv("CLAMAV_PORT", 3310))

        cd = clamd.ClamdNetworkSocket(host=clamav_host, port=clamav_port)

        # Scan file
        scan_result = cd.scan(filepath)

        if scan_result is None:
            # File is clean
            return True, None

        # File is infected
        logger.warning(f"Malware detected in {filepath}: {scan_result}")
        return False, "Malware detected"

    except clamd.ConnectionError:
        logger.warning("ClamAV not available, skipping malware scan")
        # If ClamAV is not available, allow the file but log it
        return True, None

    except Exception as e:
        logger.error(f"Malware scan error: {str(e)}", exc_info=True)
        # On error, be conservative and reject
        return False, f"Scan error: {str(e)}"
