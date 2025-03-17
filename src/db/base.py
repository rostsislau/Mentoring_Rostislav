from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Импорт моделей, чтобы Alembic их видел
# from src.domain.task.models import Task
