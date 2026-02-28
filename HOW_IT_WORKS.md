# 🎯 How Quantum LMS Works

## System Overview

Quantum LMS operates on a **multi-layered security and intelligence architecture** combining traditional web application patterns with advanced AI and quantum-inspired cryptography.

## End-to-End Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  USER REQUEST (Browser)                                      │
│  • Webcam capture → Face detection (OpenCV Haar Cascade)    │
│  • Credentials → Password verification (SQLite)             │
│  • Quantum Key → BB84 simulation verification               │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  FLASK BACKEND (Python)                                      │
│  • Session management → Secure Flask sessions                │
│  • Route handling → API endpoints                            │
│  • Database operations → SQLite with parameterized queries   │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  AI/ML SERVICES                                              │
│  • Chatbot → LangChain + Groq LLaMA 3.1                     │
│  • Video Gen → Manim + Groq LLaMA 3.3 + gTTS                │
│  • Sentiment → Lexicon-based NLP analysis                    │
│  • Anomaly → Isolation Forest (scikit-learn)                │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  RESPONSE (JSON/HTML)                                        │
│  • Dashboard → Real-time stats, grades, chatbot             │
│  • Admin Panel → Users, alerts, rankings, videos            │
│  • Downloads → Generated videos, reports                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow (3-Factor Security)

### Factor 1: Biometric Verification (Face Detection)

**Process:**
1. Browser requests webcam access via `navigator.mediaDevices.getUserMedia()`
2. Live video stream displayed to user
3. JavaScript captures single frame to `<canvas>` element
4. Frame converted to base64-encoded JPEG image
5. Sent to Flask server via POST request

**Server-side:**
```python
import cv2
import numpy as np

# Decode base64 image
img_bytes = base64.b64decode(image_data)
img_array = np.frombuffer(img_bytes, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces using Haar Cascade
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

if len(faces) > 0:
    # Face detected - proceed to next factor
    return "Face verified"
else:
    return "No face detected - please look at camera"
```

**Purpose:** Liveness check - confirms physical user presence, not just stolen credentials

---

### Factor 2: Credential Verification (Password)

**Process:**
```python
# Secure database lookup with parameterized query (SQL injection prevention)
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
user = cursor.fetchone()

if user and user[1] == entered_password:
    # Password matches
    session['user'] = username
    session['role'] = user[2]  # Student/Teacher/Admin
    return "Credentials verified"
else:
    # Log failed attempt for anomaly detection
    anomaly_detector.log_login_attempt(username, ip_address, success=False)
    return "Invalid credentials"
```

**Purpose:** Knowledge-based authentication - verifies user knows the secret password

---

### Factor 3: Quantum Key Exchange (BB84 Protocol)

**BB84 Simulation:**
```python
def generate_key(length=64):
    # Alice generates random bits
    alice_bits = [random.randint(0, 1) for _ in range(length * 2)]
    
    # Alice chooses random bases (X or Z)
    alice_bases = [random.choice(['X', 'Z']) for _ in range(length * 2)]
    
    # Bob chooses random bases independently
    bob_bases = [random.choice(['X', 'Z']) for _ in range(length * 2)]
    
    # Keep only bits where bases match (quantum principle)
    key = [str(alice_bits[i]) for i in range(len(alice_bits)) 
           if alice_bases[i] == bob_bases[i]][:length]
    
    return ''.join(key)  # e.g., "1011010110001101..."

# Generate and store in session
quantum_key = generate_key(length=64)
session['quantum_key'] = quantum_key
session['quantum_verified'] = False

# Send to client for display
return jsonify({'quantum_key': quantum_key})
```

**Client-side Verification:**
```javascript
// Modal displays quantum key automatically
document.getElementById('quantumKeyDisplay').textContent = quantum_key;

// User must copy and enter exact key
function verifyQuantumKey(entered_key) {
    fetch('/quantum_verify', {
        method: 'POST',
        body: JSON.stringify({ key: entered_key })
    })
    .then(response => {
        if (response.success) {
            window.location.href = '/dashboard';
        } else {
            alert('Invalid quantum key - please try again');
        }
    });
}
```

