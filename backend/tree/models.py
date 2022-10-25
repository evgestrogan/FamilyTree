import datetime
import uuid
from datetime import date
from typing import List

from sqlalchemy import Column, ForeignKey
from sqlmodel import SQLModel, Field
from sqlmodel.sql.sqltypes import GUID

from core.database.models import BaseModel
from user.models import UserDataBase


class BasePartners(SQLModel):
    husband_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))
    wife_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))

    wedding_date: datetime.date | None
    divorce_date: datetime.date | None


class PartnersMapper(BaseModel, BasePartners, table=True):
    pass


class PartnersGet(SQLModel):
    partner_id: uuid.UUID

    wedding_date: datetime.date | None
    divorce_date: datetime.date | None


class UserNodeMapper(BaseModel, SQLModel, table=True):
    user_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE")))
    node_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))


class BaseNodeSchema(SQLModel):
    name: str
    family_name: str
    old_family_name: str | None
    father_name: str | None
    birthday: date | None
    death_date: date | None
    photo: str | None
    information: str | None

    user_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE"), unique=True))

    father_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id'), nullable=True))
    mother_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id'), nullable=True))


class NodeDataBase(BaseModel, BaseNodeSchema, table=True):
    author_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE"), nullable=False))


class NodeSchemaGet(BaseNodeSchema):
    author_id: uuid.UUID

    partners: List[PartnersGet]


class NodeSchemaUpdate(BaseNodeSchema):
    name: str | None
    family_name: str | None











