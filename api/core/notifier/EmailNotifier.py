from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from app.config import config
from app.user.domain.entity import User


class EmailNotifier:
    def __init__(self) -> None:
        self.sender_email: str = config.admin_email
        self.sender_password: str = config.admin_email_password

    def notify(self, receiver: User, subject: str, body: str) -> None:
        sender_email: str = self.sender_email
        sender_password: str = self.sender_password

        message: MIMEMultipart = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver.email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with SMTP_SSL(host="smtp.gmail.com", port=465) as server:
            server.login(user=sender_email, password=sender_password)
            server.send_message(msg=message)
