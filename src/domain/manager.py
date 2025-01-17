from fastapi import APIRouter, FastAPI, Depends
from http.client import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from base import Base, get_async_db, engine
from domain import crud, schemas


router = APIRouter()


@router.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_task(db=db, task=task)


@router.get("/tasks/", response_model=list[schemas.TaskResponse])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    return await crud.get_tasks(db=db, skip=skip, limit=limit)


@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    task = await crud.get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_async_db)):
    updated_task = await crud.update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}
