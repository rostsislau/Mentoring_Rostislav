from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schemas import TaskCreate, TaskUpdate
from .models import Task


async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int):
    return await db.get(Task, task_id)


async def update_task(db: AsyncSession, task_id: int, task: TaskUpdate):
    db_task = await db.get(Task, task_id)
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int):
    db_task = await db.get(Task, task_id)
    if  db_task:
        await db.delete(db_task)
        await db.commit()
        return True
    return False



