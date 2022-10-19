from pydantic import BaseSettings

from core.config import project_config


class MailAuth(BaseSettings):
    mail_user: str = project_config['email']['mail_user']
    mail_host: str = project_config['email']['mail_host']
    mail_port: int = project_config['email']['mail_port']

    class Config:
        frozen = True


mail_auth = MailAuth()

