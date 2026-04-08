import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

def send_otp_email(to_email: str, otp: str) -> bool:
    if not SMTP_USERNAME and SMTP_SERVER != 'localhost':
        print("WARNING: SMTP credentials not provided. OTP not sent via email. OTP:", otp)
        return False
        
    msg = EmailMessage()
    msg.set_content(f"Hello,\n\nYour OTP for password reset is: {otp}\n\nThis OTP will expire in 1 hour. Do not share it with anyone.")
    
    msg['Subject'] = 'Password Reset OTP - Dependency Scanner'
    msg['From'] = SMTP_USERNAME if SMTP_USERNAME else "noreply@localhost"
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_SERVER != 'localhost' and SMTP_PORT != 1025:
                server.starttls()
            if SMTP_USERNAME and SMTP_PASSWORD:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"OTP successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
