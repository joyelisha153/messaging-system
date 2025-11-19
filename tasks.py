from celery_app import celery_app
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = "logs/app.log"

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)


def write_log(message: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


@celery_app.task(name="send_email_task")
def send_email_task(to_email: str):
    """Send email asynchronously via SMTP."""
    write_log(f"[EMAIL TASK START] To: {to_email} at {datetime.now()}")

    if not (SMTP_USER and SMTP_PASS):
        write_log("[EMAIL TASK ERROR] SMTP credentials not set in .env")
        return "SMTP credentials missing"

    msg = MIMEText("Hello from the messaging system via Celery & RabbitMQ!")
    msg["Subject"] = "Test Message"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        write_log(f"[EMAIL TASK SUCCESS] Email sent to {to_email}")
        return "Email sent"
    except Exception as e:
        write_log(f"[EMAIL TASK FAILED] Error: {e}")
        return f"Error: {e}"


@celery_app.task(name="log_time_task")
def log_time_task():
    """Log current server time."""
    now = datetime.now().isoformat()
    write_log(f"[TIME LOG] {now}")
    return now

