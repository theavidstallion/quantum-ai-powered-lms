"""
Quick Manim Test - Diagnoses if Manim is working correctly
Run this to test: python test_manim.py
"""
import subprocess
import sys
import os
import time

print("="*60)
print("🧪 MANIM DIAGNOSTIC TEST")
print("="*60)

# Test 1: Check if Manim is installed
print("\n📦 Test 1: Checking Manim installation...")
try:
    result = subprocess.run(
        ['manim', '--version'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"   ✅ Manim installed: {version}")
    else:
        print(f"   ❌ Manim command failed")
        print(f"   Error: {result.stderr}")
        sys.exit(1)
except FileNotFoundError:
    print("   ❌ Manim not found in PATH")
    print("   💡 Try: pip install manim")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Check FFmpeg
print("\n🎬 Test 2: Checking FFmpeg installation...")
try:
    result = subprocess.run(
        ['ffmpeg', '-version'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"   ✅ FFmpeg installed: {version_line}")
    else:
        print(f"   ⚠️ FFmpeg may not be working correctly")
except FileNotFoundError:
    print("   ❌ FFmpeg not found")
    print("   💡 Install: choco install ffmpeg (Windows)")
    sys.exit(1)

# Test 3: Create and render simple scene
print("\n🎨 Test 3: Creating test scene...")
test_code = """from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Manim Works!", color=GREEN, font_size=60)
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(text))
"""

test_file = 'manim_test_scene.py'
with open(test_file, 'w') as f:
    f.write(test_code)
print(f"   ✅ Test file created: {test_file}")

# Test 4: Render the scene
print("\n🎬 Test 4: Rendering scene (30 second timeout)...")
print("   ⏳ Please wait, this should take 10-30 seconds...")

start_time = time.time()
try:
    result = subprocess.run(
        ['manim', test_file, 'TestScene', '-ql', '--disable_caching'],
        capture_output=True,
        text=True,
        timeout=30  # 30 seconds should be enough for simple scene
    )
    
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"   ✅ RENDERING SUCCESSFUL! ({elapsed:.1f} seconds)")
        print(f"   📁 Check 'media/videos/' folder for output")
        
        # Try to find the output file
        import glob
        videos = glob.glob('media/videos/**/*.mp4', recursive=True)
        if videos:
            video_file = videos[0]
            file_size = os.path.getsize(video_file) / 1024
            print(f"   📹 Video file: {video_file} ({file_size:.1f} KB)")
    else:
        print(f"   ❌ RENDERING FAILED ({elapsed:.1f} seconds)")
        print(f"   Error output:")
        print(result.stderr[:500])
        
except subprocess.TimeoutExpired:
    elapsed = time.time() - start_time
    print(f"   ⏰ TIMEOUT after {elapsed:.1f} seconds")
    print(f"   ❌ Manim is taking too long - likely stuck")
    print(f"\n   💡 Possible causes:")
    print(f"      - LaTeX not installed or misconfigured")
    print(f"      - System resources too low (need 2GB+ RAM)")
    print(f"      - Manim installation corrupted")
    print(f"\n   🔧 Try:")
    print(f"      1. pip uninstall manim")
    print(f"      2. pip cache purge")
    print(f"      3. pip install manim --no-cache-dir")
    
except KeyboardInterrupt:
    print(f"\n   ⚠️ Test cancelled by user")
    
except Exception as e:
    print(f"   ❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
print("\n🧹 Cleaning up test files...")
if os.path.exists(test_file):
    os.remove(test_file)
    print(f"   ✅ Removed {test_file}")

print("\n" + "="*60)
print("🏁 DIAGNOSTIC COMPLETE")
print("="*60 + "\n")
