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

# Create output directories (volumes are mounted with host permissions)
echo "📁 Creating directories..."
mkdir -p /app/output/videos /app/output/audio /app/media

# Ensure database file can be created (don't fail if it already exists)
touch /app/users.db 2>/dev/null || true

# Initialize database if not exists
if [ ! -s /app/users.db ]; then
    echo "🗄️  Initializing database..."
    python -c "from app import init_db; init_db()" || echo "⚠️  Database initialization skipped (will be created on first run)"
else
    echo "✅ Database found"
fi

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
