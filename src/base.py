from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
import config


engine: AsyncEngine = create_async_engine(config.db.db_url)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()
