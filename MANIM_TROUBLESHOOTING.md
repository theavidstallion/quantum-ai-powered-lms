# Manim Troubleshooting Guide

## Issue 1: "Manim not found" despite installation

### Symptom
```
'manim' is not recognized as an internal or external command
ModuleNotFoundError: No module named 'manim'
```

### Root Causes & Solutions

#### Solution 1: Virtual Environment Not Activated (MOST COMMON)
```powershell
# Check if venv is activated (look for (venv) in prompt)
# If NOT activated:
cd e:\Projects\quantum-lms\Quantum-
.\venv\Scripts\Activate.ps1

# Verify Python location
python -c "import sys; print(sys.executable)"
# Should show: E:\Projects\quantum-lms\Quantum-\venv\Scripts\python.exe

# Verify Manim installation
python -m manim --version
```

#### Solution 2: Installed in wrong Python environment
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Install Manim in the ACTIVE venv
pip install manim

# Verify
pip show manim
# Should show: Location: e:\Projects\quantum-lms\Quantum-\venv\Lib\site-packages
```

#### Solution 3: PowerShell Execution Policy (Windows)
```powershell
# If you get "cannot be loaded because running scripts is disabled"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv
.\venv\Scripts\Activate.ps1
```

#### Solution 4: System PATH vs Virtual Environment
```powershell
# DON'T install Manim globally if using venv
# Always activate venv first, then install

# If you installed globally by mistake:
pip uninstall manim  # (outside venv - removes global)

# Then in venv:
.\venv\Scripts\Activate.ps1
pip install manim
```

#### Solution 5: Python version mismatch
```powershell
# Check Python version
python --version
# Should be Python 3.9 or higher

# If wrong version, recreate venv with correct Python
python3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Issue 2: Manim renders fail with errors

### Error: "Could not find [filename] at either of these locations"
**Cause**: AI generated code with external file references (SVGMobject, ImageMobject)

**Fix**: Already patched in video_generator.py (v2.1) - prompts now restrict AI to built-in primitives only

**Test**:
```powershell
# Try generating a new video after the fix
# If still happens, check video_generator.py line 148-160 has CRITICAL RESTRICTIONS section
```

### Error: "FFmpeg not found"
**Fix**:
```powershell
# Install FFmpeg
choco install ffmpeg

# Verify
ffmpeg -version

# Restart terminal after installation
```

### Error: "LaTeX not found" (for complex math)
**Fix**:
```powershell
# Install MiKTeX (optional - only for complex LaTeX)
choco install miktex

# Or use basic MathTex which doesn't require LaTeX
# Manim CE has built-in fallback for simple equations
```

---

## Issue 3: Flask kills video generation mid-render

### Symptom
```
Video generation hangs at STEP 4/5
Console shows: "Detected change in 'temp_scene.py', reloading"
Process completes but no video file created
```

### Solution
Already fixed in app.py line 366:
```python
app.run(debug=True, use_reloader=False)
```

**Verify**: Check [app.py](app.py#L366) has `use_reloader=False`

---

## Complete Diagnostic Checklist

### Step 1: Environment Verification
```powershell
# Run this diagnostic script
cd e:\Projects\quantum-lms\Quantum-

# 1. Check venv activation
echo $env:VIRTUAL_ENV
# Should output: E:\Projects\quantum-lms\Quantum-\venv

# 2. Check Python path
python -c "import sys; print(sys.executable)"
# Should be inside venv\Scripts\

# 3. Check Manim
python -m manim --version
# Should show: Manim Community v0.20.1

# 4. Check FFmpeg
ffmpeg -version
# Should show: ffmpeg version 8.0 or higher

# 5. Check dependencies
pip list | Select-String "manim|cv2|numpy"
# Should show: manim, numpy, opencv-python
```

### Step 2: Test Manim Directly
```powershell
# Use the test script
python test_manim.py

# Expected output:
# ✅ Python executable: venv\Scripts\python.exe
# ✅ Manim version: 0.20.1
# ✅ FFmpeg found: 8.0
# ✅ Rendering test scene...
# RENDERING SUCCESSFUL! (4-6 seconds)
```

### Step 3: Test Video Generator
```powershell
# Start Flask
python app.py

# Should see:
# * Running on http://127.0.0.1:5000
# (No "Restarting with watchdog" message)

# Generate a video via UI
# Monitor console for:
# 🎬 STEP 4/5: Rendering animation
# ✅ Manim process completed (return code: 0)
# ✅ VIDEO GENERATION COMPLETE
```

---

## Common Mistakes

❌ **Installing Manim globally**: Causes version conflicts
✅ **Always activate venv first**: `.\venv\Scripts\Activate.ps1`

❌ **Using Command Prompt on Windows**: May have PATH issues
✅ **Use PowerShell**: Better compatibility with venv

❌ **Running `pip install manim` without venv active**
✅ **Check for (venv) in prompt before installing**

❌ **Expecting Flask auto-reload to work**
✅ **Restart Flask manually after code changes**: (Ctrl+C → python app.py)

❌ **Installing FFmpeg after activating venv**
✅ **FFmpeg is system-wide**: Install with chocolatey (choco install ffmpeg)

---

## Quick Reference Commands

### Virtual Environment
```powershell
# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (CMD)
.\venv\Scripts\activate.bat

# Deactivate
deactivate
```

### Installation
```powershell
# Clean install
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Testing
```powershell
# Test Manim installation
python test_manim.py

# Test direct render
python -m manim test_manim.py TestScene -ql
```

### Running App
```powershell
# Production mode (recommended)
.\venv\Scripts\Activate.ps1
python app.py

# Background mode (Windows)
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

---

## Still Not Working?

### Debug Mode
```powershell
# Enable verbose output in video_generator.py
# Check console for detailed error messages
# Look for:
#   ❌ Manim failed with errors:
#   [Full traceback shown]

# Common error patterns:
# - "No module named 'manim'" → venv not activated
# - "Could not find [file]" → AI hallucinating external files (fixed in v2.1)
# - "FFmpeg not found" → Install via choco
# - "LaTeX error" → Use simpler MathTex expressions
```

### Get Help
1. Check console output during video generation
2. Look for full error traceback in Flask terminal
3. Run `python test_manim.py` to isolate Manim issues
4. Check [SECURITY_AUDIT.md](SECURITY_AUDIT.md) for environment setup
5. Review [README.md](README.md) Pre-Flight Checklist

---

## Version Info
- **Python**: 3.12+ required
- **Manim Community**: 0.20.1
- **FFmpeg**: 8.0+ required
- **Windows**: PowerShell 5.1+ recommended
- **Flask**: 3.1.3

Last updated: 2026-02-28
