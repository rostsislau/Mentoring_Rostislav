import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.engine import engine

# Создаём отдельный sessionmaker (НЕ использует глобальный AsyncSessionLocal)
TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """Создаёт один event loop на всю сессию тестов (избегает проблем с asyncpg)."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Создаёт новую сессию для каждого теста и откатывает изменения после теста."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()  # Откатываем изменения
