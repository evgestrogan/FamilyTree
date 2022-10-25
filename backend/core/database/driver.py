from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import project_config
from core.database.config import database_url


engine = create_async_engine(database_url, future=True, poolclass=NullPool if project_config['test'] else QueuePool)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


