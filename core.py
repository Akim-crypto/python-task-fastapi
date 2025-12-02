import json
import os
from datetime import datetime
from enum import Enum
from typing import Any,Dict,List

from exceptions import TaskNotFound,ValidationError

TASK_FILE = "tasks.json"

class Status(str,Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

    @classmethod
    def values(cls) -> list[str]:
        return [s.value for s in cls]
    
def current_time() -> str:
    return datetime.now().isoformat(timespec="seconds")

def load_data() -> Dict[str,Any]:
    if not os.path.exists(TASK_FILE):
        return {"last_id": 0 , "tasks":[]}
    try:
        with open(TASK_FILE , "r" , encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        backup_name = TASK_FILE + ".bak"
        os.replace(TASK_FILE,backup_name)
        return {"last_id":0 , "tasks":[]}

def save_data(data:Dict[str,Any]) -> None:
    with open(TASK_FILE,"w",encoding="utf-8")as f :
        json.dump(data,f,indent=4,ensure_ascii=False)

def validate_description(description:str) -> str:
    description = description.strip()
    if not description:
        raise ValidationError("Description cannot be empty") 
    if len(description)>150:
        raise ValidationError("Description is too long (max 150 chars)")
    return description

def find_task(data:Dict[str,Any], task_id:int) -> Dict[str,Any]:
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    raise TaskNotFound(task_id)

def add_task(description:str) -> Dict[str,Any]:
    description = validate_description(description)
    data = load_data()
    new_id = data["last_id"] + 1
    now = current_time()

    task = {
         "id": new_id,
        "description": description,
        "status": Status.TODO.value,
        "createdAt": now,
        "updatedAt": now,
    }

    data["last_id"] = new_id
    data["tasks"].append(task)
    save_data(data)
    return task

def update_task(task_id:int , description:str) -> Dict[str,Any]:
    description = validate_description(description)
    data = load_data()
    task = find_task(data,task_id)

    task["description"] = description
    task["updatedAt"] = current_time()
    save_data(data)
    return task

def delete_task(task_id:int) -> None:
    data = load_data()
    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    after = len(data["tasks"])

    if before == after:
        raise TaskNotFound(task_id)
    
    save_data()

def change_status(task_id: int, new_status:str) -> Dict[str,Any]:
    if new_status not in Status.values():
        raise ValidationError(
            f"Invalid status '{new_status}'. Valid: {', '.join(Status.values())}"
        )
    
    data = load_data()
    task = find_task(data, task_id)

    task["status"] = new_status
    task["updatedAt"] = current_time()
    save_data(data)
    return task


def list_tasks(status: str | None = None) -> List[Dict[str, Any]]:
    data = load_data()
    tasks = data["tasks"]

    if status:
        if status not in Status.values():
            raise ValidationError(
                f"Invalid status '{status}'. Valid: {', '.join(Status.values())}"
            )
        tasks = [t for t in tasks if t["status"] == status]

    return tasks

        

        