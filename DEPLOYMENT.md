# 🚀 Deployment Guide - Spectral Clip Forge

This guide covers deploying Spectral Clip Forge to various platforms.

---

## 📋 Pre-Deployment Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Configure proper database (PostgreSQL for production)
- [ ] Set up Redis instance
- [ ] Configure file storage (local or S3)
- [ ] Enable ClamAV for malware scanning (recommended)
- [ ] Set appropriate rate limits
- [ ] Configure CORS for your domain
- [ ] Review and set all environment variables
- [ ] Create watermark image
- [ ] Test locally first

---

## 🐋 Docker Compose (Recommended for VPS)

Perfect for DigitalOcean Droplets, AWS EC2, or any VPS.

### Setup

```bash
# On your server
git clone https://github.com/Spectral-Flow/Spectral-Clip-Forge.git
cd Spectral-Clip-Forge

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Add to .env as SECRET_KEY

# Launch
docker-compose up -d

# Check logs
docker-compose logs -f

# Access at http://your-server-ip:5000
```

### Production Enhancements

Add Nginx reverse proxy:

```nginx
# /etc/nginx/sites-available/spectral-forge
server {
    listen 80;
    server_name forge.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Upload size
        client_max_body_size 500M;
    }
}
```

Enable SSL with Let's Encrypt:

```bash
sudo certbot --nginx -d forge.yourdomain.com
```

---

## ☁️ Heroku

### Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create spectral-clip-forge

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production
heroku config:set MAX_UPLOAD_SIZE=524288000

# Deploy
git push heroku main

# Scale workers
heroku ps:scale web=1 worker=1

# View logs
heroku logs --tail
```

### Procfile

Already included:

```
web: python app.py
worker: celery -A celery_worker.celery worker --loglevel=info
```

---

## 🚂 Railway

### Deploy

1. Visit [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your forked Spectral-Clip-Forge repo
4. Add Redis service: "New" → "Database" → "Redis"
5. Set environment variables in Railway dashboard:
   - `SECRET_KEY`: Generate random string
   - `REDIS_URL`: Automatically set by Railway
   - `FLASK_ENV`: production
6. Deploy!

### railway.json

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🌊 Render

### Deploy

1. Visit [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: spectral-clip-forge
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Add Redis: "New" → "Redis"
6. Set environment variables:
   - `SECRET_KEY`: Generate random
   - `REDIS_URL`: Copy from Redis instance
   - `FLASK_ENV`: production
7. Create!

### render.yaml

```yaml
services:
  - type: web
    name: spectral-forge-web
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: REDIS_URL
        fromService:
          type: redis
          name: spectral-forge-redis
          property: connectionString
          
  - type: worker
    name: spectral-forge-worker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: celery -A celery_worker.celery worker --loglevel=info
    envVars:
      - key: REDIS_URL
        fromService:
          type: redis
          name: spectral-forge-redis
          property: connectionString
          
  - type: redis
    name: spectral-forge-redis
    plan: starter
```

---

## ☁️ AWS (Elastic Beanstalk)

### Deploy

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 spectral-clip-forge

# Create environment
eb create spectral-forge-env

# Set environment variables
eb setenv SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
eb setenv FLASK_ENV=production

# Deploy
eb deploy

# View logs
eb logs
```

### .ebextensions/01_packages.config

```yaml
packages:
  yum:
    ffmpeg: []
    libmagic: []
```

---

## 🔵 DigitalOcean App Platform

### Deploy

1. Visit [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect GitHub repo
4. Configure:
   - **Name**: spectral-clip-forge
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python app.py`
5. Add Redis component
6. Set environment variables
7. Deploy!

---

## 🌐 Google Cloud Run

### Deploy

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT-ID/spectral-forge

# Deploy
gcloud run deploy spectral-forge \
  --image gcr.io/PROJECT-ID/spectral-forge \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=your-secret-key

# Add Redis (use Cloud Memorystore)
```

---

## 📊 Production Configuration

### Environment Variables

Essential for production:

```bash
# Security
SECRET_KEY=<strong-random-key>
FLASK_ENV=production

# Database (use PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379/0

# Uploads
MAX_UPLOAD_SIZE=524288000  # 500MB
UPLOAD_FOLDER=/app/uploads
OUTPUT_FOLDER=/app/output

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100

# Security
CLAMAV_ENABLED=true
CLAMAV_HOST=clamav
CLAMAV_PORT=3310

# CORS
CORS_ORIGINS=https://yourdomain.com
```

### Database Migration to PostgreSQL

```python
# In .env
DATABASE_URL=postgresql://user:password@host:5432/spectral_forge

# Install psycopg2
pip install psycopg2-binary

# Migrate (automatic on startup)
python app.py
```

### File Storage

For production, consider using S3 or similar:

```python
# Add to requirements.txt
boto3

# Configure in app.py
import boto3
s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
```

---

## 🔧 Maintenance

### Backup Database

```bash
# Docker
docker-compose exec web python -c "from app import db; db.create_all()"

# Export
docker-compose exec db pg_dump -U user dbname > backup.sql
```

### Clean Old Files

Set up a cron job:

```bash
# Clean files older than 24 hours
0 2 * * * docker-compose exec web python -c "from utils.file_utils import cleanup_old_files; cleanup_old_files('uploads', 24); cleanup_old_files('output', 24)"
```

### Monitor Resources

```bash
# CPU/Memory
docker stats

# Disk usage
df -h

# Redis queue size
docker-compose exec redis redis-cli LLEN celery
```

### Update Deployment

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

---

## 🚨 Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs web

# Verify environment
docker-compose exec web env | grep SECRET_KEY

# Check database connection
docker-compose exec web python -c "from app import db; db.create_all()"
```

### Worker not processing jobs

```bash
# Check worker logs
docker-compose logs worker

# Verify Redis connection
docker-compose exec redis redis-cli PING

# Check queue
docker-compose exec worker celery -A celery_worker.celery inspect active
```

### Upload failing

```bash
# Check upload directory permissions
docker-compose exec web ls -la /app/uploads

# Verify FFmpeg installation
docker-compose exec web ffmpeg -version

# Check file size limits
docker-compose exec web python -c "from app import app; print(app.config['MAX_CONTENT_LENGTH'])"
```

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale workers
docker-compose up -d --scale worker=3

# Scale web instances (behind load balancer)
docker-compose up -d --scale web=2
```

### Load Balancing

Use Nginx, HAProxy, or cloud load balancers to distribute traffic across multiple web instances.

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
```

---

## 🛡️ Security Hardening

1. **Use HTTPS only** (Let's Encrypt or cloud provider SSL)
2. **Set secure headers** (add Flask-Talisman)
3. **Enable ClamAV** for malware scanning
4. **Rate limit aggressively** for public deployments
5. **Regular backups** of database and files
6. **Monitor logs** for suspicious activity
7. **Update dependencies** regularly
8. **Use secrets manager** for sensitive config (AWS Secrets Manager, etc.)

---

## 📞 Support

Need help deploying? 
- 📖 Check the [README](README.md)
- 🐛 Open an [Issue](https://github.com/Spectral-Flow/Spectral-Clip-Forge/issues)
- 💬 Join our Discord (link in README)

---

May your deployment be swift and your forge burn eternal! 🔥⚡