**Purpose:** Session binding - ensures the authenticated session wasn't hijacked

**Security Principle:** Quantum keys detect eavesdropping because measuring quantum states changes them (simulated here)

---

## 🤖 AI Chatbot Operation

### Technology Stack
- **Framework:** LangChain (Python LLM orchestration)
- **LLM Provider:** Groq Cloud (high-performance inference)
- **Model:** LLaMA 3.1-8b-instant (8 billion parameters)
- **Memory:** InMemoryChatMessageHistory (per-session storage)

### Conversation Flow

**1. User Input**
```javascript
// Student types message
const message = "Explain how gradient descent works";

// Sent to Flask backend
fetch('/chatbot', {
    method: 'POST',
    body: JSON.stringify({ message: message })
});
```

**2. Session Retrieval**
```python
# Each student has unique session ID
session_id = session.get('user', 'default')  # e.g., "student1"

# Retrieve conversation history
chat_history = self.chat_histories.get(session_id, InMemoryChatMessageHistory())
```

**3. Context Building**
```python
# System prompt sets assistant personality
system_prompt = """You are QUANTUM ASSISTANT, an educational AI tutor.
- Provide clear, step-by-step explanations
- Use encouraging language
- Break down complex topics into simple concepts
- Give examples to illustrate concepts
- Be patient and supportive"""

# Combine with user message and history
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_message),
    *chat_history.messages  # Previous context
]
```

**4. LLM Processing (Groq)**
```python
# Send to Groq with LLaMA 3.1 model
response = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    groq_api_key=os.getenv('GROQ_API_KEY')
).invoke(messages)

# Extract response
answer = response.content
```

**5. Memory Storage**
```python
# Save both user message and AI response for next turn
chat_history.add_user_message(user_message)
chat_history.add_ai_message(answer)

# Store updated history
self.chat_histories[session_id] = chat_history
```

**6. Response Delivery**
```python
# Return to frontend
return jsonify({'response': answer})
```

**Example Conversation:**
```
Turn 1:
User: "What is calculus?"
AI: "Calculus is the mathematical study of continuous change..."

Turn 2 (with memory):
User: "Give me an example"
AI: "Let's continue with calculus. A great example is finding the speed of a car..." 
     # AI remembers we were discussing calculus
```

---

## 🎬 AI Video Generation Pipeline

### Complete 6-Step Process

### Step 1: Topic Detection & Profile Selection

```python
def detect_topic_profile(topic):
    topic_lower = topic.lower()
    
    # Check keywords for each category
    if any(kw in topic_lower for kw in ['calculus', 'derivative', 'integral', 'matrix']):
        return TOPIC_PROFILES['math']
    elif any(kw in topic_lower for kw in ['force', 'energy', 'physics', 'momentum']):
        return TOPIC_PROFILES['physics']
    elif any(kw in topic_lower for kw in ['array', 'algorithm', 'sorting', 'tree']):
        return TOPIC_PROFILES['dsa']
    elif any(kw in topic_lower for kw in ['regression', 'neural', 'classification']):
        return TOPIC_PROFILES['ml']
    else:
        return TOPIC_PROFILES['default']
```

**Example:**
```
Input: "Pythagorean Theorem"
→ Detected: MATH category
→ Profile includes:
  - Formulas: ['a^2 + b^2 = c^2']
  - Visual style: Axes + animated triangle
  - Colors: BLUE=variables, YELLOW=constants, GREEN=result
```

---

### Step 2: Narration Script Generation

```python
def generate_narration_script(topic):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            'role': 'user',
            'content': f'''Write a clear 60-second educational narration 
                          script about "{topic}". Plain text only, no headers 
                          or bullet points. Make it engaging and suitable for 
                          a visual explainer video. Focus on key concepts, 
                          examples, and practical applications.'''
        }],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
```

