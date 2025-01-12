from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app_17_4.backend.db_depends import get_db
from typing import Annotated
from app_17_4.models import User
from app_17_4.schemas.UserSchemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).order_by(User.id)).all()
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no users"
        )
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], user: CreateUser):
    if db.scalar(select(User).where(User.username == user.username)) is None:
        db.execute(
            insert(User).values(username=user.username, firstname=user.firstname, lastname=user.lastname, age=user.age))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User was registered"
        )


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user: UpdateUser, user_id: int):
    if db.scalar(select(User).where(User.id == user_id)) is not None:
        db.execute(update(User).where(User.id == user_id).values(firstname=user.firstname, lastname=user.lastname, age=user.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    if db.scalar(select(User).where(User.id == user_id)) is not None:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
