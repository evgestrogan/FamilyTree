from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from core.database.models import BaseModel


class BaseUserSchema(SQLModel):
    username: str
    email: EmailStr = Field(unique=True)


class UserSchemaGet(BaseModel, BaseUserSchema):
    active: bool = Field(default=False)


class UserSchemaCreate(BaseUserSchema):
    password: str


class UserDataBase(UserSchemaGet, table=True):
    password: bytes


class UpdateUserSchema(SQLModel):
    username: str | None
    email: EmailStr | None
    password: str | None
