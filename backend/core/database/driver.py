from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database.config import database_url


engine = None


def init_db():
    global engine
    engine = create_async_engine(database_url, future=True)


def get_engine():
    global engine
    return engine


@asynccontextmanager
async def get_session() -> AsyncSession:
    try:
        async_session = sessionmaker(
            get_engine(), class_=AsyncSession
        )
        async with async_session() as session:
            yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