**Output Example:**
```
"Welcome to this explainer on the Pythagorean Theorem. This fundamental 
mathematical relationship describes how the sides of a right triangle 
are connected. The theorem states that in a right triangle, the square 
of the hypotenuse equals the sum of squares of the other two sides. 
Let's visualize this concept with an animated example..."
```

---

### Step 3: Text-to-Speech Conversion

```python
def text_to_speech(script, filename):
    # Google Text-to-Speech API
    tts = gTTS(text=script, lang='en', slow=False)
    audio_path = os.path.join('output/videos', filename)
    tts.save(audio_path)
    
    # Estimate duration (average 150 words per minute)
    words = len(script.split())
    duration = (words / 150) * 60  # seconds
    
    return audio_path, duration  # e.g., "narration.mp3", 58.2
```

**Output:** `20260228_120000_audio.mp3` (~60 seconds)

---

### Step 4: Manim Animation Code Generation

```python
def generate_manim_code(topic, duration, visual_guide, formulas):
    system_prompt = f'''You are a Manim CE expert. Generate ONLY raw Python code.

RULES:
1. Class name: GeneratedVideo(Scene)
2. Start with: from manim import *\\nimport numpy as np
3. Duration: ~{duration:.0f} seconds total
4. LAYOUT (NO OVERLAP):
   - Title: .to_edge(UP) — short title only
   - Main: .move_to(ORIGIN) — diagram or graph
   - Formula: .to_edge(DOWN) — MathTex only
5. FadeOut(*self.mobjects) between stages
6. Use self.wait() to match audio timing

{visual_guide}

KEY FORMULAS TO SHOW:
{chr(10).join([f"  MathTex(r'{f}')" for f in formulas[:3]])}'''

    user_prompt = f'Topic: {topic}'
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0.5,
        max_tokens=2000
    )
    
    code = response.choices[0].message.content.strip()
    
    # Extract code from markdown if present
    if '```' in code:
        code = code.split('```python')[-1].split('```')[0].strip()
    
    return code
```

**Output Example:**
```python
from manim import *
import numpy as np

