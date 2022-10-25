import smtplib

from core.additional import singleton
from core.config import project_config
from core.email.config import mail_auth


@singleton
class Mail:

    def __init__(self, gmail_user: str, host: str, port: int):
        self.user = gmail_user
        self.host = host
        self.port = port
        try:
            self.server = smtplib.SMTP(host=self.host, port=self.port)
        except Exception as e:
            if not project_config['test']:
                print('error mail connection', e)
                exit()
            else:
                self.server = None

    def send_message(self, to: str, subject: str, text: str):
        msg = f"""
            From: From Person <{self.user}>
            To: To Person <{to}>
            Subject: {subject}
        
            {text}
        """
        self.server.sendmail(self.user, to, msg)

    def __del__(self):
        if self.server is not None:
            self.server.close()


mail = Mail(mail_auth.mail_user, mail_auth.mail_host, mail_auth.mail_port)


