#!/bin/bash
# Quick start script for Spectral Clip Forge

set -e

echo "🔥 Spectral Clip Forge - Quick Start 🔥"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env with generated secret
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
    else
        sed -i "s/change-this-to-a-random-secret-key-in-production/$SECRET_KEY/" .env
    fi
    
    echo "✅ .env file created with random SECRET_KEY"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads output logs static/images

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo ""
    echo "🐋 Docker detected! Starting with Docker Compose..."
    echo ""
    docker-compose up -d
    echo ""
    echo "✨ Spectral Clip Forge is now running! ✨"
    echo "🌐 Access at: http://localhost:5000"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
else
    echo ""
    echo "⚠️  Docker not found. Using local Python setup..."
    echo ""
    
    # Check if Python venv exists
    if [ ! -d "venv" ]; then
        echo "🐍 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv and install dependencies
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt > /dev/null 2>&1
    
    echo ""
    echo "⚠️  Note: You need Redis running for background processing"
    echo "   Install Redis: sudo apt-get install redis-server (Ubuntu/Debian)"
    echo "   Or: brew install redis (macOS)"
    echo ""
    echo "🚀 Starting Spectral Clip Forge..."
    echo "   Web app: python app.py"
    echo "   Worker: celery -A celery_worker.celery worker --loglevel=info"
    echo ""
    echo "Run 'python app.py' to start the server"
fi
