import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailSender:
    def __init__(self):
        self.client = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        self.from_email = os.environ.get("EMAIL_FROM", "english-daily@study.com")

    def send(self, to_email: str, subject: str, html_content: str) -> bool:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        response = self.client.send(message)
        success = response.status_code in (200, 201, 202)
        if success:
            print(f"Email sent successfully to {to_email}")
        else:
            print(f"Email send failed: status {response.status_code}")
        return success
