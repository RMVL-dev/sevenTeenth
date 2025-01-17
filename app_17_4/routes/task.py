from fastapi import APIRouter, Depends, status, HTTPException
from app_17_4.backend.db_depends import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app_17_4.schemas.TaskSchemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from app_17_4.models.task import Task
from app_17_4.models.user import User

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).order_by(Task.id)).all()
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks no found"
        )
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: Annotated[int, "task id"]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {task_id} not found"
        )
    return task


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], task: Annotated[CreateTask, "Task model"], user_id: Annotated[int, "User id"]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(
            insert(Task).values(title=task.title, content=task.content, priority=task.priority, user_id=user_id)
        )
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id = {user_id} not found"
        )


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task: Annotated[CreateTask, "Task model"], user_id: Annotated[int, "New user id"], task_id: Annotated[int, "Task id"]):
    user = db.scalar(select(User).where(User.id == user_id))
    prev_task = db.scalar(select(Task).where(Task.id == task_id))
    if user is not None and prev_task is not None:
        db.execute(
            update(Task).where(Task.id == task_id).values(title=task.title, content=task.content, priority=task.priority, user_id=user_id)
        )
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    elif user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id = {user_id} was not found. Update task failed."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {task_id} was not found. Update task failed."
        )


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: Annotated[int, "task id"]):
    if db.scalar(select(Task).where(Task.id == task_id)) is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {task_id} was not found. Update task failed."
        )