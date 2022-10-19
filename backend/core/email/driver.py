import smtplib

from core.additional import singleton
from core.email.config import mail_auth


@singleton
class Mail:

    def __init__(self, gmail_user: str, host: str, port: int):
        try:
            self.user = gmail_user
            self.host = host
            self.port = port
            self.server = smtplib.SMTP(host=self.host, port=self.port)
        except Exception as e:
            print('error mail connection', e)
            exit()

    def send_message(self, to: str, subject: str, text: str):
        msg = f"""
            From: From Person <{self.user}>
            To: To Person <{to}>
            Subject: {subject}
        
            {text}
        """
        self.server.sendmail(self.user, to, msg)

    def __del__(self):
        self.server.close()


mail = Mail(mail_auth.mail_user, mail_auth.mail_host, mail_auth.mail_port)


