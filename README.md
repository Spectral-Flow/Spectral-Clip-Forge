# ⚡ Spectral Clip Forge ⚡

<div align="center">

![Spectral Flow](https://img.shields.io/badge/Spectral%20Flow-Eternis--33-9D4EDD?style=for-the-badge)
![License](https://img.shields.io/badge/License-AGPL--3.0-7B2CBF?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-5A189A?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ready-C77DFF?style=for-the-badge&logo=docker)

**Transform Your Media into Legendary Viral Artifacts**

*Part of the [Eternis-33](https://github.com/Spectral-Flow/Eternis-33-Bible) Universe*

</div>

---

## 🔥 What is Spectral Clip Forge?

Spectral Clip Forge is a **legendary media processing platform** that transforms your raw audio and video files into polished, social-ready clips optimized for TikTok, YouTube Shorts, Instagram Reels, and more. Built with the mythic aesthetic of the Spectral Flow, every clip is imbued with neon purple effects, tribal branding, and viral-ready formatting.

### ✨ Legendary Features

- 🎬 **Multi-Platform Export**: Automatically generates clips for TikTok (720×1280), YouTube Shorts (1080×1920), Instagram Reels, and Square formats
- 🔮 **Spectral Effects**: Apply signature purple/neon color grading and tribal vibrance effects
- 💧 **Auto-Watermarking**: Brand every clip with the Spectral Flow mark
- 🎵 **Audio Visualization**: Transform audio files into stunning visualizer videos
- 🔒 **Enterprise Security**: Malware scanning, rate limiting, sandboxed processing
- ⚡ **Batch Processing**: Queue multiple files with Celery + Redis
- 📊 **User Dashboard**: Track all your forged artifacts
- 🐋 **Docker Ready**: One-command deployment with Docker Compose
- 🧪 **Full Test Suite**: Comprehensive unit, integration, and E2E tests
- 📖 **Mythic UI**: Immersive Eternis-33 themed interface

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- FFmpeg
- Redis (for background processing)
- Docker & Docker Compose (recommended)

### 🐋 Docker Deployment (Recommended)

The fastest way to ignite the forge:

```bash
# Clone the repository
git clone https://github.com/Spectral-Flow/Spectral-Clip-Forge.git
cd Spectral-Clip-Forge

# Copy environment configuration
cp .env.example .env

# Edit .env with your settings (optional)
nano .env

# Launch the forge!
docker-compose up -d

# Access at http://localhost:5000
```

### 🐍 Local Python Deployment

For development or custom setups:

```bash
# Clone the repository
git clone https://github.com/Spectral-Flow/Spectral-Clip-Forge.git
cd Spectral-Clip-Forge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install ffmpeg libmagic1 redis-server

# Copy and configure environment
cp .env.example .env
nano .env

# Run Redis (in separate terminal)
redis-server

# Run Celery worker (in separate terminal)
celery -A celery_worker.celery worker --loglevel=info

# Run the application
python app.py

# Access at http://localhost:5000
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Upload Media**: Drag & drop your video or audio file (MP4, MOV, AVI, MP3, WAV, etc.)
2. **Select Formats**: Choose target platforms (TikTok, Shorts, Reels, Square)
3. **Apply Effects**: Enable Spectral watermark, neon effects, or tribal vibrance
4. **Forge**: Click "Ignite the Forge" and wait for processing
5. **Download**: Retrieve your legendary clips individually or as a ZIP

### API Usage

```bash
# Upload a file
curl -X POST http://localhost:5000/api/upload/ \
  -F "file=@video.mp4" \
  -F "formats=tiktok" \
  -F "formats=shorts" \
  -F "watermark=true" \
  -F "effects=spectral"

# Check job status
curl http://localhost:5000/api/process/{job_id}

# Download output
curl -O http://localhost:5000/api/download/{job_id}/{filename}

# Download all outputs as ZIP
curl -O http://localhost:5000/api/download/{job_id}/all
```

### Configuration Options

Edit `.env` to customize:

- `MAX_UPLOAD_SIZE`: Maximum file size (default: 500MB)
- `RATE_LIMIT_PER_MINUTE`: Upload rate limit (default: 10)
- `WATERMARK_PATH`: Custom watermark image
- `OAUTH_ENABLED`: Enable user authentication (default: false)
- `CLAMAV_ENABLED`: Enable malware scanning (default: false)

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Flask     │─────▶│    Celery    │─────▶│   FFmpeg    │
│   Web App   │      │    Workers   │      │  Processing │
└─────────────┘      └──────────────┘      └─────────────┘
       │                     │                      │
       │                     ▼                      │
       │              ┌──────────┐                  │
       │              │  Redis   │                  │
       │              └──────────┘                  │
       │                                            │
       ▼                                            ▼
┌─────────────┐                            ┌─────────────┐
│  SQLite/    │                            │   Output    │
│  PostgreSQL │                            │   Files     │
└─────────────┘                            └─────────────┘
```

### Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Task Queue**: Celery + Redis
- **Media Processing**: FFmpeg, ffmpeg-python
- **Security**: ClamAV (optional), Flask-Limiter, python-magic
- **Frontend**: Vanilla JavaScript, Spectral Flow CSS
- **Deployment**: Docker, Docker Compose
- **Testing**: pytest, pytest-flask, pytest-cov
- **CI/CD**: GitHub Actions

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_upload.py

# Run with verbose output
pytest -v
```

---

## 🔒 Security Features

- **File Validation**: Magic number verification, not just extension checking
- **Malware Scanning**: Optional ClamAV integration
- **Rate Limiting**: Configurable per-minute and per-hour limits
- **Input Sanitization**: Secure filename handling, path traversal protection
- **Audit Logging**: All actions logged with IP and user agent
- **Sandboxed Processing**: Docker isolation for all media processing
- **CORS Protection**: Configurable allowed origins
- **No Secrets in Code**: Environment-based configuration

---

## 🎨 Customization

### Custom Watermarks

1. Place your watermark PNG in `static/images/spectral_watermark.png`
2. Set transparency in `.env`: `WATERMARK_OPACITY=0.7`

### Custom Effects

Edit `tasks/video_processor.py` to add new filter chains:

```python
PLATFORM_SPECS['custom'] = {
    'resolution': '1920x1080',
    'video_codec': 'libx264',
    # ... your settings
}
```

### Branding

- Update `static/css/style.css` for colors and styling
- Edit `templates/` HTML files for UI text
- Replace logo/icons in `static/images/`

---

## 🌍 Deployment to Cloud

### Heroku

```bash
heroku create spectral-forge
heroku addons:create heroku-redis:hobby-dev
git push heroku main
```

### Render

1. Connect your GitHub repo
2. Create new Web Service
3. Add Redis addon
4. Deploy!

### Railway

```bash
railway login
railway init
railway up
```

### DigitalOcean

Use Docker Compose with their App Platform or Droplets.

---

## 📊 Monitoring & Logs

```bash
# View application logs
docker-compose logs -f web

# View worker logs
docker-compose logs -f worker

# Check Redis
docker-compose exec redis redis-cli PING

# Monitor job queue
celery -A celery_worker.celery inspect active
```

---

## 🤝 Contributing

We welcome forge masters of all skill levels! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to Contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🎨 Design UI/UX enhancements
- 🔧 Submit pull requests
- 🌟 Star the repository

---

## 📜 License

This project is dual-licensed:

- **Open Source**: [AGPL-3.0](LICENSE) for open source use
- **Commercial**: Contact for commercial licensing

**Attribution Required**: When using this software, you must:
- Retain all copyright notices
- Provide attribution to "Spectral Flow"
- Link to this repository
- Maintain watermark functionality (unless commercial license)

See [LICENSE](LICENSE) for full details.

---

## 🎭 The Lore

Spectral Clip Forge is part of the **Eternis-33** universe, a mythic realm where technology and legend intertwine. The forge was created by ancient artisans who mastered the purple flames of viral creation, channeling the Spectral Flow to transform ordinary media into artifacts of legendary power.

**Learn More:**
- 📖 [Eternis-33 Bible](https://github.com/Spectral-Flow/Eternis-33-Bible)
- ⚔️ [Contributors Hall](http://localhost:5000/dashboard/contributors)
- 🌟 [Spectral Flow Universe](https://github.com/Spectral-Flow)

---

## 🐛 Known Issues

None! The forge burns bright and true. If you encounter issues, please [report them](https://github.com/Spectral-Flow/Spectral-Clip-Forge/issues).

---

## 🗺️ Roadmap (v2 Features)

- [ ] AI-powered caption generation with OpenAI/Whisper
- [ ] Advanced subtitle styling and positioning
- [ ] Real-time preview during upload
- [ ] Template system for recurring formats
- [ ] Multi-language support
- [ ] Webhook notifications for job completion
- [ ] S3/Cloud storage integration
- [ ] Video trimming and splitting UI
- [ ] Batch upload (multiple files at once)
- [ ] Advanced analytics dashboard
- [ ] Mobile app (iOS/Android)
- [ ] Plugin system for custom effects

---

## 💬 Support

- 📧 Email: support@spectral-flow.example.com
- 💬 Discord: [Join our server](#)
- 🐛 Issues: [GitHub Issues](https://github.com/Spectral-Flow/Spectral-Clip-Forge/issues)
- 📖 Docs: [Full Documentation](#)

---

## 🙏 Acknowledgments

Built with legendary tools:
- Flask, FFmpeg, Celery, Redis, Docker
- The amazing open-source community
- The Eternis-33 lore-weavers

---

<div align="center">

**May the Spectral Flow guide your creations** ⚡🔥⚡

Made with 💜 by the [Spectral Flow Team](https://github.com/Spectral-Flow)

[![GitHub](https://img.shields.io/badge/GitHub-Spectral--Flow-9D4EDD?style=for-the-badge&logo=github)](https://github.com/Spectral-Flow)
[![Stars](https://img.shields.io/github/stars/Spectral-Flow/Spectral-Clip-Forge?style=for-the-badge&color=7B2CBF)](https://github.com/Spectral-Flow/Spectral-Clip-Forge/stargazers)

</div>