"""
System Utilities
System stats and monitoring
"""
import os
import psutil
import logging

logger = logging.getLogger(__name__)

def get_system_stats():
    """
    Get current system statistics
    
    Returns:
        dict: System stats
    """
    try:
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'upload_count': count_files('uploads'),
            'output_count': count_files('output')
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}", exc_info=True)
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'upload_count': 0,
            'output_count': 0
        }

def count_files(directory):
    """
    Count files in a directory
    
    Args:
        directory: Directory path
        
    Returns:
        int: Number of files
    """
    try:
        if not os.path.exists(directory):
            return 0
        
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        
        return count
        
    except Exception as e:
        logger.error(f"Error counting files in {directory}: {str(e)}", exc_info=True)
        return 0