class GeneratedVideo(Scene):
    def construct(self):
        # Title
        title = Text("Pythagorean Theorem", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Main diagram - right triangle
        triangle = Polygon(
            ORIGIN, RIGHT*3, RIGHT*3+UP*4,
            color=BLUE
        ).move_to(ORIGIN)
        
        # Labels
        a_label = MathTex("a", color=YELLOW).next_to(triangle, DOWN)
        b_label = MathTex("b", color=YELLOW).next_to(triangle, RIGHT)
        c_label = MathTex("c", color=GREEN).next_to(triangle, LEFT+UP)
        
        self.play(Create(triangle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(2)
        
        # Formula
        formula = MathTex(r"a^2 + b^2 = c^2", font_size=40).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(3)
        
        self.play(FadeOut(*self.mobjects))
```

---

### Step 5: Manim Rendering

```bash
# Command executed by Python subprocess
python -m manim temp_scene.py GeneratedVideo \
    -ql \                        # Quality: low (480p) for speed
    --media_dir output/videos \  # Output directory
    --disable_caching            # Fresh render each time
```

**Process:**
1. Manim parses Python code
2. Renders each animation frame
3. Uses FFmpeg internally to create MP4
4. Saves to: `output/videos/videos/480p15/GeneratedVideo.mp4`

**Duration:** 30-120 seconds depending on complexity

**Output:** `animation.mp4` (480p, no audio)

---

### Step 6: Video + Audio Merging

```bash
# FFmpeg command executed by Python subprocess
ffmpeg -y \
    -i animation.mp4 \           # Video input
    -i narration.mp3 \           # Audio input
    -c:v copy \                  # Copy video codec (no re-encode)
    -c:a aac \                   # Encode audio to AAC
    -shortest \                  # End when shortest stream ends
    final_video.mp4              # Output file
```

**Result:** `20260228_120530_pythagorean_theorem.mp4`
- Duration: 60 seconds
- Resolution: 480p
- Audio: AAC codec, synchronized
- Size: ~5-10 MB

---

### Step 7: Database Tracking

```python
# Update video request status
cursor.execute("""
    UPDATE video_requests 
    SET status = 'completed',
        video_path = ?,
        script = ?,
        completed_at = ?
    WHERE id = ?
""", (final_path, script, datetime.now(), request_id))
```

**Status Flow:**
```
pending → processing → completed
           ↓
        failed (if error)
```

---

## 🔍 Anomaly Detection (Security)

### Algorithm: Isolation Forest

**How Isolation Forest Works:**
1. Randomly select a feature (e.g., time_of_day)
2. Randomly select split value between min and max
3. Partition data into two groups
4. Repeat recursively to build tree
5. Anomalies are isolated in fewer splits (shorter path length)

### Implementation

```python
from sklearn.ensemble import IsolationForest

class LoginBehaviorAnalyzer:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,    # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        
    def extract_features(self, login_attempt):
        return [
            login_attempt['hour'],                    # 0-23
            login_attempt['day_of_week'],             # 0-6
            login_attempt['failed_attempts_today'],   # Count
            hash(login_attempt['ip_address']) % 1000, # IP hash
            login_attempt['minutes_since_last']       # Time delta
        ]
    
    def train(self, historical_logins):
        features = [self.extract_features(login) for login in historical_logins]
        self.model.fit(features)
    
    def detect_anomaly(self, current_login):
        features = self.extract_features(current_login)
        prediction = self.model.predict([features])    # -1 or 1
        score = self.model.score_samples([features])  # Anomaly score
        
        if prediction[0] == -1:  # Anomaly detected
            self.create_alert(
                username=current_login['username'],
                alert_type="Suspicious Login Pattern",
                description=f"Unusual login from {current_login['ip_address']} at {current_login['time']}",
                severity="HIGH"
            )
            return True
        return False
```

### Real-world Example

**Normal Pattern for student1:**
- Logs in Mon-Fri between 9 AM - 5 PM
- From IP 192.168.1.100
- Success rate: 95%

**Anomaly Detected:**
- Login at 3 AM Sunday
- From IP 203.45.67.89 (different location)
- 5 failed attempts in 10 minutes

**System Action:**
```
Alert Created:
- Type: Unusual Login Time
- Severity: HIGH
- Description: Login at 03:14 AM from unfamiliar IP
- Action: Admin notified, account flagged for review
```

---

## 💭 Sentiment Analysis (NLP)

### Lexicon-Based Algorithm

```python
class SentimentAnalyzer:
    POSITIVE_WORDS = [
        'excellent', 'great', 'outstanding', 'brilliant', 'helpful',
        'smart', 'talented', 'dedicated', 'impressive', 'wonderful'
        # ... 70+ more words
    ]
    
    NEGATIVE_WORDS = [
        'poor', 'terrible', 'lazy', 'slow', 'careless', 'rude',
        'unprepared', 'disappointing', 'inadequate', 'weak'
        # ... 50+ more words
    ]
    
    INTENSIFIERS = {
        'very': 1.5, 'extremely': 2.0, 'incredibly': 2.0,
        'somewhat': 0.5, 'slightly': 0.3
    }
    
    def analyze(self, feedback_text):
        words = self.tokenize(feedback_text.lower())
        
        score = 0
        intensifier = 1.0
        
        for word in words:
            # Check for intensifiers
            if word in self.INTENSIFIERS:
                intensifier = self.INTENSIFIERS[word]
                continue
            
            # Check sentiment
            if word in self.POSITIVE_WORDS:
                score += 1.0 * intensifier
                intensifier = 1.0  # Reset
            elif word in self.NEGATIVE_WORDS:
                score -= 1.0 * intensifier
                intensifier = 1.0
        
        # Normalize to [-1, +1]
        normalized_score = math.tanh(score)
        
        # Classify
        if normalized_score > 0.3:
            label = "POSITIVE"
        elif normalized_score < -0.3:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        
        return {
            'score': normalized_score,
            'label': label,
            'confidence': abs(normalized_score)
        }
```

### Analysis Example

**Feedback:** "The student is very excellent and extremely helpful but slightly lazy"

**Processing:**
```
Tokens: ['student', 'is', 'very', 'excellent', 'extremely', 'helpful', 'but', 'slightly', 'lazy']

Step-by-step:
1. 'very' → intensifier = 1.5
2. 'excellent' → score += 1.0 * 1.5 = +1.5
3. 'extremely' → intensifier = 2.0
4. 'helpful' → score += 1.0 * 2.0 = +3.5
5. 'slightly' → intensifier = 0.3
6. 'lazy' → score -= 1.0 * 0.3 = +3.2

Normalized: tanh(3.2) = 0.996
Classification: POSITIVE (> 0.3)
Confidence: 99.6%
```

---

## 📊 Student Ranking System

### Ranking Formula

```
final_score = 0.7 * academic_score + 0.3 * sentiment_score

Where:
- academic_score: 0-4.0 (GPA scale)
- sentiment_score: 0-1.0 (normalized from -1 to +1)
```

### Calculation Process

**Step 1: Calculate Academic Score**
```python
def calculate_academic_score(student_id):
    grades = get_student_grades(student_id)
    
    # Convert letter grades to GPA
    gpa_map = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
               'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    
    total_gpa = sum(gpa_map.get(grade, 0) for grade in grades)
    academic_score = total_gpa / len(grades) if grades else 0
    
    return academic_score  # 0-4.0
```

**Step 2: Calculate Sentiment Score**
```python
def calculate_sentiment_score(student_id):
    feedback = get_student_feedback(student_id)
    
    if not feedback:
        return 0.5  # Neutral if no feedback
    
    # Analyze each feedback
    sentiments = [sentiment_analyzer.analyze(f) for f in feedback]
    avg_sentiment = sum(s['score'] for s in sentiments) / len(sentiments)
    
    # Normalize from [-1, +1] to [0, 1]
    normalized = (avg_sentiment + 1) / 2
    
    return normalized  # 0-1.0
```

**Step 3: Combine Scores**
```python
def calculate_final_score(academic_score, sentiment_score):
    final = (0.7 * academic_score / 4.0) + (0.3 * sentiment_score)
    return final  # 0-1.0
```

**Step 4: Assign Ranks**
```python
def update_rankings():
    students = get_all_students()
    
    # Calculate scores for each
    rankings = []
    for student in students:
        academic = calculate_academic_score(student.id)
        sentiment = calculate_sentiment_score(student.id)
        final = calculate_final_score(academic, sentiment)
        rankings.append((student.id, academic, sentiment, final))
    
    # Sort by final score (descending)
    rankings.sort(key=lambda x: x[3], reverse=True)
    
    # Assign rank positions
    for rank, (student_id, academic, sentiment, final) in enumerate(rankings, 1):
        save_ranking(
            student_id=student_id,
            rank_position=rank,
            academic_score=academic,
            sentiment_score=sentiment,
            final_score=final
        )
```

### Example Calculation

**Student A:**
- Grades: A, A-, B+, A → GPA: 3.75
- Feedback: 3 positive comments → Sentiment: 0.85
- Final Score: (0.7 × 3.75/4.0) + (0.3 × 0.85) = 0.656 + 0.255 = **0.911**
- Rank: **#1**

**Student B:**
- Grades: B, B-, B, C+ → GPA: 2.75
- Feedback: 2 neutral, 1 negative → Sentiment: 0.35
- Final Score: (0.7 × 2.75/4.0) + (0.3 × 0.35) = 0.481 + 0.105 = **0.586**
- Rank: **#2**

---

## 🗄️ Database Design Philosophy

### Core Principles

**1. Simplicity**
- SQLite for zero-configuration, file-based storage
- Single database file (`users.db`)
- No complex joins or foreign key constraints
- Easy to backup (just copy the file)

**2. Security**
- Parameterized queries prevent SQL injection
- No plain-text password storage (in production, would use bcrypt)
- Audit trail via `login_attempts` table
- Session management via Flask secure cookies

**3. Scalability**
- Designed for 100-1000 users (educational institution scale)
- SQLite handles up to 1 TB database size
- For larger scale, migration path to PostgreSQL exists
- Indexes on frequently queried columns (username, student_id)

### Table Relationships

```
users (username) ←─┬─ grades (student_id)
                   ├─ feedback (student)
                   ├─ student_rankings (student)
                   ├─ login_attempts (username)
                   ├─ anomaly_alerts (username)
                   └─ video_requests (username)
```

### Data Integrity

**Constraints:**
- PRIMARY KEY on all id/username columns
- UNIQUE constraint on student_rankings.student
- DEFAULT values for timestamps
- BOOLEAN fields for status flags

**Validation:**
- Application-level checks (not NULL)
- Type enforcement (INTEGER, TEXT, REAL, TIMESTAMP)
- Length limits in application code

---

## 🔄 Request-Response Cycle Examples

### Example 1: Student Viewing Dashboard

```
1. Browser → GET /dashboard
2. Flask checks session['user'] and session['quantum_verified']
3. If authorized:
   - Query grades for student
   - Query rankings for student
   - Render dashboard.html template with data
4. Browser receives HTML with embedded JavaScript
5. JavaScript loads chatbot interface
6. Dashboard displays with real-time data
```

### Example 2: Video Generation Request

```
1. Student clicks "Generate Video" button
2. JavaScript → POST /request_video with topic
3. Flask:
   - Validates session
   - Inserts row in video_requests (status='pending')
   - Spawns background thread
   - Returns request_id to client
4. Background thread:
   - Updates status to 'processing'
   - Calls video_generator.generate_video(topic)
   - Updates status to 'completed' with video_path
5. Client polls GET /my_videos every 10 seconds
6. When status=='completed', shows download button
7. User clicks → GET /download_video/123
8. Flask sends file via send_file()
```

### Example 3: Chatbot Conversation

```
1. Student types "What is recursion?" → Enter
2. JavaScript → POST /chatbot with message
3. Flask:
   - Retrieves session_id from session['user']
   - Loads chat history from memory
   - Calls chatbot.chat(message, session_id)
4. Chatbot:
   - Builds context with history + new message
   - Sends to Groq API
   - Waits for response
   - Saves to memory
   - Returns response
5. Flask → JSON response to client
6. JavaScript displays response in chat bubble
7. User sees answer appear with typing animation
```

---

## 🎓 Educational Value

### How This System Teaches

**1. Security Concepts:**
- Multi-factor authentication
- Biometric verification
- Quantum-inspired cryptography
- Anomaly detection
- Session management

**2. AI/ML Techniques:**
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Computer Vision
- Unsupervised Learning (Isolation Forest)
- Text-to-Speech synthesis

**3. Software Engineering:**
- RESTful API design
- MVC architecture (Model-View-Controller)
- Database normalization
- Async/background processing
- Error handling and logging

**4. Full-Stack Development:**
- Backend: Python/Flask
- Frontend: HTML/CSS/JavaScript
- Database: SQL/SQLite
- DevOps: Virtual environments, dependencies

---

## 📚 Further Reading

- **BB84 Protocol**: Original paper by Bennett & Brassard (1984)
- **Isolation Forest**: Liu, Ting, Zhou (2008) - "Isolation-based Anomaly Detection
"
- **LangChain Documentation**: https://python.langchain.com/docs/
- **Manim Community**: https://docs.manim.community/
- **Flask Documentation**: https://flask.palletsprojects.com/

---

**This document explains the internal workings of Quantum LMS. For setup instructions, see [README.md](README.md)**
