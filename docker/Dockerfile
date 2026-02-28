# Multi-stage Docker build for Quantum LMS
# Includes: Python 3.12, FFmpeg, Manim CE, all pip dependencies

FROM python:3.12-slim-bookworm AS base

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    # FFmpeg for video processing
    ffmpeg \
    # Build tools for Python packages
    gcc \
    g++ \
    make \
    # System libraries for OpenCV and Manim
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # LaTeX for Manim (optional, for complex math)
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-science \
    dvipng \
    # Cairo for Manim rendering
    libcairo2-dev \
    pkg-config \
    # Pango for text rendering
    libpango1.0-dev \
    # Git for potential package installations
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app user (security best practice - don't run as root)
RUN useradd -m -u 1000 -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
COPY --chown=appuser:appuser ../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Verify critical installations
RUN python -c "import manim; print(f'Manim {manim.__version__}')" && \
    python -c "import cv2; print(f'OpenCV {cv2.__version__}')" && \
    ffmpeg -version | head -n 1

# Copy application code
COPY --chown=appuser:appuser .. /app/

# Create necessary directories with proper permissions
RUN mkdir -p /app/output/videos /app/output/audio /app/media && \
    chown -R appuser:appuser /app/output /app/media

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Copy and set entrypoint script
COPY --chown=appuser:appuser entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "app.py"]
