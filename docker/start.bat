@echo off
REM Quick Start Script for Quantum LMS with Docker (Windows)

echo ========================================
echo   Quantum LMS - Docker Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Navigate to docker folder
cd /d "%~dp0"

echo Starting Docker containers...
echo This may take 5-10 minutes on first run (downloading and building image)
echo.
echo All dependencies will be installed automatically:
echo   - Python 3.12
echo   - FFmpeg 8.0+
echo   - Manim CE 0.20.1
echo   - LaTeX (texlive)
echo   - All pip packages
echo.

docker-compose up --build

echo.
echo ========================================
echo   Quantum LMS stopped
echo ========================================
pause
