from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from cache.engine import Base
import enum

class TaskStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN PROGRESS"
    RESOLVED = "RESOLVED"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#test