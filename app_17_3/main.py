from fastapi import FastAPI
from routes.task import router as task_router
from routes.user import router as user_router

task_scheduler_app = FastAPI()


@task_scheduler_app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

task_scheduler_app.include_router(task_router)
task_scheduler_app.include_router(user_router)
