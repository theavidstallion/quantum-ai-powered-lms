# Quantum LMS - Quick Start Guide

**For experienced developers who want to get running in 5 minutes.**

## TL;DR

```bash
# Clone and setup
git clone <repo-url>
cd quantum-lms
python -m venv venv
venv\Scripts\activate  # Windows | source venv/bin/activate (Linux/Mac)

# Install dependencies
pip install -r requirements.txt
choco install ffmpeg  # Windows | apt install ffmpeg (Linux) | brew install ffmpeg (Mac)

# Configure
copy .env.example .env
# Edit .env - Add your Groq API key from: https://console.groq.com/keys

# Run
python app.py
# Open http://127.0.0.1:5000
# Login: admin / admin123
```

## Critical Notes

### 1. Flask Auto-Reload is Disabled
```python
# In app.py - DO NOT change this
app.run(debug=True, use_reloader=False)
```
**Why**: Flask's watchdog kills Manim subprocess during video generation.  
**Impact**: You must manually restart Flask after code changes (Ctrl+C → python app.py).

### 2. Manim Must Be Installed
```bash
pip install manim
manim --version  # Verify: Manim Community v0.18.0+
```
**Why**: Required for AI video generation feature.  
**Test**: `python test_manim.py` (should complete in 10-30 seconds)

