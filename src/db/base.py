from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from config import config


engine: AsyncEngine = create_async_engine(config.db.db_url)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
