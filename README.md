# 🔐 Quantum LMS - Secure Learning Management System

A next-generation Learning Management System featuring quantum-inspired security, AI-powered student analytics, and advanced anomaly detection for educational institutions.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-2.0+-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📋 Table of Contents

### Getting Started
- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [Usage Guide](#usage-guide)
- [Default User Credentials](#default-user-credentials)

### Product Documentation
- [How It Works](#how-it-works)
- [User Workflows](#user-workflows)
- [Security Features](#security-features)

### Technical Documentation
- [Technical Architecture](#technical-architecture)
- [System Components](#system-components)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)

### Additional Resources
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**Quantum LMS** is an advanced Learning Management System designed for modern educational institutions. It combines traditional LMS functionality with cutting-edge security measures including:

- **Quantum Key Distribution (BB84)** for session encryption
- **Biometric Face Verification** for login authentication
- **AI-Powered Student Ranking** with sentiment analysis
- **Machine Learning Anomaly Detection** for security threats
- **Intelligent Chatbot Assistant** powered by LangChain + Groq

The system provides separate interfaces for students and administrators, with real-time analytics, automated grading, feedback systems, and comprehensive security monitoring.

**Live Demo**: Access at `http://127.0.0.1:5000` after setup  
**Default Admin**: `admin` / `admin123`  
**Browser Support**: Chrome, Firefox, Edge (Webcam required)

---

## ⚡ Quick Start

**⚡ For experienced developers**: See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

**📚 For detailed setup**: Follow the complete guide below.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/quantum-lms.git
cd quantum-lms

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install FFmpeg (for video generation)
# Windows:
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html

# 5. Configure environment variables
copy .env.example .env  # Edit with your API keys

# 6. Run the application
python app.py

# IMPORTANT: Auto-reload is DISABLED to prevent video generation issues
# After editing code, manually restart Flask (Ctrl+C, then python app.py)

# 7. Open browser
# Navigate to: http://127.0.0.1:5000
# Login: admin / admin123
```

**That's it!** 🎉 You're ready to explore Quantum LMS.

**⚠️ Important Note**: The Flask auto-reloader is disabled (`use_reloader=False`) to prevent video generation from being interrupted. This means you need to manually restart the server after code changes.

---

## 🚀 Key Features

### 🔒 Advanced Security
- **Multi-Factor Authentication**: Face recognition + password + quantum key verification
- **BB84 Quantum Key Distribution**: Simulated quantum encryption for session security
- **Anomaly Detection**: ML-based detection of suspicious login patterns
- **Real-time Security Alerts**: Immediate notification of security threats
- **IP Tracking**: Monitor and log all access attempts

### 🤖 AI-Powered Intelligence
- **Student Chatbot**: Natural language assistant for academic queries using Groq's LLaMA 3.1
- **AI Video Generator**: Create educational videos with Manim animations and voiceover narration
- **Sentiment Analysis**: NLP-based analysis of teacher feedback
- **Student Ranking System**: AI-driven ranking combining academic scores and sentiment
- **Automated Anomaly Detection**: Isolation Forest algorithm for behavioral analysis

### 📊 Student Features
- Personal dashboard with course overview
- Grade tracking and performance analytics
- AI-powered ranking system
- Interactive chatbot for academic help
- **AI Video Generator** for educational content creation
- Teacher feedback submission
- Real-time session security status

### 👨‍💼 Admin Features
- Comprehensive user management
- Security alerts dashboard
- Student rankings overview
- **Video generation monitoring** and management
- Feedback analytics
- Course and grade management
- Real-time anomaly monitoring

---

## 🏗️ Technical Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Login UI   │  │  Dashboard   │  │ Admin Panel  │  │
│  │  + Webcam    │  │  + Chatbot   │  │  + Analytics │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend Layer (Flask)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Authentication  │  Session Management  │  APIs  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Security   │  │  AI/ML Layer │  │   Database   │
│   Module     │  │              │  │   (SQLite)   │
│              │  │              │  │              │
│ • BB84 QKD   │  │ • Chatbot    │  │ • Users      │
│ • Face Rec   │  │ • Sentiment  │  │ • Grades     │
│ • Anomaly    │  │ • Ranking    │  │ • Feedback   │
│   Detection  │  │              │  │ • Rankings   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Data Flow

1. **Login Flow**:
   ```
   User → Webcam Capture → Face Detection → Password Check → 
   BB84 Key Generation → Quantum Key Verification → Session Established
   ```

2. **Chatbot Flow**:
   ```
   User Query → LangChain Processing → Groq LLM (LLaMA) → 
   Context-Aware Response → Display to User
   ```

3. **Ranking Flow**:
   ```
   Grade Data + Feedback → Sentiment Analysis → Score Calculation → 
   Ranking Algorithm → Database Update → Display
   ```

---

## 🔧 System Components

### 1. **app.py** - Main Flask Application
- **Purpose**: Core backend server handling all routes and business logic
- **Key Functions**:
  - User authentication and session management
  - Route handlers for all endpoints
  - Integration point for all modules
  - Database operations coordinator
- **Routes**:
  - `/` - Login page
  - `/login` - Authentication with face + password
  - `/quantum_verify` - Quantum key verification
  - `/dashboard` - Student interface
  - `/admin_panel` - Administrator interface
  - `/chatbot` - AI assistant API
  - `/submit_feedback` - Feedback submission
  - `/update_rankings` - Recalculate student rankings
  - `/anomaly_alerts` - Fetch security alerts
  - `/resolve_alert` - Mark alerts as resolved
  - `/request_video` - Request AI video generation
  - `/my_videos` - List user's video requests
  - `/all_video_requests` - Admin: view all requests
  - `/download_video/<id>` - Download completed video
  - `/logout` - Session termination

### 2. **bb84.py** - Quantum Key Distribution
- **Purpose**: Simulates BB84 quantum key distribution protocol
- **How It Works**:
  1. Alice generates random bits and bases
  2. Bob independently chooses random bases
  3. Key bits are kept only where bases match (quantum principle)
  4. Returns secure key string for session encryption
- **Security**: Provides quantum-inspired session keys that detect eavesdropping

### 3. **anomaly_detector.py** - Machine Learning Security
- **Purpose**: Detects unusual login patterns and security threats
- **Algorithm**: Isolation Forest (unsupervised ML)
- **Features Analyzed**:
  - Login time patterns
  - IP address changes
  - Failed attempt frequency
  - Geographic location anomalies
- **Output**: Anomaly score and automatic alert generation
- **Database Tables**:
  - `login_attempts` - Logs all authentication attempts
  - `anomaly_alerts` - Stores security incidents

### 4. **sentiment_analyzer.py** - NLP Feedback Analysis
- **Purpose**: Analyzes teacher feedback to extract sentiment
- **Algorithm**: Lexicon-based sentiment scoring
- **Process**:
  1. Tokenize feedback text
  2. Match words against positive/negative dictionaries
  3. Apply intensifiers (e.g., "very", "extremely")
  4. Calculate sentiment score (-1.0 to +1.0)
  5. Classify as positive/neutral/negative
- **Lexicon**: 80+ positive words, 60+ negative words
- **Output**: Sentiment score, label, and confidence

### 5. **chatbot.py** - AI Academic Assistant
- **Purpose**: Provides intelligent tutoring and academic help
- **Technology Stack**:
  - **LangChain**: Framework for LLM applications
  - **Groq**: High-performance LLM inference
  - **Model**: LLaMA 3.1 8B Instant
- **Features**:
  - Conversational memory (per-session storage)
  - Step-by-step math problem solving
  - Academic question answering
  - Encouraging and supportive responses
  - Context-aware conversations
- **System Prompt**: Acts as "QUANTUM ASSISTANT" with focus on education

### 6. **video_generator.py** - AI Video Generator
- **Purpose**: Generates educational videos with AI-powered animations and narration
- **Technology Stack**:
  - **Manim CE**: Mathematical animation engine
  - **Groq LLaMA 3.3-70b**: AI code generation
  - **gTTS**: Text-to-speech narration
  - **FFmpeg**: Video/audio merging
- **Features**:
  - Topic detection (math, physics, DSA, ML, probability)
  - Automatic visual style selection
  - Narration script generation
  - Self-correcting code generation (retries on errors)
  - Background processing (non-blocking)
- **Process**:
  1. Generate narration script using Groq
  2. Convert script to speech with gTTS
  3. Generate Manim animation code
  4. Render video with Manim
  5. Merge video and audio with ffmpeg
- **Output**: 720p MP4 videos (~60 seconds) with synchronized voiceover
- **Database**: Tracks requests in `video_requests` table with status monitoring

### 7. **Frontend (HTML/CSS/JS)**

#### **login.html + login.js**
- Live webcam feed using `getUserMedia` API
- Canvas-based frame capture to base64
- Quantum key verification modal
- Real-time feedback animations
- No external dependencies

#### **dashboard.html**
- Student-focused interface
- Stats cards showing: courses, rank, score, sentiment
- Grades table with color-coded performance
- Integrated chatbot widget
- Teacher feedback form
- Security status bar

#### **admin_panel.html**
- Administrator control center
- Overview statistics
- Security alerts management (resolve functionality)
- Student rankings table
- User management
- Feedback analytics
- Course and grade overview

#### **style.css**
- Dark quantum/cyberpunk theme
- CSS variables for consistent theming
- Responsive grid layouts
- Smooth animations and transitions
- Custom scrollbar styling

---

## 💻 Installation Guide

### System Requirements

| Component | Requirement | Purpose |
|-----------|-------------|----------|
| **Python** | 3.8 or higher | Backend runtime |
| **pip** | Latest version | Package management |
| **Webcam** | Any USB/Built-in | Face verification |
| **Internet** | Active connection | Groq API access |
| **FFmpeg** | 4.4 or higher | Video generation |
| **Storage** | 500 MB+ free | Videos & database |
| **RAM** | 4 GB minimum | Manim rendering |
| **Browser** | Chrome/Firefox/Edge | Modern web features |

### Step 1: Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/your-username/quantum-lms.git
cd quantum-lms

# Or using SSH
git clone git@github.com:your-username/quantum-lms.git
cd quantum-lms
```

### Step 2: Set Up Virtual Environment

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see "(venv)" in prompt)
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation
which python  # Should show path inside venv/
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Installed Packages:**
- `flask` - Web framework for backend API
- `opencv-python` - Computer vision for face detection
- `numpy` - Numerical operations and array handling
- `scikit-learn` - Machine learning algorithms (Isolation Forest)
- `langchain` - LLM application framework
- `langchain-core` - Core LangChain components
- `langchain-groq` - Groq LLM integration
- `groq` - High-performance LLM inference API
- `manim` - Mathematical animation engine
- `gtts` - Google Text-to-Speech synthesis
- `python-dotenv` - Environment variable management

**If installation fails:**
```bash
# Try installing problematic packages individually
pip install flask opencv-python numpy scikit-learn
pip install langchain langchain-core langchain-groq groq
pip install manim gtts python-dotenv

# For OpenCV issues on Windows:
pip install opencv-python-headless
```

### Step 4: Install FFmpeg (Video Generation)

FFmpeg is **required** for AI video generation to work.

#### Windows Installation

**Option A: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey first if not installed
# Visit: https://chocolatey.org/install

# Install FFmpeg
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Option B: Manual Installation**
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Choose "Windows builds by BtbN" or "gyan.dev builds"
3. Download the "ffmpeg-release-full.7z" file
4. Extract to `C:\ffmpeg`
5. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit "Path" under System Variables
   - Add new entry: `C:\ffmpeg\bin`
   - Click OK and restart terminal
6. Verify: `ffmpeg -version`

#### Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# Verify installation
ffmpeg -version
```

#### macOS Installation

```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### Step 5: Install LaTeX (Optional - For Advanced Math)

LaTeX enables complex mathematical formula rendering in videos.

#### Windows
- Download MiKTeX: https://miktex.org/download
- Run installer (Complete installation recommended)
- MiKTeX will auto-install packages as needed

#### Linux
```bash
# Ubuntu/Debian
sudo apt install texlive-full

# Or minimal install
sudo apt install texlive texlive-latex-extra
```

#### macOS
```bash
# Using Homebrew
brew install --cask mactex
```

**Note**: LaTeX is optional. Videos will still generate without it, but complex math formulas may render differently.

### Step 6: Configure Environment Variables

**Create `.env` file** in the project root directory:

```bash
# Create from template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Or create manually
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Add the following configuration:**

```env
# ==================================================
# GROQ API KEY (Required for AI features)
# ==================================================
GROQ_API_KEY=your_groq_api_key_here

# ==================================================
# FLASK CONFIGURATION
# ==================================================
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# ==================================================
# EMAIL CONFIGURATION (Optional - for notifications)
# ==================================================
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

#### Getting Your Groq API Key (Free)

1. **Visit**: [console.groq.com](https://console.groq.com)
2. **Sign Up**: Create a free account (no credit card required)
3. **Navigate**: Go to "API Keys" in the dashboard
4. **Generate**: Click "Create API Key"
5. **Copy**: Save the key (starts with `gsk_...`)
6. **Paste**: Add to `.env` file as `GROQ_API_KEY=gsk_your_key_here`

**Free Tier Limits:**
- 30 requests per minute
- 14,400 requests per day
- Sufficient for development and small deployments

### Step 7: Initialize Database

The database is automatically created on first run:

```bash
# Start the application
python app.py
```

**What happens on first run:**
1. Creates `users.db` SQLite database
2. Creates 7 tables (users, grades, feedback, rankings, login_attempts, anomaly_alerts, video_requests)
3. Adds default admin account: `admin` / `admin123`
4. Initializes empty tables for tracking

**To reset database** (if needed):
```bash
# Stop the application first (Ctrl+C)
# Delete the database file
del users.db        # Windows
rm users.db         # Linux/Mac

# Restart app to recreate
python app.py
```

### Step 8: Add Test Users (Optional)

Add sample student and teacher accounts for testing:

```bash
# Create test users script
python add_test_users.py
```

Or create manually via Python:

```python
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Add test students
students = [
    ('student1', 'student123', 'Student', 'student1@umt.edu.pk'),
    ('student2', 'student123', 'Student', 'student2@umt.edu.pk'),
    ('student3', 'student123', 'Student', 'student3@umt.edu.pk'),
]

# Add test teachers
teachers = [
    ('teacher1', 'teacher123', 'Teacher', 'teacher1@umt.edu.pk'),
    ('teacher2', 'teacher123', 'Teacher', 'teacher2@umt.edu.pk'),
]

for user in students + teachers:
    try:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', user)
        print(f"✅ Added: {user[0]}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Already exists: {user[0]}")

conn.commit()
conn.close()
print("\n✅ Test users added successfully!")
```

### Step 9: Run the Application

```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal prompt

# Start Flask development server
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 10: Access the Application

1. **Open browser**: Chrome, Firefox, or Edge (recommended)
2. **Navigate to**: `http://127.0.0.1:5000` or `http://localhost:5000`
3. **Allow webcam access** when prompted
4. **Login** with default credentials:
   - Username: `admin`
   - Password: `admin123`

**🎉 Congratulations!** Your Quantum LMS is now running.

---

## ✅ Pre-Flight Checklist

Before reporting issues, verify all components are properly installed:

### Quick System Check

Run these commands to verify your setup:

```bash
# 1. Check Python version (must be 3.8+)
python --version
# Expected: Python 3.8.x or higher

# 2. Check if virtual environment is activated
# Windows: Should see (venv) in prompt
# Linux/Mac: Run `which python` - should show path inside venv/

# 3. Verify all Python packages are installed
pip list | findstr "flask opencv"
# Expected: flask and opencv-python listed

# 4. Test Manim installation
manim --version
# Expected: Manim Community v0.18.0 or higher

# 5. Test FFmpeg installation
ffmpeg -version
# Expected: ffmpeg version 4.4 or higher

# 6. Verify .env file exists and has Groq API key
cat .env | findstr GROQ_API_KEY  # Windows
# grep GROQ_API_KEY .env  # Linux/Mac
# Expected: GROQ_API_KEY=gsk_...

# 7. Check if database was created
dir users.db  # Windows
# ls -lh users.db  # Linux/Mac
# Expected: File exists, size > 100 KB

# 8. Test Manim rendering (quick diagnostic)
python test_manim.py
# Expected: "RENDERING SUCCESSFUL" in 10-30 seconds
```

### Component Verification

| Component | Check Command | Expected Result |
|-----------|---------------|-----------------|
| **Python** | `python --version` | 3.8+ |
| **pip** | `pip --version` | Latest |
| **Flask** | `pip show flask` | Installed |
| **OpenCV** | `pip show opencv-python` | Installed |
| **Manim** | `manim --version` | v0.18.0+ |
| **FFmpeg** | `ffmpeg -version` | v4.4+ |
| **Groq API** | Check `.env` file | Key present |
| **Database** | File `users.db` exists | ✓ |
| **Webcam** | Browser settings | Allowed |

### Common Setup Issues

If any check fails, refer to the [Troubleshooting](#troubleshooting) section below.

**All checks passed?** 🎉 Your system is ready!

---

## 🔑 Default User Credentials

### Pre-configured Accounts

The following accounts are available immediately after setup:

#### Administrator
```
Username: admin
Password: admin123
Role:     Admin
Access:   Full system control, security monitoring, user management
```

#### Sample Student
```
Username: f2022376139
Password: nahin123
Role:     Student
Access:   Dashboard, grades, chatbot, video generator, feedback
```

#### Sample Teacher
```
Username: sir ail
Password: ali123
Role:     Teacher
Note:     Username contains a space
Access:   Teacher interface (if implemented)
```

#### Test Accounts (After running add_test_users.py)

**Students:**
- `student1` / `student123`
- `student2` / `student123`
- `student3` / `student123`

**Teachers:**
- `teacher1` / `teacher123`
- `teacher2` / `teacher123`

**⚠️ Security Warning**: Change default passwords in production!

---

## � Default User Credentials

The system currently has the following accounts in the database:

### Administrator Account
```
Username: admin
Password: admin123
Role: Admin Access
```

### Student Account
```
Username: f2022376139
Password: nahin123
Role: Student
```

### Teacher Account
```
Username: sir ail
Password: ali123
Role: Teacher
Note: Username contains a space
```

**⚠️ Important Notes:**
- These are the ONLY accounts currently in the database
- The `init_db()` function only creates the admin account by default
- To add more test users, see "Adding Test Users" section below

### Adding Test Users

To add student and teacher test accounts, run this Python script:

```python
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Add test students
students = [
    ('student1', 'student123', 'Student', 'student1@umt.edu.pk'),
    ('student2', 'student123', 'Student', 'student2@umt.edu.pk'),
    ('student3', 'student123', 'Student', 'student3@umt.edu.pk'),
]

# Add test teachers
teachers = [
    ('teacher1', 'teacher123', 'Teacher', 'teacher1@umt.edu.pk'),
    ('teacher2', 'teacher123', 'Teacher', 'teacher2@umt.edu.pk'),
]

for user in students + teachers:
    try:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', user)
        print(f"Added user: {user[0]}")
    except sqlite3.IntegrityError:
        print(f"User {user[0]} already exists")

conn.commit()
conn.close()
print("Test users added successfully!")
```

Save as `add_test_users.py` and run: `python add_test_users.py`

---

## �📖 Usage Guide

### For Students

#### 1. **Login Process**

1. **Navigate** to `http://127.0.0.1:5000`
2. **Allow webcam access** when prompted by browser
3. **Position your face** in the camera view (green border = detected)
4. **Enter credentials**:
   - Example: `username: f2022376139`, `password: nahin123`
5. **Click LOGIN** button
6. **Wait for the Quantum Key Modal** to appear automatically
   - The system will display a unique quantum key (e.g., `1011010110...`)
   - This key is generated using BB84 quantum protocol
7. **Copy the entire quantum key** from the modal (it will be highlighted)
8. **Paste the key** into the verification input field
9. **Click VERIFY** to complete authentication and access dashboard

**How the Quantum Key Works:**
- After successful password + face check, the server generates a random quantum key
- The key is sent to your browser and stored in the session
- You must enter this EXACT key to prove session ownership
- This adds a third authentication factor after face + password
- Keys are single-use and expire after verification

**📌 Troubleshooting:**
- **Modal doesn't appear?** Check browser console for errors
- **Key verification fails?** Make sure you copied the ENTIRE key (no spaces added)
- **Stuck on verification?** Refresh page and login again

#### 2. **Dashboard Features**

**View Statistics:**
- See your total courses
- Check your current rank
- View your final score
- Monitor sentiment status

**Check Grades:**
- Scroll to "My Grades" section
- View all courses, assessments, scores, and grades
- Color-coded grades (Green=A, Cyan=B, Yellow=C, Red=D/F)

**Use Chatbot:**
- Scroll to "Quantum Assistant" section
- Type questions about courses, homework, or concepts
- Chatbot remembers conversation context
- Get step-by-step help for math problems
- Receive encouraging feedback

**Generate AI Videos: (AI Agent)**
- Scroll to "🎬 Video Generator" section
- Enter topic (e.g., "Pythagorean Theorem", "Binary Search")
- Add optional description for specific details
- Click "🚀 Generate Video"
- Wait 2-5 minutes for video generation
- Download completed video from "My Videos" list
- Videos include Manim animations + voiceover narration

**Submit Feedback:**
- Scroll to "Submit Teacher Feedback" section
- Select teacher from dropdown
- Rate 1-5 stars
- Write detailed comment
- Click "Submit Feedback"

### For Administrators

#### 1. **Login as Admin**

Use credentials: `admin` / `admin123`

After quantum verification, you'll be redirected to the admin panel.

**Teachers' accounts**

Username: teacher1
Password: teacher123
Role: Teacher

Username: teacher2
Password: teacher123
Role: Teacher

**Students' accounts**

Username: student1
Password: student123
Role: Student

Username: student2
Password: student123
Role: Student

Username: student3
Password: student123
Role: Student

#### 2. **Admin Panel Features**

**Overview Dashboard:**
- View total users count
- Monitor total feedback
- Check active security alerts
- See number of ranked students

**Security Alerts Management:**
- Review unresolved alerts (red badges)
- Check alert type, username, description
- View severity level (HIGH/MEDIUM/LOW)
- Click "✓ Resolve" to mark as handled
- Alerts disappear from active list

**Student Rankings:**
- View complete ranking table
- See academic scores, sentiment scores, final scores
- Monitor sentiment labels
- Click "🔄 Refresh Rankings" to recalculate
- Gold/Silver/Bronze highlighting for top 3

**User Management:**
- View all system users
- Check roles (ADMIN/TEACHER/STUDENT)
- Monitor email addresses

**Feedback Analytics:**
- Review all submitted feedback
- See student, teacher, rating, comments
- Track submission dates
- Identify trends in feedback

**Video Generation Management:**
- View all video generation requests
- Monitor status (Pending/Processing/Completed/Failed)
- See which students requested videos
- Track completion times
- Click "🔄 Refresh" to update list

**Courses & Grades:**
- View active courses list
- Monitor recent grade submissions
- Check distribution of grades

---

## 📁 Project Structure

```
Quantum-/
├── app.py                      # Main Flask application
├── chatbot.py                  # LangChain chatbot module
├── video_generator.py          # AI video generation module
├── bb84.py                     # Quantum key distribution
├── anomaly_detector.py         # ML anomaly detection
├── sentiment_analyzer.py       # NLP sentiment analysis
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── users.db                    # SQLite database (auto-created)
├── VIDEO_GENERATOR_GUIDE.md    # Video generator documentation
│
├── templates/                  # HTML templates
│   ├── login.html             # Login page with webcam
│   ├── dashboard.html         # Student interface
│   └── admin_panel.html       # Admin interface
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Global styles (quantum theme)
│   └── js/
│       ├── main.js            # Shared utilities
│       └── login.js           # Login page logic
│
└── output/                     # Generated content
    └── videos/                # AI-generated videos
```

---

## 🔐 Security Features

### Multi-Layer Authentication

1. **Biometric Layer**: OpenCV face detection (Haar Cascade)
2. **Credential Layer**: Username/password verification
3. **Quantum Layer**: BB84-inspired key distribution
4. **Session Layer**: Flask secure sessions

### Anomaly Detection

- **Algorithm**: Isolation Forest (scikit-learn)
- **Monitoring**: Login times, IP addresses, failure rates
- **Response**: Automatic alert generation for admins
- **Logging**: Complete audit trail in database

### Quantum Key Distribution (BB84 Simulation)

The BB84 protocol ensures:
- **Key Generation**: Random bits with random bases
- **Basis Reconciliation**: Only matching bases are kept
- **Security**: Eavesdropping detection principle
- **Session Binding**: Unique key per login session

### Data Protection

- **Environment Variables**: Sensitive data in `.env`
- **Session Management**: Secure Flask sessions
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Proper template escaping

---

## 🔌 API Endpoints

### Authentication
- `POST /login` - Authenticate with face + password
- `POST /quantum_verify` - Verify quantum key
- `GET /logout` - End session

### Student Interface
- `GET /dashboard` - Student dashboard
- `POST /chatbot` - Chat with AI assistant
- `POST /submit_feedback` - Submit teacher feedback
- `POST /request_video` - Request AI video generation
- `GET /my_videos` - Get user's video requests
- `GET /download_video/<id>` - Download video file

### Admin Interface
- `GET /admin_panel` - Admin control panel
- `GET /anomaly_alerts` - Fetch security alerts (JSON)
- `POST /resolve_alert` - Mark alert as resolved
- `POST /update_rankings` - Recalculate student rankings
- `GET /all_video_requests` - View all video generation requests

---

## 🛠️ Technologies Used

### Backend
- **Flask** - Python web framework
- **SQLite** - Embedded database
- **OpenCV** - Computer vision for face detection
- **scikit-learn** - Machine learning library
- **NumPy** - Numerical computing

### AI/ML
- **LangChain** - LLM application framework
- **Groq** - High-speed LLM inference
- **LLaMA 3.1/3.3** - Large language models (8B-70B parameters)
- **Manim CE** - Mathematical animation engine
- **gTTS** - Google Text-to-Speech
- **FFmpeg** - Video processing

### Frontend
- **HTML5** - Structure and webcam API
- **CSS3** - Styling with custom properties
- **Vanilla JavaScript** - No frameworks (lightweight)
- **Fetch API** - Async HTTP requests

### Security
- **python-dotenv** - Environment variable management
- **Haar Cascade** - Face detection classifier
- **BB84 Protocol** - Quantum key distribution simulation

---

## 🎯 Future Enhancements

- [ ] Real quantum hardware integration
- [ ] Advanced ML models (VADER sentiment, BERT)
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Video conferencing integration
- [ ] Advanced analytics dashboard
- [ ] Assignment submission system
- [ ] Real-time notifications
- [ ] Email alert system integration
- [ ] OAuth2 authentication

---

## 📝 Database Schema

### users
| Column   | Type | Description          |
|----------|------|----------------------|
| username | TEXT | Primary key          |
| password | TEXT | Hashed password      |
| role     | TEXT | Admin/Teacher/Student|
| email    | TEXT | Contact email        |

### grades
| Column      | Type    | Description       |
|-------------|---------|-------------------|
| id          | INTEGER | Auto-increment    |
| student_id  | TEXT    | Student username  |
| course      | TEXT    | Course name       |
| assessment  | TEXT    | Assessment type   |
| score       | TEXT    | Score achieved    |
| grade       | TEXT    | Letter grade      |

### feedback
| Column  | Type    | Description     |
|---------|---------|-----------------|
| id      | INTEGER | Auto-increment  |
| student | TEXT    | Student name    |
| teacher | TEXT    | Teacher name    |
| rating  | INTEGER | 1-5 stars       |
| comment | TEXT    | Feedback text   |
| date    | TEXT    | Submission date |

### student_rankings
| Column          | Type      | Description           |
|-----------------|-----------|-----------------------|
| id              | INTEGER   | Auto-increment        |
| student         | TEXT      | Student name (unique) |
| academic_score  | REAL      | Grade-based score     |
| sentiment_score | REAL      | Feedback sentiment    |
| final_score     | REAL      | Combined score        |
| rank_position   | INTEGER   | Rank number           |
| sentiment_label | TEXT      | pos/neg/neutral       |
| feedback_count  | INTEGER   | Total feedback        |
| last_updated    | TIMESTAMP | Update timestamp      |

### login_attempts
| Column        | Type      | Description        |
|---------------|-----------|--------------------|
| id            | INTEGER   | Auto-increment     |
| username      | TEXT      | Attempted username |
| timestamp     | TIMESTAMP | Time of attempt    |
| ip_address    | TEXT      | Source IP          |
| success       | BOOLEAN   | Success flag       |
| face_detected | BOOLEAN   | Face check result  |
| is_anomaly    | BOOLEAN   | Anomaly flag       |
| anomaly_score | REAL      | ML anomaly score   |
| location      | TEXT      | Geographic location|

### anomaly_alerts
| Column      | Type      | Description          |
|-------------|-----------|----------------------|
| id          | INTEGER   | Auto-increment       |
| username    | TEXT      | Affected user        |
| alert_time  | TIMESTAMP | Time of alert        |
| alert_type  | TEXT      | Type of threat       |
| description | TEXT      | Alert details        |
| severity    | TEXT      | high/medium/low      |
| resolved    | BOOLEAN   | Resolution status    |

### video_requests
| Column        | Type      | Description              |
|---------------|-----------|---------------------------|
| id            | INTEGER   | Auto-increment            |
| username      | TEXT      | Requesting student        |
| topic         | TEXT      | Video topic               |
| description   | TEXT      | Additional details        |
| status        | TEXT      | pending/processing/completed/failed |
| video_path    | TEXT      | Path to generated video   |
| script        | TEXT      | Narration script          |
| requested_at  | TIMESTAMP | Request time              |
| completed_at  | TIMESTAMP | Completion time           |
| error_message | TEXT      | Error details (if failed) |

---

## 🤝 Contributing

This is an academic project. For questions or suggestions, please contact the development team.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Authors

**Quantum LMS Development Team**  
University of Management and Technology (UMT)  
Spring 2026

---

## 🆘 Troubleshooting

### Installation Issues

#### "Python not found" or "pip not found"
```bash
# Verify Python installation
python --version
python3 --version  # Try python3 on Linux/Mac

# Add Python to PATH (Windows)
# System Properties → Environment Variables → Path → Add Python directory
```

#### "Virtual environment activation failed"
```powershell
# Windows: Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\activate
```

#### "pip install fails" or "Module not found"
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall requirements
pip install -r requirements.txt --no-cache-dir

# If specific package fails (e.g., opencv)
pip install opencv-python-headless  # Alternative for OpenCV
```

#### "FFmpeg not found" when generating videos
```bash
# Verify FFmpeg is installed and in PATH
ffmpeg -version

# Windows: Check PATH contains ffmpeg\bin
echo %PATH%

# Linux/Mac: Check ffmpeg location
which ffmpeg

# If not found, reinstall FFmpeg and restart terminal
```

### Runtime Issues

#### Webcam not working
**Symptoms**: "Face CHECK FAILED" or black webcam screen

**Solutions**:
1. **Check browser permissions**:
   - Chrome: Settings → Privacy → Site Settings → Camera → Allow
   - Firefox: about:preferences#privacy → Permissions → Camera
   - Edge: Settings → Cookies and site permissions → Camera

2. **Close other apps** using webcam (Zoom, Teams, Skype)

3. **Try different browser** (Chrome recommended)

4. **Check device manager** (Windows):
   - Ensure camera driver is enabled
   - Update camera driver if needed

5. **Test webcam**:
   ```bash
   # Linux: Test with cheese
   cheese
   
   # Windows: Open Camera app
   # Mac: Open Photo Booth
   ```

#### Chatbot not responding
**Symptoms**: "Empty response" or "Error: Unable to chat"

**Solutions**:
1. **Verify GROQ_API_KEY in `.env`**:
   ```bash
   # Check if key exists and is valid
   cat .env | grep GROQ_API_KEY
   # Should show: GROQ_API_KEY=gsk_...
   ```

2. **Test API key manually**:
   ```python
   from groq import Groq
   client = Groq(api_key="your_key_here")
   response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
       messages=[{"role":"user","content":"test"}]
   )
   print(response.choices[0].message.content)
   ```

3. **Check internet connection**

4. **Verify API quota**: Visit [console.groq.com](https://console.groq.com) → Usage

5. **Check server logs** for detailed error messages

#### Video generation takes forever / never completes
**Symptoms**: Audio (.mp3) generated quickly, but video stuck at "STEP 4/5: Rendering animation" for 5+ minutes

**Root Cause**: Flask's debug mode auto-reload (watchdog) is killing the Manim subprocess when it detects file changes.

**Solution** (CRITICAL):
The app.py has been configured with `use_reloader=False` to prevent this issue. **DO NOT change this setting** or video generation will fail.

```python
# In app.py - keep this setting:
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    # ☝️ use_reloader=False is ESSENTIAL for video generation
```

**If you modified app.py**, restore this setting and restart:
```bash
# Kill any stuck processes
taskkill /F /IM python.exe  # Windows
# pkill -9 python  # Linux/Mac

# Restart Flask
python app.py
```

**Note**: With `use_reloader=False`, Flask won't auto-restart when you change code. After editing files, manually restart Flask (Ctrl+C, then `python app.py`).

#### Video generation produces only audio (no video)
**Symptoms**: Only .mp3 file generated, no .mp4 output, process completes quickly

**Root Causes & Solutions**:

1. **Manim not installed** (most common):
   ```bash
   # Test Manim installation
   manim --version
   
   # If not found, install it
   pip install manim
   
   # Test with diagnostic script
   python test_manim.py
   ```

2. **FFmpeg not in PATH**:
   ```bash
   # Verify FFmpeg is accessible
   ffmpeg -version
   
   # If fails, add to PATH and restart terminal
   ```

3. **LaTeX not installed** (for math formulas):
   - Install MiKTeX (Windows) or TeX Live (Linux)
   - Or request non-math topics (won't need LaTeX)

4. **Insufficient permissions**:
   ```bash
   # Check output directory is writable
   # Windows:
   icacls output\videos
   
   # Linux/Mac:
   ls -la output/videos
   chmod 755 output/videos
   ```

5. **Check Manim logs**:
   ```bash
   # Look for error messages in console
   # Common: "LaTeX Error", "File not found", "Permission denied"
   ```

6. **Manual test**:
   ```python
   # Create test scene
   from manim import *
   
   class Test(Scene):
       def construct(self):
           text = Text("Hello")
           self.play(Write(text))
   
   # Save as test.py and run:
   # manim test.py Test -ql
   ```

#### "Quantum key verification failed"
**Symptoms**: Modal shows key but verification rejects it

**Solutions**:
1. **Copy entire key** - ensure no spaces/linebreaks added
2. **Paste directly** - don't type manually
3. **Try again** - refresh page and login fresh
4. **Clear browser cache** - Ctrl+Shift+Delete

#### Database errors
**Symptoms**: "Database is locked" or "Table not found"

**Solutions**:
1. **Reset database**:
   ```bash
   # Stop application (Ctrl+C)
   # Backup first if needed
   copy users.db users_backup.db  # Windows
   
   # Delete and recreate
   del users.db
   python app.py  # Will recreate automatically
   ```

2. **Check file permissions**:
   ```bash
   # Linux/Mac
   chmod 644 users.db
   
   # Windows: Right-click → Properties → Security
   ```

3. **Close other connections**:
   - Only run one instance of `python app.py`
   - Close any SQLite browser tools

#### Import errors
**Symptoms**: `ModuleNotFoundError: No module named '...'`

**Solutions**:
1. **Verify virtual environment is activated**:
   - Look for `(venv)` in terminal prompt
   - Reactivate if needed: `venv\Scripts\activate`

2. **Check Python interpreter** (VS Code):
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choose the one inside `venv` folder

3. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

4. **Verify Python version**:
   ```bash
   python --version  # Must be 3.8+
   ```

### Performance Issues

#### Video generation is very slow
**Expected**: 2-5 minutes per video  
**If taking 10+ minutes**:

1. **Use lower quality** (edit `video_generator.py`):
   ```python
   # Change from -ql (low) to -ql (stays low)
   # For faster: Keep -ql
   # For better quality but slower: Use -qm or -qh
   ```

2. **Reduce video duration** - request shorter topics

3. **Check system resources**:
   - Close other heavy applications
   - Ensure sufficient RAM (4GB+ free)

4. **Upgrade hardware** or use cloud deployment

#### Application is unresponsive
**Solutions**:
1. **Check console for errors** - look for Python exceptions
2. **Restart Flask server** - Ctrl+C then `python app.py`
3. **Clear browser cache** - Ctrl+Shift+Delete
4. **Check database locks** - close other SQLite connections

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Address already in use` | Port 5000 occupied | Kill process on port 5000 or change port |
| `No module named 'cv2'` | OpenCV not installed | `pip install opencv-python` |
| `Groq API error 401` | Invalid API key | Check `.env` file, regenerate key |
| `FFmpeg not found` | FFmpeg not in PATH | Install FFmpeg, add to PATH, restart terminal |
| `LaTeX Error` | LaTeX not installed | Install MiKTeX or request non-math topics |
| `Database is locked` | Multiple connections | Close other SQLite tools, restart app |
| `Face detection failed` | Webcam issues | Check browser permissions, lighting |
| `Session expired` | Quantum key timeout | Login again from scratch |

### Getting Help

If issues persist:

1. **Check logs**: Look at terminal output for detailed error messages
2. **Enable debug mode**: Set `FLASK_DEBUG=True` in `.env`
3. **Test components individually**: Run each module separately to isolate issues
4. **Check GitHub Issues**: Search for similar problems
5. **Contact support**: Open an issue with:
   - Error message (full traceback)
   - Python version (`python --version`)
   - OS version
   - Steps to reproduce

---

## 📞 Support

For technical support or inquiries:
- **Email**: support@quantum-lms.edu
- **Documentation**: See inline code comments
- **Issues**: Report bugs via issue tracker

---

**Built with ❤️ for the future of education**

---

## 📚 Additional Documentation

For more detailed information:

- **[VIDEO_GENERATOR_GUIDE.md](VIDEO_GENERATOR_GUIDE.md)** - Complete video generation documentation
- **Inline Code Comments** - Detailed explanations in all Python files
- **API Documentation** - See [API Endpoints](#api-endpoints) section above

---

## 🔄 Updating the Application

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
python app.py
```
