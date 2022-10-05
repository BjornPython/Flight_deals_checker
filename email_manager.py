import smtplib
from email.message import EmailMessage
import ssl


class SendMail:

    def __init__(self, my_email, my_pass, subject, body):
        self.my_email = my_email
        self.my_pass = my_pass
        self.email_receiver = [""]
        self.subject = subject

        self.em = EmailMessage()
        self.em["From"] = my_email
        self.em["Subject"] = subject
        self.em.set_content(body)
        self.context = ssl.create_default_context()

    def send_email(self, recipient):
        """Sends an email to the given recipient."""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
            connection.login(self.my_email, self.my_pass)
            connection.sendmail(self.my_email,
                                recipient,
                                self.em.as_string()
                                )


