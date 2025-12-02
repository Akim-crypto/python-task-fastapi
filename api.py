from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core import add_task, update_task, delete_task, change_status, list_tasks
from exceptions import ValidationError, TaskNotFound

app = FastAPI(title="Task Tracker API")


class TaskCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)


class TaskUpdate(BaseModel):
    description: str = Field(min_length=1, max_length=255)


class TaskOut(BaseModel):
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate):
    try:
        return add_task(task.description)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(status: str | None = None):
    try:
        return list_tasks(status)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    try:
        tasks = list_tasks()
        for t in tasks:
            if t["id"] == task_id:
                return t
        raise TaskNotFound(task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task_endpoint(task_id: int, task: TaskUpdate):
    try:
        return update_task(task_id, task.description)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int):
    try:
        delete_task(task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/tasks/{task_id}/status/{status}", response_model=TaskOut)
def change_status_endpoint(task_id: int, status: str):
    try:
        return change_status(task_id, status)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
