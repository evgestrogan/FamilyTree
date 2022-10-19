import uuid

from sqlalchemy.exc import ProgrammingError, StatementError
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.database.driver import get_session
from core.database.models import BaseModel


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
    async def get(select: Select | SelectOfScalar):
        result = await Crud.base_get(select)
        return result.first() if result is not None else None

    @staticmethod
    async def get_all(select: Select | SelectOfScalar) -> list:
        result = await Crud.base_get(select)
        return result.all() if result is not None else []

    @staticmethod
    async def save(database_object: BaseModel) -> uuid.UUID:
        async with get_session() as session:
            session.add(database_object)
            await session.commit()
            await session.refresh(database_object)
            return database_object.id

    @staticmethod
    async def delete(database_object: BaseModel) -> None:
        async with get_session() as session:
            await session.delete(database_object)
            await session.commit()


