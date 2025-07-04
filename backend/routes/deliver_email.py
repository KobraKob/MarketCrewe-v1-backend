from fastapi import APIRouter, Form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

email_router = APIRouter()

@email_router.post("/email")
def send_email(to_email: str = Form(...)):
    try:
        # Read content from the cleaned posts file
        with open("backend/delivery/weekly_posts_cleaned.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Email configurations from environment variables
        sender_email = os.getenv("EMAIL_USERNAME")
        sender_password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("EMAIL_HOST")
        smtp_port = int(os.getenv("EMAIL_PORT", 587)) # Default to 587 for TLS

        if not all([sender_email, sender_password, smtp_server]):
            return {"status": "error", "message": "Email configuration missing. Please set EMAIL_USERNAME, EMAIL_PASSWORD, and EMAIL_HOST in your .env file."}

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['Subject'] = "Your Generated Content from MarketCrew"

        # Attach the content as plain text
        msg.attach(MIMEText(content, 'plain'))

        # Send to multiple recipients
        recipients = [email.strip() for email in to_email.split(',') if email.strip()]
        if not recipients:
            return {"status": "error", "message": "No valid recipient email addresses provided."}
        msg['To'] = ", ".join(recipients)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return {"status": "success", "message": f"Email successfully sent to {to_email}!"}
    except FileNotFoundError:
        return {"status": "error", "message": "Cleaned weekly posts not found. Please generate content first."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}
