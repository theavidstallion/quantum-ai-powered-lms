# 🎬 AI Video Generator - Quick Start Guide

## Overview

The AI Video Generator creates educational videos with:
- **AI-Generated Animations**: Manim-powered mathematical and scientific visualizations
- **Voiceover Narration**: Natural-sounding speech using gTTS
- **Topic Detection**: Automatically detects topic type (math, physics, DSA, ML, etc.)
- **Groq LLaMA 3.3**: Generates both narration script and Manim animation code

---

## Installation

### 1. Install New Dependencies

```powershell
pip install manim groq gtts
```

**Note**: Manim also requires:
- **ffmpeg** (for video processing)
- **LaTeX** (for mathematical formulas)

#### Install FFmpeg on Windows:

**Option A: Using Chocolatey**
```powershell
choco install ffmpeg
```

**Option B: Manual Install**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

#### Install LaTeX (Optional but Recommended):

Download MiKTeX from https://miktex.org/download

---

## Configuration

The video generator automatically uses your existing `GROQ_API_KEY` from `.env`:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

No additional configuration needed!

---

## How to Use

### For Students:

1. **Login** to your dashboard
2. **Navigate** to "🎬 Video Generator" section
3. **Enter a topic**, for example:
   - `Pythagorean Theorem`
   - `Binary Search Algorithm`
   - `K-Nearest Neighbors`
   - `Gradient Descent`
   - `Newton's Laws of Motion`
   - `Fourier Transform`
4. **Add description** (optional) for specific details
5. **Click "🚀 Generate Video"**
6. **Wait 2-5 minutes** for video generation
7. **Download** the video when status shows "✅ COMPLETED"

### For Admins:

1. **Login** to admin panel
2. **Navigate** to "🎬 Videos" section
3. **View all video requests** from all students
4. **Monitor status** (Pending → Processing → Completed/Failed)
5. **Click "🔄 Refresh"** to update the list

---

## Topic Profiles

The generator automatically detects topic types and applies appropriate visual styles:

### 🔢 Math
- **Keywords**: calculus, derivative, integral, matrix, algebra, geometry
- **Visuals**: Axes with function plots, colored formula terms, animated graphs
- **Formulas**: Chain rule, integration, Euler's identity, Pythagorean theorem

### ⚛️ Physics
- **Keywords**: mechanics, force, energy, momentum, velocity, gravity
- **Visuals**: Force arrows, motion graphs, wave animations, circuit diagrams
- **Formulas**: F=ma, E=mc², kinetic energy, Ohm's law

### 💻 DSA (Data Structures & Algorithms)
- **Keywords**: array, tree, graph, sorting, BFS, DFS, algorithm
- **Visuals**: Square arrays with color states, tree nodes, graph traversal
- **Formulas**: Big-O notation (O(n), O(log n), O(n²))

### 🤖 Machine Learning
- **Keywords**: regression, classification, neural network, gradient, training
- **Visuals**: Scatter plots, decision boundaries, loss curves, neural nets
- **Formulas**: Loss functions, gradient descent, sigmoid

### 📊 Probability
- **Keywords**: probability, bayes, distribution, statistics, gaussian
- **Visuals**: Bell curves, Venn diagrams, bar charts, confidence intervals
- **Formulas**: Bayes theorem, expected value, normal distribution

---

## Video Generation Process

```
1. Student submits topic
   ↓
2. Groq generates narration script (60 seconds)
   ↓
3. gTTS converts script to audio (.mp3)
   ↓
4. Groq generates Manim animation code
   ↓
5. Manim renders video (.mp4)
   ↓
6. ffmpeg merges video + audio
   ↓
7. Final video ready for download!
```

**Average Generation Time**: 2-5 minutes per video

---

## File Storage

Videos are stored in:
```
output/videos/
  └── YYYYMMDD_HHMMSS_topic_name.mp4
```

Each video includes:
- Visual animation (720p)
- Synchronized narration
- Mathematical formulas (when applicable)
- Step-by-step explanations

---

## Troubleshooting

### "Video generation failed"
- **Check**: FFmpeg is installed and in PATH
- **Run**: `ffmpeg -version` to verify
- **Solution**: Reinstall ffmpeg or add to PATH

### "Import 'manim' could not be resolved"
- **Check**: Virtual environment is activated
- **Run**: `pip install manim`
- **Solution**: Select correct Python interpreter in VS Code

### Video stuck in "Processing"
- **Check**: Database status with: `python -c "import sqlite3; conn = sqlite3.connect('users.db'); print(conn.execute('SELECT * FROM video_requests').fetchall())"`
- **Solution**: Review terminal output for Manim errors

### "LaTeX not found" error
- **Check**: MiKTeX is installed
- **Solution**: Install MiKTeX or use non-LaTeX topics (DSA, basic physics)

### Low-quality animations
- **Cause**: Using `-ql` (low quality) flag for speed
- **Solution**: Edit [video_generator.py](video_generator.py#L220) line 220, change `-ql` to `-qh` for high quality

---

## Dependencies Summary

| Package | Purpose | Version |
|---------|---------|---------|
| manim | Animation engine | Latest |
| groq | LLM API client | Latest |
| gtts | Text-to-speech | Latest |
| ffmpeg | Video processing | 4.4+ |
| LaTeX | Math rendering | Any |

---

## Examples

### Example 1: Math Topic
**Input**: "Pythagorean Theorem"

**Output**:
- 60-second video
- Animated right triangle
- Formula: a² + b² = c²
- Narration explaining geometric proof
- Visual demonstration with colored sides

### Example 2: DSA Topic
**Input**: "Binary Search Algorithm"

**Output**:
- Array visualization with colored cells
- Step-by-step search animation
- Big-O notation: O(log n)
- Narration explaining divide-and-conquer
- Comparison with linear search

### Example 3: ML Topic
**Input**: "Gradient Descent"

**Output**:
- 3D loss curve animation
- Ball rolling to minimum
- Formula: θ := θ - α∇J
- Narration explaining optimization
- Learning rate visualization

---

## API Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/request_video` | POST | Submit video generation request |
| `/my_videos` | GET | List user's videos |
| `/all_video_requests` | GET | Admin: list all videos |
| `/download_video/<id>` | GET | Download completed video |

---

## Performance Notes

- **Concurrent Requests**: Handled by background threads
- **Queue**: Multiple students can request videos simultaneously
- **Storage**: ~5-10MB per video
- **API Usage**: ~2 Groq API calls per video (script + code generation)

---

## Future Enhancements

- [ ] Real-time progress updates (WebSockets)
- [ ] Video quality selector (low/medium/high)
- [ ] Custom duration (30s / 60s / 120s)
- [ ] Thumbnail preview
- [ ] Video sharing links
- [ ] Batch video generation
- [ ] Video editing (trim, add captions)

---

## Credits

Built with:
- **Manim Community Edition** by 3Blue1Brown
- **Groq LLaMA 3.3-70b** for AI generation
- **gTTS** for text-to-speech
- **FFmpeg** for video processing

---

## Support

If you encounter issues:
1. Check terminal output for error messages
2. Verify all dependencies are installed
3. Ensure GROQ_API_KEY is valid
4. Review `video_requests` table in database

**Video generation is compute-intensive. First run may take longer as Manim downloads dependencies.**

---

**Enjoy creating educational videos! 🎓🎬**
