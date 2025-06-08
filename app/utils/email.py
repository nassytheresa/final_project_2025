import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD


def send_email(
    subject: str,
    body: str,
    to_emails: List[str] = ["nassytheresa@gmail.com"],
    from_email: Optional[str] = None,
    is_html: bool = False,
) -> bool:
    """
    Send an email using SMTP.

    Args:
        subject (str): Email subject
        body (str): Email body content
        to_emails (List[str]): List of recipient email addresses
        from_email (Optional[str]): Sender email address (defaults to SMTP_USERNAME from env)
        is_html (bool): Whether the body content is HTML (defaults to False)

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:

        if not all([SMTP_USERNAME, SMTP_PASSWORD]):
            raise ValueError("SMTP credentials not found in environment variables")

        # Create message
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_email or SMTP_USERNAME
        msg["To"] = ", ".join(to_emails)

        # Attach body
        content_type = "html" if is_html else "plain"
        msg.attach(MIMEText(body, content_type))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
