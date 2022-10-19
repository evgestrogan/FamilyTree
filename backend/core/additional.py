import os
from datetime import timedelta, datetime
from typing import Callable, Optional

from jose import jwt
from pydantic import BaseSettings

from core.config import project_config, applications


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class BaseUrlConfig(BaseSettings):
    tags: list
    name: str
    description: str
    response_model: Callable
    status_code: int

    class Config:
        frozen = True


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, project_config['authentication']['secret_key'], algorithm='HS256')
    return token


def decode_token(token: str) -> dict:
    return jwt.decode(token, project_config['authentication']['secret_key'], algorithms='HS256')


def get_models():
    models = []
    for app in applications:
        if 'models.py' in os.listdir(app):
            models.append(f"{app}.models")
    return models