### 3. FFmpeg is a System Dependency
```bash
ffmpeg -version  # Must return version 4.4+
```
**Why**: Required for video/audio merging in AI video generator.  
**Install**: See Step 4 in [README Installation Guide](README.md#step-4-install-ffmpeg-video-generation)

### 4. Groq API Key is Free
- Get it from: https://console.groq.com/keys
- No credit card required
- Free tier: 30 req/min, 14.4K req/day
- Add to `.env` as: `GROQ_API_KEY=gsk_...`

## Architecture Overview

```
┌───────────────────────────────────────────────────┐
│ Frontend (HTML/JS/CSS)                            │
│ • Dashboard, Admin Panel, Login                   │
└───────────────────────────────────────────────────┘
                      ↓
┌───────────────────────────────────────────────────┐
│ Flask Backend (app.py)                            │
│ • Routes, Session Management, DB Operations       │
└───────────────────────────────────────────────────┘
                      ↓
┌──────────────┬──────────────┬──────────────┬──────┐
│ bb84.py      │ chatbot.py   │ video_gen.py │ ...  │
│ Quantum Keys │ LangChain    │ Manim+Groq   │ More │
└──────────────┴──────────────┴──────────────┴──────┘
                      ↓
┌───────────────────────────────────────────────────┐
│ SQLite Database (users.db)                        │
│ • 7 tables: users, grades, feedback, rankings,    │
│   login_attempts, anomaly_alerts, video_requests  │
└───────────────────────────────────────────────────┘
```

## Key Features

| Feature | Tech Stack | Purpose |
|---------|------------|---------|
| **3-Factor Auth** | OpenCV + BB84 + Passwords | Face + Quantum Key + Credentials |
| **AI Chatbot** | LangChain + Groq LLaMA 3.1 | Student academic assistant |
| **Video Generator** | Manim + Groq LLaMA 3.3 + gTTS | Auto-generate educational videos |
| **Anomaly Detection** | scikit-learn Isolation Forest | Detect suspicious logins |
| **Sentiment Analysis** | Lexicon-based NLP | Analyze teacher feedback |
| **Student Ranking** | Custom algorithm | 70% academic + 30% sentiment |

## File Structure

```
Quantum-/
├── app.py                      # Main Flask application
├── video_generator.py          # AI video generation module
├── chatbot.py                  # LangChain chatbot
├── bb84.py                     # Quantum key distribution
├── anomaly_detector.py         # ML security monitoring
├── sentiment_analyzer.py       # NLP feedback analysis
├── test_manim.py              # Manim diagnostic tool
├── restart_clean.py           # Recovery script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from .env.example)
├── users.db                   # SQLite database (auto-created)
├── templates/                 # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   └── admin_panel.html
├── static/                    # CSS/JS assets
│   ├── css/
│   └── js/
└── output/videos/            # Generated videos storage
```

## API Endpoints

### Authentication
- `POST /login` - Face + credentials verification
- `POST /quantum_verify` - BB84 quantum key check
- `GET /logout` - Session termination

### Dashboard
- `GET /dashboard` - Student interface
- `GET /admin` - Admin panel
- `POST /chatbot` - AI chatbot messages

### Video Generation
- `POST /request_video` - Create video request
- `GET /my_videos` - List user's videos
- `GET /all_video_requests` - Admin: all requests
- `GET /download_video/<id>` - Download completed video

### Analytics
- `GET /student_rankings` - Fetch ranking data
- `GET /security_alerts` - Admin: anomaly alerts

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Video hangs forever | Flask auto-reload killed Manim - restart Flask |
| "Manim not found" | `pip install manim` then `manim --version` |
| Only MP3, no video | Run `python test_manim.py` - Manim likely not working |
| "FFmpeg not found" | Install FFmpeg system-wide, add to PATH |
| Chatbot empty response | Check `GROQ_API_KEY` in `.env` |
| "No module named cv2" | Virtual environment not activated |
| Webcam not detected | Browser permissions + close other apps |
| Database locked | Stop Flask, ensure only one instance running |

## Development Workflow

```bash
# 1. Make code changes
# 2. Stop Flask (Ctrl+C)
# 3. Restart Flask
python app.py
# 4. Test in browser
# 5. Repeat
```

**Note**: Flask auto-reload is disabled, so manual restart is required.

## Video Generation Timeline

Expected duration for AI video generation:

1. **Audio generation**: 5-10 seconds ✓
2. **Manim code generation**: 10-20 seconds
3. **Manim rendering**: 30 seconds - 2 minutes (varies by complexity)
4. **FFmpeg merge**: 5-10 seconds

**Total**: 1-3 minutes for simple topics, up to 5 minutes for complex math/physics.

**If takes longer**: Likely hung - check troubleshooting section.

## Production Deployment

### Security Hardening
```python
# MUST DO before production:
1. Change all default passwords
2. Set strong SECRET_KEY in .env
3. Enable HTTPS
4. Set up proper user authentication
5. Configure database backups
6. Set rate limiting on API endpoints
```

### Scaling Considerations
- SQLite → PostgreSQL for >1000 users
- Add Redis for session storage
- Use Celery for background video generation
- Deploy with Gunicorn + Nginx
- Set up CDN for video file delivery

## Useful Commands

```bash
# Kill stuck processes
taskkill /F /IM python.exe  # Windows
pkill -9 python             # Linux/Mac

# Reset database
del users.db; python app.py  # Windows
rm users.db && python app.py # Linux/Mac

# Test components individually
python -c "import cv2; print(cv2.__version__)"           # OpenCV
python -c "from groq import Groq; print('Groq OK')"     # Groq
python test_manim.py                                     # Manim
ffmpeg -version                                          # FFmpeg

# Check what's installed
pip list
pip show flask opencv-python manim groq langchain

# Upgrade all packages
pip install -r requirements.txt --upgrade
```

## Resources

- **Full Documentation**: [README.md](README.md)
- **Video Generator Guide**: [VIDEO_GENERATOR_GUIDE.md](VIDEO_GENERATOR_GUIDE.md)
- **How It Works**: [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
- **Groq API Docs**: https://console.groq.com/docs
- **Manim Docs**: https://docs.manim.community
- **LangChain Docs**: https://python.langchain.com

## Support

If stuck after following this guide:
1. Check [README.md Troubleshooting](README.md#troubleshooting)
2. Run `python test_manim.py` for diagnostics
3. Verify all checklist items in [README Pre-Flight Checklist](README.md#pre-flight-checklist)
4. Check console output for error messages

---

**Built for rapid deployment. Questions? See full [README.md](README.md)**
