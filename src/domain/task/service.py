from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from domain.task.models import Task
from domain.task.schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj: TaskCreate):
        task = Task(**obj.dict())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get(self, obj_id: int):
        task = await self.db.get(Task, obj_id)
        if not task:
            raise NoResultFound
        return task

    async def get_all(self, skip: int = 0, limit: int = 10):
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, obj_id: int, obj: TaskUpdate):
        task = await self.get(obj_id)
        for key, value in obj.dict(exclude_unset=True).items():
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, obj_id: int):
        task = await self.get(obj_id)
        await self.db.delete(task)
        await self.db.commit()
