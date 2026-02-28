import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load credentials from .env file (SECURE)
load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
TARGET_EMAIL = os.getenv('SENDER_EMAIL')  # Send to yourself

if not SENDER_EMAIL or not SENDER_PASSWORD:
    print("❌ ERROR: Email credentials not found in .env file")
    print("Add these lines to your .env file:")
    print("SENDER_EMAIL=your_email@gmail.com")
    print("SENDER_PASSWORD=your_app_password_here")
    exit(1)

try:
    print("1. Connecting to Gmail...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    print("2. Logging in...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    print("3. Sending test message...")
    msg = MIMEText("If you see this, your App Password works!")
    msg['Subject'] = "QSAM Test Email"
    msg['From'] = SENDER_EMAIL
    msg['To'] = TARGET_EMAIL
    
    server.send_message(msg)
    server.quit()
    print("✅ SUCCESS! Email sent. Check your inbox.")

except Exception as e:
    print("\n❌ FAILED. Here is the error:")
    print(e)
    print("\nFIX:")
    print("- If error is 'Username and Password not accepted': Your App Password is wrong.")
    print("- If error is 'Please log in via your web browser': You are using your normal password (STOP). Use an App Password.")