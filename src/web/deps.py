from db.base import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from domain.task.service import TaskService


async def get_db_session():
    async with get_async_db() as session:
        yield session


async def get_task_service(
    db_session: AsyncSession = Depends(get_async_db)):
    return TaskService(db_session)

