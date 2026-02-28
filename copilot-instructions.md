> I have a Flask-based LMS (Learning Management System) project called **Quantum-**. I need you to build a complete, working frontend for it using only **HTML, CSS, and vanilla JavaScript**. The backend is Python/Flask and is already partially written. Read the full context below carefully before writing any code.
>
> ---
>
> ## 📁 Current Project Structure
>
> ```
> Quantum-/
> ├── app.py                    ← Main Flask app (partially written, needs fixes)
> ├── bb84.py                   ← Quantum key simulation
> ├── anomaly_detector.py       ← ML login anomaly detection (Isolation Forest)
> ├── sentiment_analyzer.py     ← NLP sentiment analyzer + student ranker
> ├── lms_chatbot.py            ← LangChain + Groq chatbot (Colab script, needs refactoring)
> ├── users.db                  ← SQLite database (DO NOT modify or regenerate)
> ├── .env                      ← API keys and secrets (already created)
> ├── requirements.txt          ← Dependencies (already created)
> ├── templates/
> │   ├── login.html            ← Exists but needs fixing
> │   ├── dashboard.html        ← Exists but needs fixing
> │   └── admin_panel.html      ← Exists but needs fixing
> └── static/
>     ├── css/
>     └── js/
> ```
>
> ---
>
> ## 🗄️ Database Schema (DO NOT TOUCH `users.db`)
>
> The SQLite database already exists and has real data. Do not drop, recreate, or modify any tables. The schema is:
>
> ```sql
> -- Already exists with data
> CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, role TEXT, email TEXT);
> CREATE TABLE feedback (id INTEGER, student TEXT, teacher TEXT, rating INTEGER, comment TEXT, date TEXT);
> CREATE TABLE grades (id INTEGER, student_id TEXT, course TEXT, assessment TEXT, score TEXT, grade TEXT);
> CREATE TABLE student_rankings (id INTEGER, student TEXT UNIQUE, academic_score REAL, sentiment_score REAL, final_score REAL, rank_position INTEGER, sentiment_label TEXT, feedback_count INTEGER, last_updated TIMESTAMP);
> CREATE TABLE login_attempts (id INTEGER, username TEXT, timestamp TIMESTAMP, ip_address TEXT, success BOOLEAN, face_detected BOOLEAN, is_anomaly BOOLEAN, anomaly_score REAL, location TEXT);
> CREATE TABLE anomaly_alerts (id INTEGER, username TEXT, alert_time TIMESTAMP, alert_type TEXT, description TEXT, severity TEXT, resolved BOOLEAN);
> ```
>
> Default admin credentials already in the DB: `username: admin`, `password: admin123`
>
> ---
>
> ## 🔧 Task 1 — Fix and Complete `app.py`
>
> The existing `app.py` is incomplete. Rewrite it fully with these requirements:
>
> - Load secrets from `.env` using `python-dotenv` — replace all hardcoded keys/passwords
> - Keep `init_db()` but change it so it **never drops existing tables** — use `CREATE TABLE IF NOT EXISTS` only, no `DROP TABLE`, no deleting existing data
> - Fix template names: use `dashboard.html` and `admin_panel.html` (not `dashboard_updated.html` or `admin_panel_updated.html`)
> - Add ALL missing routes:
>
> ```python
> GET  /                    → render login.html
> POST /login               → face check + password check + quantum key generation
> POST /quantum_verify      → verify the quantum key, set session['quantum_verified'] = True
> GET  /dashboard           → student dashboard (requires quantum_verified session)
> GET  /admin_panel         → admin panel (requires Admin role)
> POST /chatbot             → call StudentChatbot.chat(), return JSON response
> POST /submit_feedback     → insert feedback into DB
> POST /update_rankings     → call student_ranker.save_rankings_to_db()
> GET  /anomaly_alerts      → return JSON list of unresolved anomaly alerts
> POST /resolve_alert       → mark an alert as resolved (set resolved=1)
> GET  /logout              → clear session, redirect to /
> ```
>
> - Import `.env` variables like this:
> ```python
> from dotenv import load_dotenv
> load_dotenv()
> SENDER_EMAIL = os.getenv('SENDER_EMAIL')
> SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
> app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret')
> ```
>
> ---
>
> ## 🤖 Task 2 — Create `chatbot.py` (New File)
>
> The existing `lms_chatbot.py` is a Colab notebook script. It cannot run inside Flask. Create a **new file** called `chatbot.py` in the project root that:
>
> - Defines a `StudentChatbot` class with a `chat(self, message, session_id)` method
> - Defines a `ChatHistory` class (can be a simple placeholder class)
> - Uses LangChain + Groq with the `llama-3.1-8b-instant` model
> - Loads `GROQ_API_KEY` from environment variables using `os.getenv('GROQ_API_KEY')`
> - Uses `InMemoryChatMessageHistory` for per-session conversation memory
> - Uses this exact system prompt for the chatbot persona:
>
> ```
> You are QUANTUM ASSISTANT, a helpful academic assistant for university students.
> Help with: grades, courses, study tips, academic questions, and university life.
> Be friendly, supportive, and encouraging. Keep responses concise and clear.
> If asked about math or science, explain step by step.
> End every response with a short encouraging line.
> ```
>
> - Auto-detects subject type from keywords:
>   - math/algebra/calculus/equation → prepend "Solve step by step: " to message
>   - science/physics/chemistry → no change but note the subject
> - Returns the response as a plain string from the `chat()` method
> - Does NOT use `!pip install`, `input()`, `print()`, or any Colab-specific code
>
> Example usage that `app.py` will use:
> ```python
> from chatbot import StudentChatbot, ChatHistory
> chatbot = StudentChatbot()
> response = chatbot.chat("What is Newton's first law?", session_id="student_123")
> ```
>
> ---
>
> ## 🎨 Task 3 — Build the Frontend (HTML/CSS/JS)
>
> Create or fully rewrite these files. Use a **dark quantum/cyberpunk theme** with these CSS variables:
>
> ```css
> :root {
>   --bg-dark: #050510;
>   --bg-card: #0d0d2b;
>   --bg-card2: #111135;
>   --accent-cyan: #00e5ff;
>   --accent-purple: #7c3aed;
>   --accent-green: #22c55e;
>   --accent-red: #ef4444;
>   --accent-yellow: #f59e0b;
>   --text-primary: #e2e8f0;
>   --text-muted: #94a3b8;
>   --border: #1e2a4a;
>   --glow-cyan: 0 0 20px rgba(0, 229, 255, 0.3);
>   --glow-purple: 0 0 20px rgba(124, 58, 237, 0.3);
> }
> ```
>
> Put shared styles in `static/css/style.css` and shared JS in `static/js/main.js`.
>
> ---
>
> ### Page 1 — `templates/login.html`
>
> Fully rewrite this page. It must:
>
> **Layout:**
> - Centered card on a dark animated background (subtle particle effect or CSS gradient animation)
> - Logo/title at top: "🔐 QUANTUM LMS"
> - Username and password input fields
> - Live webcam preview box (small, 200x150px) with a label "Face Verification Active"
> - A "LOGIN" button
> - A status message area below the button
>
> **JavaScript behavior (`/static/js/login.js`):**
> 1. On page load: call `navigator.mediaDevices.getUserMedia({ video: true })` and show the live webcam feed in a `<video>` element
> 2. On LOGIN button click:
>    - Draw the current video frame onto a hidden `<canvas>` element
>    - Convert canvas to base64 string: `canvas.toDataURL('image/jpeg')`
>    - POST to `/login` as JSON: `{ username, password, image: base64string }`
>    - Show a loading spinner on the button during the request
> 3. On response from `/login`:
>    - If `success: false` → show `message` in red status area, shake the card
>    - If `success: true` → show a **Quantum Key Verification modal/overlay**:
>      - Display: "🔑 Your Quantum Key:" followed by the key in a monospace box
>      - An input field: "Enter the key to verify your identity"
>      - A "VERIFY" button
>      - On VERIFY click: POST `{ key: enteredKey }` to `/quantum_verify`
>      - If verified: `window.location.href = '/dashboard'`
>      - If not: show "Invalid quantum key" error
>
> **Visual details:**
> - Webcam box has a cyan glowing border that pulses
> - Input fields have a dark background with cyan border on focus
> - LOGIN button is cyan with a hover glow effect
> - If face check fails, the webcam border turns red
>
> ---
>
> ### Page 2 — `templates/dashboard.html`
>
> Fully rewrite this page. It must:
>
> **Layout (sidebar + main content):**
> - Left sidebar (fixed, 220px wide, dark background):
>   - User avatar (initials circle, cyan background)
>   - Username and role displayed
>   - Navigation links: Dashboard, My Grades, Chatbot, Feedback, Logout
> - Main content area with these sections:
>
> **Section A — Stats Bar (top row of 4 cards):**
> - Total Courses (count from grades)
> - Current Rank (from `ranking[0]` passed from Flask)
> - Final Score (from `ranking[1]`)
> - Sentiment Label (from `ranking[2]`) — color coded: green=positive, red=negative, yellow=neutral
> - Display "Not ranked yet" if ranking is None
>
> **Section B — My Grades Table:**
> - Table with columns: Course, Assessment, Score, Grade
> - Grade column color coded: A=green, B=cyan, C=yellow, D/F=red
> - Populate from the `grades` Jinja2 variable: `{% for grade in grades %}`
>
> **Section C — Chatbot Widget (most important section):**
> - Full-width chat interface card with title "🤖 Quantum Assistant"
> - Chat message display area (scrollable, min 350px height, dark background)
> - User messages aligned right (cyan bubble), bot messages aligned left (dark purple bubble)
> - Input bar at bottom with a text input and a "Send" button
> - A "typing..." indicator that shows while waiting for response
> - On page load: show a welcome message from the bot: "Hello [username]! I'm your Quantum Assistant. How can I help you today?"
> - On Send (or Enter key):
>   - Append user message to chat
>   - Show typing indicator
>   - POST `{ message: userText }` to `/chatbot`
>   - Remove typing indicator, append bot response
>   - Auto-scroll to bottom after each message
>
> **Section D — Submit Feedback (for teachers):**
> - Simple form: Teacher name dropdown (hardcoded: Dr. Fatima Tariq, Mr. Zunnurain, Ms. Ayesha), star rating (1-5), comment textarea
> - Submit button: POST `{ teacher, rating, comment }` to `/submit_feedback`
> - Show success/error message after submit
>
> **Security info bar (bottom of page):**
> - Show: "🌐 Your IP: {{ ip }}" and "🔒 Quantum Session Active"
>
> ---
>
> ### Page 3 — `templates/admin_panel.html`
>
> Fully rewrite this page. It must:
>
> **Layout (same sidebar + main structure as dashboard):**
> - Sidebar navigation: Overview, Users, Rankings, Alerts, Courses, Feedback, Logout
>
> **Section A — Overview Stats (top row of 4 cards):**
> - Total Users
> - Total Feedback
> - Active Alerts (count of unresolved anomaly alerts)
> - Total Students Ranked
>
> **Section B — Anomaly Alerts Panel (most prominent section):**
> - Title: "🚨 Security Alerts" with a red badge showing the count of unresolved alerts
> - For each alert from `alerts` (Jinja2 loop):
>   - Card showing: username, alert_type, description, alert_time, severity badge
>   - Severity badge color: high=red, medium=yellow, low=green
>   - A "✓ Resolve" button per alert
>   - On Resolve click: POST `{ alert_id: id }` to `/resolve_alert`, remove the card from DOM on success
> - If no alerts: show "✅ No active security alerts"
>
> **Section C — Student Rankings Table:**
> - Table: Rank, Student, Academic Score, Sentiment Score, Final Score, Sentiment Label, Last Updated
> - Row highlight: rank 1=gold, rank 2=silver, rank 3=bronze
> - "🔄 Refresh Rankings" button at the top right — POST to `/update_rankings`, reload the table on success
>
> **Section D — All Users Table:**
> - Table: Username, Role, Email, Actions
> - Role badge: Admin=purple, Student=cyan, Teacher=green
>
> **Section E — Feedback Table:**
> - Table: Student, Teacher, Rating (show stars ⭐), Comment, Date
>
> **Section F — Courses & Grades:**
> - Two sub-panels side by side:
>   - Courses list (from `courses`)
>   - Recent grades (from `grades`)
>
> ---
>
> ## 📐 General Frontend Rules
>
> 1. **No external CDN dependencies** — write pure CSS and JS only. No Bootstrap, no jQuery, no Tailwind, no external fonts.
> 2. **All pages must be fully responsive** — work on screens 768px and wider.
> 3. **Flask template syntax** — use `{{ variable }}`, `{% for %}`, `{% if %}` correctly in the HTML files. Reference static files with `{{ url_for('static', filename='css/style.css') }}`.
> 4. **All fetch() calls must use `Content-Type: application/json`** and handle both success and error responses.
> 5. **No page reloads for chatbot, feedback, resolve alert, or refresh rankings** — all must be async with fetch().
> 6. **Session protection** — if a user is not logged in (not `quantum_verified`), they must be redirected to `/`. The Flask backend handles this — the frontend just needs to handle `401` or redirect responses gracefully.
> 7. **Do not modify `users.db`** at any point in this process.
>
> ---
>
> ## 🔄 Complete Flow Summary
>
> ```
> / (login page)
>  → webcam captures face
>  → POST /login → face check (OpenCV) + password check (SQLite) + BB84 key gen
>  → quantum key modal appears
>  → POST /quantum_verify → session['quantum_verified'] = True
>  → redirect to /dashboard (students) or /admin_panel (admin)
>
> /dashboard
>  → shows grades, ranking, IP
>  → chatbot widget → POST /chatbot → LangChain + Groq → response
>  → feedback form → POST /submit_feedback → insert to DB
>
> /admin_panel
>  → shows all users, feedback, rankings, alerts
>  → resolve alert → POST /resolve_alert → DB update
>  → refresh rankings → POST /update_rankings → recalculate + save to DB
>
> /logout → clear session → redirect to /
> ```
>
> ---
>
> ## ✅ Deliverables
>
> Create or modify exactly these files:
>
> 1. `app.py` — fixed and completed Flask backend
> 2. `chatbot.py` — new file, Flask-compatible chatbot class
> 3. `templates/login.html` — full rewrite
> 4. `templates/dashboard.html` — full rewrite
> 5. `templates/admin_panel.html` — full rewrite
> 6. `static/css/style.css` — shared styles
> 7. `static/js/main.js` — shared utilities
> 8. `static/js/login.js` — login page specific JS
>
> Do NOT modify: `bb84.py`, `anomaly_detector.py`, `sentiment_analyzer.py`, `lms_chatbot.py`, `users.db`, `.env`, `requirements.txt`
