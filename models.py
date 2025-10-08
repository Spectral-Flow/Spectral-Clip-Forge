"""
Database Models for Spectral Clip Forge
Storing the legends of media transformations
"""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model):
    """User model for authentication and tracking"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    oauth_provider = db.Column(db.String(50))  # 'github', 'google', or None
    oauth_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    jobs = db.relationship('Job', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Job(db.Model):
    """Processing job model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='pending', index=True)
    # Status: pending, processing, completed, failed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Processing configuration
    target_formats = db.Column(db.Text)  # JSON list: ['tiktok', 'shorts', 'reels']
    options = db.Column(db.Text)  # JSON: watermark, effects, subtitles, etc.
    
    # Results
    output_files = db.Column(db.Text)  # JSON list of generated files
    error_message = db.Column(db.Text)
    
    # Stats
    processing_time = db.Column(db.Float)  # seconds
    
    def set_target_formats(self, formats):
        """Set target formats as JSON"""
        self.target_formats = json.dumps(formats)
    
    def get_target_formats(self):
        """Get target formats from JSON"""
        return json.loads(self.target_formats) if self.target_formats else []
    
    def set_options(self, options):
        """Set options as JSON"""
        self.options = json.dumps(options)
    
    def get_options(self):
        """Get options from JSON"""
        return json.loads(self.options) if self.options else {}
    
    def set_output_files(self, files):
        """Set output files as JSON"""
        self.output_files = json.dumps(files)
    
    def get_output_files(self):
        """Get output files from JSON"""
        return json.loads(self.output_files) if self.output_files else []
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'target_formats': self.get_target_formats(),
            'options': self.get_options(),
            'output_files': self.get_output_files(),
            'error_message': self.error_message,
            'processing_time': self.processing_time
        }

class AuditLog(db.Model):
    """Audit log for security and compliance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    details = db.Column(db.Text)  # JSON
    
    @staticmethod
    def log_action(action, user_id=None, details=None, ip_address=None, user_agent=None):
        """Create an audit log entry"""
        log = AuditLog(
            action=action,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=json.dumps(details) if details else None
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def get_details(self):
        """Get details from JSON"""
        return json.loads(self.details) if self.details else {}
