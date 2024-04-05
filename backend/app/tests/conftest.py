from collections.abc import AsyncGenerator, Generator
from contextlib import ExitStack
from typing import TypeVar

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import sessionmanager
from app.main import app as actual_app

T = TypeVar("T")

YieldFixture = Generator[T, None, None]
AsyncYieldFixture = AsyncGenerator[T, None]


@pytest.fixture(autouse=True)
def app() -> YieldFixture[FastAPI]:
    with ExitStack():
        yield actual_app


@pytest.fixture
async def client(app: FastAPI) -> AsyncYieldFixture[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://test",
    ) as c:
        yield c


@pytest.fixture(scope="function", autouse=True)
async def transactional_session() -> AsyncYieldFixture[AsyncSession]:
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await sessionmanager._engine.dispose()  # to deal with issues with connection pooling and async tests (https://github.com/tiangolo/fastapi/issues/1800#issuecomment-1260777088)
            await session.rollback()


@pytest.fixture(scope="function")
async def db_session(transactional_session: AsyncSession) -> AsyncYieldFixture[AsyncSession]:
    return transactional_session
