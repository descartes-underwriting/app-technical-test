from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from pydantic_core import MultiHostUrl
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


class DatabaseConnectionError(Exception):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self) -> None:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        del self._engine, self._sessionmaker

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                raise DatabaseConnectionError(e)

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise DatabaseConnectionError(e)
        finally:
            await session.close()


db_url = settings.SQLALCHEMY_DATABASE_URI
if isinstance(db_url, MultiHostUrl):
    db_url = db_url.unicode_string()

sessionmanager = DatabaseSessionManager(db_url, {"echo": settings.ECHO_SQL_QUERIES})
