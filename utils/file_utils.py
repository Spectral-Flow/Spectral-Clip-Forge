"""
File Utilities
Helper functions for file operations
"""
import os
import json
import logging

logger = logging.getLogger(__name__)


def get_file_info(filepath):
    """
    Get information about a file

    Args:
        filepath: Path to file

    Returns:
        dict: File information
    """
    try:
        stat = os.stat(filepath)

        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": os.path.splitext(filepath)[1].lower(),
        }

    except Exception as e:
        logger.error(f"Error getting file info: {str(e)}", exc_info=True)
        return {"size": 0, "created": None, "modified": None, "extension": None}


def ensure_directory(directory):
    """
    Ensure a directory exists, create if not

    Args:
        directory: Directory path
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}", exc_info=True)
        return False


def cleanup_old_files(directory, max_age_hours=24):
    """
    Clean up old files from a directory

    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files in hours
    """
    import time

    try:
        now = time.time()
        max_age_seconds = max_age_hours * 3600

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                file_age = now - os.path.getmtime(filepath)

                if file_age > max_age_seconds:
                    try:
                        os.remove(filepath)
                        logger.info(f"Cleaned up old file: {filename}")
                    except Exception as e:
                        logger.error(f"Error removing file {filename}: {str(e)}")

        return True

    except Exception as e:
        logger.error(f"Error cleaning directory {directory}: {str(e)}", exc_info=True)
        return False
