from datetime import datetime

from pydantic import BaseModel

from .models import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.NEW


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
