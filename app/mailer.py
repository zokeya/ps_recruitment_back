import smtplib
from email.mime.text import MIMEText

from app.config import settings

smtp_server = settings.smtp_server
smtp_port = settings.smtp_port
sender_email = settings.sender_email
sender_password = settings.sender_password
server_url = settings.server_url


def send_password_reset_email(email: str, reset_token: str):
    subject = "Password Reset"
    body = f"Click the following link to reset your password: {server_url}/reset-password?token={reset_token}"
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [email], message.as_string())
