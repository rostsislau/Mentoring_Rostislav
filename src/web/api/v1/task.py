from fastapi import APIRouter, Depends, HTTPException

from src.domain.task import schemas
from src.domain.task.schemas import TaskResponse
from src.domain.task.service import TaskService
from src.web.deps import get_task_service

router = APIRouter()


@router.post("/task/", response_model=schemas.TaskResponse)
async def create(
    task: schemas.TaskCreate, service: TaskService = Depends(get_task_service)
):
    return await service.create(task)


@router.get("/tasks/", response_model=list[TaskResponse])
async def get_tasks(
    skip: int = 0, limit: int = 10, service: TaskService = Depends(get_task_service)
):
    return await service.get_all(skip, limit)


@router.get("/task/{task_id}", response_model=schemas.TaskResponse)
async def get_task_by_id(
    task_id: int, service: TaskService = Depends(get_task_service)
):
    return await service.get(obj_id=task_id)


@router.put("/task/{task_id}", response_model=schemas.TaskResponse)
async def update_task_by_id(
    task_id: int,
    task: schemas.TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return await service.update(task_id, task)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Task with id={task_id} not found")


@router.delete("/task/{task_id}", response_model=dict)
async def delete_task_by_id(
    task_id: int, service: TaskService = Depends(get_task_service)
):
    try:
        await service.delete(task_id)
        return {"message": f"Task with id={task_id} deleted successfully"}
    except Exception:
        raise HTTPException(status_code=404, detail=f"Task with id={task_id} not found")
