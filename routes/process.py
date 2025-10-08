"""
Process Route Blueprint
Monitor and control the forging process
"""
from flask import Blueprint, jsonify, request
from app import db, limiter, logger
from models import Job

bp = Blueprint('process', __name__, url_prefix='/api/process')

@bp.route('/<job_id>', methods=['GET'])
@limiter.limit("30/minute")
def get_job_status(job_id):
    """
    Get the status of a processing job
    Peer into the flames to see your artifact's transformation
    """
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({
                'error': 'Lost artifact',
                'message': 'Job not found'
            }), 404
        
        return jsonify({
            'success': True,
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Status check error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Vision obscured',
            'message': 'Could not retrieve job status'
        }), 500

@bp.route('/<job_id>/cancel', methods=['POST'])
@limiter.limit("10/minute")
def cancel_job(job_id):
    """
    Cancel a processing job
    Extinguish the flames before completion
    """
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({
                'error': 'Lost artifact',
                'message': 'Job not found'
            }), 404
        
        if job.status == 'completed':
            return jsonify({
                'error': 'Artifact already forged',
                'message': 'Cannot cancel completed job'
            }), 400
        
        if job.status == 'failed':
            return jsonify({
                'error': 'Forge already cooled',
                'message': 'Job already failed'
            }), 400
        
        # Revoke Celery task
        from celery_worker import celery
        celery.control.revoke(job_id, terminate=True)
        
        # Update job status
        job.status = 'cancelled'
        db.session.commit()
        
        logger.info(f"Job {job_id} cancelled")
        
        return jsonify({
            'success': True,
            'message': 'The forging has been halted',
            'job_id': job_id
        }), 200
        
    except Exception as e:
        logger.error(f"Cancel error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Cannot extinguish',
            'message': 'Could not cancel job'
        }), 500

@bp.route('/list', methods=['GET'])
@limiter.limit("20/minute")
def list_jobs():
    """
    List recent jobs
    View the chronicles of the forge
    """
    try:
        # Get query parameters
        status = request.args.get('status')
        limit = min(int(request.args.get('limit', 50)), 100)
        
        query = Job.query.order_by(Job.created_at.desc())
        
        if status:
            query = query.filter_by(status=status)
        
        jobs = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs],
            'count': len(jobs)
        }), 200
        
    except Exception as e:
        logger.error(f"List jobs error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Chronicles lost',
            'message': 'Could not retrieve jobs'
        }), 500
