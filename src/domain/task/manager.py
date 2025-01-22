from select import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Task


class TaskManager:
    model = Task

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, obj_id: int) -> Task | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.scalars(stmt)
        if not result:
            raise FileNotFoundError(f" Task with id {obj_id} not found")
        return result

    async def list(self, limit, offset) -> list[Task]:
        stmt = select(self.model).offset(offset).limit(limit)
        return await self.session.scalars(stmt)
