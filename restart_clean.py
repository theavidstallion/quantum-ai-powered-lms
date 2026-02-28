"""
Clean restart script - kills stuck processes and restarts Flask
Run this if video generation gets stuck: python restart_clean.py
"""
import subprocess
import sys
import time

print("="*60)
print("🧹 CLEANING UP STUCK PROCESSES")
print("="*60)

# Kill any stuck Python/Manim processes
print("\n1️⃣ Killing stuck Manim/Flask processes...")
try:
    # Kill Python processes (will kill current Flask)
    result = subprocess.run(
        ['taskkill', '/F', '/IM', 'python.exe'],
        capture_output=True,
        text=True
    )
    if "SUCCESS" in result.stdout:
        print("   ✅ Killed stuck processes")
    else:
        print("   ℹ️ No Python processes to kill")
except Exception as e:
    print(f"   ⚠️ Could not kill processes: {e}")

time.sleep(2)

# Clean up temp files
print("\n2️⃣ Cleaning temporary scene files...")
import os
temp_scene = 'output/videos/temp_scene.py'
if os.path.exists(temp_scene):
    try:
        os.remove(temp_scene)
        print(f"   ✅ Removed {temp_scene}")
    except:
        print(f"   ⚠️ Could not remove {temp_scene}")
else:
    print(f"   ℹ️ No temp files to clean")

# Option to restart Flask
print("\n3️⃣ Ready to restart!")
print("\n" + "="*60)
print("NOW RUN: python app.py")
print("="*60 + "\n")
