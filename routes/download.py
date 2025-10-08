"""
Download Route Blueprint
Retrieve the legendary artifacts forged from media
"""
from flask import Blueprint, send_file, jsonify, request
from app import app, db, limiter, logger
from models import Job, AuditLog
import os

bp = Blueprint('download', __name__, url_prefix='/api/download')

@bp.route('/<job_id>/<filename>', methods=['GET'])
@limiter.limit("20/minute")
def download_file(job_id, filename):
    """
    Download a processed file
    Claim your forged artifact
    """
    try:
        # Verify job exists
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({
                'error': 'Lost artifact',
                'message': 'Job not found'
            }), 404
        
        if job.status != 'completed':
            return jsonify({
                'error': 'Artifact not ready',
                'message': f'Job status: {job.status}'
            }), 400
        
        # Verify file exists in job outputs
        output_files = job.get_output_files()
        if filename not in output_files:
            return jsonify({
                'error': 'Artifact not found',
                'message': 'File not in job outputs'
            }), 404
        
        # Build file path
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], job_id, filename)
        
        if not os.path.exists(filepath):
            logger.error(f"Output file missing: {filepath}")
            return jsonify({
                'error': 'Artifact vanished',
                'message': 'File not found on server'
            }), 404
        
        # Log download
        AuditLog.log_action('file_download', details={
            'job_id': job_id,
            'filename': filename
        })
        
        logger.info(f"File downloaded: {filename} from job {job_id}")
        
        # Send file
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Retrieval failed',
            'message': 'Could not download file'
        }), 500

@bp.route('/<job_id>/all', methods=['GET'])
@limiter.limit("10/minute")
def download_all(job_id):
    """
    Download all files from a job as a zip archive
    Claim the complete collection of forged artifacts
    """
    try:
        import zipfile
        import io
        
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({
                'error': 'Lost artifact',
                'message': 'Job not found'
            }), 404
        
        if job.status != 'completed':
            return jsonify({
                'error': 'Artifacts not ready',
                'message': f'Job status: {job.status}'
            }), 400
        
        output_files = job.get_output_files()
        if not output_files:
            return jsonify({
                'error': 'No artifacts',
                'message': 'No output files available'
            }), 404
        
        # Create zip file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in output_files:
                filepath = os.path.join(app.config['OUTPUT_FOLDER'], job_id, filename)
                if os.path.exists(filepath):
                    zf.write(filepath, filename)
        
        memory_file.seek(0)
        
        # Log download
        AuditLog.log_action('batch_download', details={
            'job_id': job_id,
            'file_count': len(output_files)
        })
        
        logger.info(f"Batch download: {len(output_files)} files from job {job_id}")
        
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f'spectral_forge_{job_id}.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Batch download error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Collection failed',
            'message': 'Could not create archive'
        }), 500
