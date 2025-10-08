"""
Test Database Models
"""
import pytest
from models import User, Job, AuditLog
from app import db

def test_user_creation(client):
    """Test user model creation"""
    with client.application.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.check_password('testpassword')
        assert not user.check_password('wrongpassword')

def test_job_creation(client):
    """Test job model creation"""
    with client.application.app_context():
        job = Job(
            id='test-job-123',
            filename='test.mp4',
            file_size=1024000,
            file_type='mp4'
        )
        job.set_target_formats(['tiktok', 'shorts'])
        job.set_options({'watermark': True, 'effects': 'spectral'})
        db.session.add(job)
        db.session.commit()
        
        assert job.id == 'test-job-123'
        assert job.get_target_formats() == ['tiktok', 'shorts']
        assert job.get_options()['watermark'] is True

def test_audit_log_creation(client):
    """Test audit log creation"""
    with client.application.app_context():
        log = AuditLog.log_action(
            action='test_action',
            details={'test': 'data'}
        )
        
        assert log.id is not None
        assert log.action == 'test_action'
        assert log.get_details()['test'] == 'data'
