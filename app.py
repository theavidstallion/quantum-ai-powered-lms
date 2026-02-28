from flask import Flask, render_template, jsonify, request, redirect, url_for, session, send_file
import cv2
import base64
import numpy as np
import socket
import sqlite3
import os
import threading
from datetime import datetime
from dotenv import load_dotenv
from bb84 import generate_key
from sentiment_analyzer import SentimentAnalyzer, StudentRanker
from anomaly_detector import LoginBehaviorAnalyzer
from chatbot import StudentChatbot
from video_generator import VideoGenerator

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-quantum-secret-2026')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

failed_attempts = {}
sentiment_analyzer = SentimentAnalyzer()
student_ranker = StudentRanker()
anomaly_detector = LoginBehaviorAnalyzer()
anomaly_detector.init_db()
chatbot = StudentChatbot()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video_generator = VideoGenerator(GROQ_API_KEY) if GROQ_API_KEY else None

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT, email TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, student TEXT, teacher TEXT, rating INTEGER, comment TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, course TEXT, assessment TEXT, score TEXT, grade TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS student_rankings (id INTEGER PRIMARY KEY AUTOINCREMENT, student TEXT UNIQUE, academic_score REAL, sentiment_score REAL, final_score REAL, rank_position INTEGER, sentiment_label TEXT, feedback_count INTEGER, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS login_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ip_address TEXT, success BOOLEAN, face_detected BOOLEAN, is_anomaly BOOLEAN DEFAULT 0, anomaly_score REAL, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS anomaly_alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, alert_type TEXT, description TEXT, severity TEXT, resolved BOOLEAN DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS video_requests (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, topic TEXT, description TEXT, status TEXT DEFAULT 'pending', video_path TEXT, script TEXT, requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, completed_at TIMESTAMP, error_message TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    u, p = data['username'], data['password']
    img_data = data.get('image', '').split(',')[1] if 'image' in data else None
    ip_address = request.remote_addr or 'unknown'

    if not img_data:
        return jsonify({'success': False, 'message': 'Camera blocked or image missing.'})

    img_bytes = base64.b64decode(img_data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        anomaly_detector.log_login_attempt(u if 'u' in locals() else 'unknown', ip_address, False, False)
        return jsonify({'success': False, 'message': 'FACE CHECK FAILED: Look at the camera.'})

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (u,))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    if user[1] == p:
        anomaly_detector.log_login_attempt(u, ip_address, True, True)
        qkey = generate_key(length=64)['key']
        session['quantum_key'] = qkey
        session['quantum_verified'] = False
        session['user'] = u
        session['role'] = user[2]
        failed_attempts[u] = 0
        return jsonify({'success': True, 'quantum_key': qkey})
    else:
        failed_attempts[u] = failed_attempts.get(u, 0) + 1
        anomaly_detector.log_login_attempt(u, ip_address, False, True)
        msg = "Wrong Password" if failed_attempts[u] < 3 else "Multiple failed attempts detected!"
        if failed_attempts[u] >= 3:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO anomaly_alerts (username, alert_type, description, severity) VALUES (?, ?, ?, ?)",
                     (u, 'Failed Login', f'3+ failed attempts from {ip_address}', 'high'))
            conn.commit()
            conn.close()
            failed_attempts[u] = 0
        return jsonify({'success': False, 'message': msg})

@app.route('/quantum_verify', methods=['POST'])
def quantum_verify():
    data = request.json
    entered_key = data.get('key', '')
    if 'quantum_key' in session and entered_key == session['quantum_key']:
        session['quantum_verified'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid quantum key'})

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or not session.get('quantum_verified'):
        return redirect(url_for('home'))
    if session['role'] == 'Admin':
        return redirect(url_for('admin_panel'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT course, assessment, score, grade FROM grades WHERE student_id = ?", (session['user'],))
    grades = c.fetchall()
    c.execute("SELECT rank_position, final_score, sentiment_label FROM student_rankings WHERE student = ?", (session['user'],))
    ranking = c.fetchone()
    conn.close()
    
    return render_template('dashboard.html', 
                         username=session['user'], 
                         role=session['role'], 
                         grades=grades, 
                         ip=request.remote_addr or 'unknown', 
                         ranking=ranking)

@app.route('/admin_panel')
def admin_panel():
    if 'user' not in session or session['role'] != 'Admin':
        return redirect(url_for('home'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    users = c.execute("SELECT * FROM users").fetchall()
    feedback = c.execute("SELECT * FROM feedback ORDER BY date DESC").fetchall()
    rankings = c.execute("SELECT * FROM student_rankings ORDER BY rank_position").fetchall()
    alerts = c.execute("SELECT * FROM anomaly_alerts WHERE resolved = 0 ORDER BY alert_time DESC").fetchall()
    grades = c.execute("SELECT * FROM grades LIMIT 20").fetchall()
    courses = [("CS401", "Final Year Project II"), ("CS305", "Information Security"), ("MG101", "Professional Practices")]
    conn.close()
    
    return render_template('admin_panel.html', 
                         users=users, 
                         feedback=feedback, 
                         courses=courses, 
                         grades=grades, 
                         rankings=rankings, 
                         alerts=alerts)

@app.route('/chatbot', methods=['POST'])
def chatbot_route():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    message = data.get('message', '')
    session_id = session.get('user', 'default')
    response = chatbot.chat(message, session_id)
    return jsonify({'response': response})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.json
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (student, teacher, rating, comment, date) VALUES (?, ?, ?, ?, ?)",
             (session['user'], data['teacher'], data['rating'], data['comment'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/update_rankings', methods=['POST'])
def update_rankings():
    if 'user' not in session or session['role'] != 'Admin':
        return jsonify({'success': False}), 401
    try:
        student_ranker.save_rankings_to_db()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/anomaly_alerts')
def anomaly_alerts():
    if 'user' not in session or session['role'] != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 401
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    alerts = c.execute("SELECT * FROM anomaly_alerts WHERE resolved = 0 ORDER BY alert_time DESC").fetchall()
    conn.close()
    return jsonify([{
        'id': a[0], 'username': a[1], 'alert_time': a[2], 
        'alert_type': a[3], 'description': a[4], 'severity': a[5]
    } for a in alerts])

@app.route('/resolve_alert', methods=['POST'])
def resolve_alert():
    if 'user' not in session or session['role'] != 'Admin':
        return jsonify({'success': False}), 401
    data = request.json
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE anomaly_alerts SET resolved = 1 WHERE id = ?", (data['alert_id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/request_video', methods=['POST'])
def request_video():
    """Student requests a video generation"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.json
    topic = data.get('topic', '').strip()
    description = data.get('description', '').strip()
    
    if not topic:
        return jsonify({'success': False, 'message': 'Topic is required'})
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO video_requests (username, topic, description, status) VALUES (?, ?, ?, ?)",
             (session['user'], topic, description, 'pending'))
    request_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # Start video generation in background thread
    if video_generator:
        thread = threading.Thread(target=generate_video_background, args=(request_id,))
        thread.daemon = True
        thread.start()
    
    return jsonify({'success': True, 'request_id': request_id, 'message': 'Video generation started!'})

def generate_video_background(request_id):
    """Background task to generate video"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        # Get request details
        c.execute("SELECT topic, description FROM video_requests WHERE id = ?", (request_id,))
        row = c.fetchone()
        if not row:
            return
        
        topic, description = row
        
        # Update status to processing
        c.execute("UPDATE video_requests SET status = ? WHERE id = ?", ('processing', request_id))
        conn.commit()
        
        # Generate video
        success, video_path, script, error = video_generator.generate_video(topic)
        
        if success:
            c.execute("UPDATE video_requests SET status = ?, video_path = ?, script = ?, completed_at = ? WHERE id = ?",
                     ('completed', video_path, script, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request_id))
        else:
            c.execute("UPDATE video_requests SET status = ?, error_message = ? WHERE id = ?",
                     ('failed', error, request_id))
        conn.commit()
    except Exception as e:
        c.execute("UPDATE video_requests SET status = ?, error_message = ? WHERE id = ?",
                 ('failed', str(e), request_id))
        conn.commit()
    finally:
        conn.close()

@app.route('/my_videos')
def my_videos():
    """Get user's video requests"""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, topic, description, status, requested_at, completed_at, error_message FROM video_requests WHERE username = ? ORDER BY requested_at DESC",
             (session['user'],))
    videos = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': v[0],
        'topic': v[1],
        'description': v[2],
        'status': v[3],
        'requested_at': v[4],
        'completed_at': v[5],
        'error_message': v[6]
    } for v in videos])

@app.route('/all_video_requests')
def all_video_requests():
    """Admin view of all video requests"""
    if 'user' not in session or session['role'] != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username, topic, description, status, requested_at, completed_at FROM video_requests ORDER BY requested_at DESC LIMIT 50")
    videos = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': v[0],
        'username': v[1],
        'topic': v[2],
        'description': v[3],
        'status': v[4],
        'requested_at': v[5],
        'completed_at': v[6]
    } for v in videos])

@app.route('/download_video/<int:video_id>')
def download_video(video_id):
    """Download completed video"""
    if 'user' not in session:
        return redirect(url_for('home'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT video_path, username, topic FROM video_requests WHERE id = ?", (video_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return "Video not found", 404
    
    video_path, owner, topic = row
    
    # Check permission (owner or admin)
    if session['user'] != owner and session['role'] != 'Admin':
        return "Unauthorized", 403
    
    if not video_path or not os.path.exists(video_path):
        return "Video file not found", 404
    
    return send_file(video_path, as_attachment=True, download_name=f"{topic.replace(' ', '_')}.mp4")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # IMPORTANT: Use use_reloader=False to prevent Flask from killing
    # background video generation subprocess when files change
    # For development, you can manually restart after code changes
    app.run(
        debug=True,
        use_reloader=False  # Disable auto-reload to prevent subprocess interruption
    )