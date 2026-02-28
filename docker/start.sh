#!/bin/bash
# Quick Start Script for Quantum LMS with Docker (Linux/Mac)

set -e

echo "========================================"
echo "  Quantum LMS - Docker Quick Start"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker ps >/dev/null 2>&1; then
    echo "[ERROR] Docker is not running!"
    echo "Please start Docker daemon and try again."
    echo ""
    echo "Ubuntu/Debian: sudo systemctl start docker"
    echo "macOS: Open Docker Desktop application"
    exit 1
fi

echo "[OK] Docker is running"
echo ""

# Navigate to docker folder
cd "$(dirname "$0")"

echo "Starting Docker containers..."
echo "This may take 5-10 minutes on first run (downloading and building image)"
echo ""
echo "All dependencies will be installed automatically:"
echo "  - Python 3.12"
echo "  - FFmpeg 8.0+"
echo "  - Manim CE 0.20.1"
echo "  - LaTeX (texlive)"
echo "  - All pip packages"
echo ""

docker-compose up --build

echo ""
echo "========================================"
echo "  Quantum LMS stopped"
echo "========================================"
