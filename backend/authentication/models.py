import datetime
import uuid

from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey
from sqlmodel import SQLModel, Field
from sqlmodel.sql.sqltypes import GUID

from core.database.models import BaseModel
from user.models import UserDataBase


class UpdatePasswordSchema(SQLModel):
    password: str


class RecoveryPasswordSchema(SQLModel):
    email: EmailStr


class LoginUserSchema(SQLModel):
    username: str
    password: str


class BaseRefreshToken(BaseModel, table=True):
    user_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE")))
    time_out: datetime.datetime
