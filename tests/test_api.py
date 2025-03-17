import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.engine import AsyncSessionLocal
from src.domain.task.models import Task


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Создаёт новую сессию для каждого теста и откатывает изменения после теста."""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest.mark.asyncio
async def test_create_task(db_session: AsyncSession):
    """Тест создания задачи"""
    new_task = Task(title="Test Task", description="This is a test task")
    db_session.add(new_task)
    await db_session.commit()
    await db_session.refresh(new_task)

    result = await db_session.execute(select(Task).filter_by(title="Test Task"))
    task = result.scalars().first()

    assert task is not None
    assert task.title == "Test Task"
    assert task.description == "This is a test task"


@pytest.mark.asyncio
async def test_get_all_tasks(db_session: AsyncSession):
    """Тест получения всех задач"""
    valid_statuses = ["NEW", "IN_PROGRESS", "RESOLVED"]

    new_task = Task(
        title="Test Task", description="Test Description", status=valid_statuses[0]
    )
    db_session.add(new_task)
    await db_session.commit()
    await db_session.refresh(new_task)

    result = await db_session.execute(select(Task))
    tasks = result.scalars().all()

    assert len(tasks) > 0
    assert tasks[0].status in valid_statuses


@pytest.mark.asyncio
async def test_get_task_by_id(db_session):
    """Тест получения задачи по ID"""
    new_task = Task(title="Test Task", description="Task for testing")
    db_session.add(new_task)
    await db_session.commit()
    await db_session.refresh(new_task)  # Получаем ID

    result = await db_session.execute(select(Task).filter_by(id=new_task.id))
    task = result.scalars().first()

    assert task is not None
    assert task.id == new_task.id
    assert task.title == "Test Task"


@pytest.mark.asyncio
async def test_update_task(db_session):
    """Тест обновления задачи"""
    new_task = Task(title="Old Title", description="Old Description")
    db_session.add(new_task)
    await db_session.commit()
    await db_session.refresh(new_task)

    # Обновляем задачу
    new_task.title = "Updated Title"
    new_task.description = "Updated Description"
    await db_session.commit()

    result = await db_session.execute(select(Task).filter_by(id=new_task.id))
    updated_task = result.scalars().first()

    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"


@pytest.mark.asyncio
async def test_delete_task(db_session):
    """Тест удаления задачи"""
    new_task = Task(title="To Be Deleted", description="Will be removed")
    db_session.add(new_task)
    await db_session.commit()
    await db_session.refresh(new_task)

    # Удаляем задачу
    await db_session.delete(new_task)
    await db_session.commit()

    result = await db_session.execute(select(Task).filter_by(id=new_task.id))
    deleted_task = result.scalars().first()

    assert deleted_task is None
