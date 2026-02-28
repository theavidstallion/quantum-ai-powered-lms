#!/bin/bash
set -e

echo "🚀 Quantum LMS Docker Container Starting..."

# Verify environment variables
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  WARNING: GROQ_API_KEY not set. Video generation will fail."
fi

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  WARNING: SECRET_KEY not set. Using default (INSECURE for production)."
fi

# Verify FFmpeg installation
echo "📹 Checking FFmpeg..."
ffmpeg -version | head -n 1 || { echo "❌ FFmpeg not found!"; exit 1; }

# Verify Manim installation
echo "🎨 Checking Manim..."
python -c "import manim; print(f'✅ Manim Community v{manim.__version__}')" || { echo "❌ Manim not found!"; exit 1; }

# Create database if not exists
if [ ! -f /app/quantum_lms.db ]; then
    echo "🗄️  Initializing database..."
    python -c "from app import init_db; init_db()" || { echo "❌ Database initialization failed!"; exit 1; }
else
    echo "✅ Database found"
fi

# Create output directories
mkdir -p /app/output/videos /app/output/audio /app/media
echo "📁 Output directories ready"

# Display startup info
echo ""
echo "═════════════════════════════════════════════════════"
echo "   🎓 QUANTUM LMS - AI-Powered Learning Platform   "
echo "═════════════════════════════════════════════════════"
echo "   🌐 Access: http://127.0.0.1:5000"
echo "   📚 Features: Chatbot, Video Generator, Analytics"
echo "   🐳 Running in Docker container"
echo "═════════════════════════════════════════════════════"
echo ""

# Execute the main command (python app.py)
exec "$@"
