import uuid
from typing import Any

from sqlalchemy.exc import ProgrammingError, StatementError, IntegrityError
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.database.driver import get_session
from core.database.models import BaseModel
from core.exception.base_exeption import UniqueIndexException, ForeignKeyErrorException


class Crud:

    @staticmethod
    async def base_get(select: Select | SelectOfScalar):
        async with get_session() as session:
            try:
                result = await session.exec(select)
            except (ProgrammingError, StatementError):
                return None
            else:
                return result

    @staticmethod
    async def get(select: Select | SelectOfScalar) -> Any:
        result = await Crud.base_get(select)
        return result.first() if result is not None else None

    @staticmethod
    async def get_all(select: Select | SelectOfScalar) -> list:
        result = await Crud.base_get(select)
        return result.all() if result is not None else []

    @staticmethod
    async def save(database_object: BaseModel) -> uuid.UUID:
        async with get_session() as session:
            try:
                session.add(database_object)
                await session.commit()
            except IntegrityError as e:
                sqlstate = e.orig.sqlstate
                if sqlstate == '23505':
                    raise UniqueIndexException(e)
                elif sqlstate == '23503':
                    raise ForeignKeyErrorException(e)
                else:
                    raise e
            except Exception as e:
                raise e
            await session.refresh(database_object)
            return database_object.id

    @staticmethod
    async def delete(database_object: BaseModel) -> None:
        async with get_session() as session:
            await session.delete(database_object)
            await session.commit()


