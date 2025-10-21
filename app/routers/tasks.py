from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.task import TaskCreate, TaskResponse, TaskUpdate
from ..crud.task import task_crud
from ..crud.project import project_crud
from ..models.user import User
from ..models.task import TaskStatus
from .auth import get_current_user

router = APIRouter(tags=["tasks"])

def check_task_access(task_id: int, user: User, db: Session):
    task = task_crud.get_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404, 
            detail=f"Task with ID {task_id} not found"
        )
    
    project = project_crud.get_by_id(db, task.project_id)
    if project.owner_id != user.id and user not in project.contributors:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied. You must be the owner or a contributor of project '{project.title}' to access task '{task.title}'. Contact the project owner ({project.owner.username}) to request access."
        )
    
    return task

def check_project_access(project_id: int, user: User, db: Session):
    project = project_crud.get_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=404, 
            detail=f"Project with ID {project_id} not found"
        )
    
    if project.owner_id != user.id and user not in project.contributors:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied. You must be the owner or a contributor of project '{project.title}' to perform this action. Contact the project owner ({project.owner.username}) to request access."
        )
    
    return project



@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_project_access(project_id, current_user, db)
    return task_crud.get_by_project(db, project_id)

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def create_project_task(project_id: int, task_create: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_project_access(project_id, current_user, db)
    task_create.project_id = project_id
    return task_crud.create(db, task_create)

@router.get("/tasks/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return check_task_access(task_id, current_user, db)

@router.put("/tasks/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def update_task(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = check_task_access(task_id, current_user, db)
    return task_crud.update(db, task, task_update)

@router.delete("/tasks/{task_id}", dependencies=[Depends(get_current_user)])
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = check_task_access(task_id, current_user, db)
    task_crud.delete(db, task)
    return {"message": "Task deleted successfully"}

@router.get("/tasks/status/{status}", response_model=List[TaskResponse])
def get_tasks_by_status(status: TaskStatus, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all tasks by status for current user's accessible projects"""
    all_tasks = task_crud.get_by_status(db, status)
    # Filter tasks from projects user has access to
    accessible_tasks = []
    for task in all_tasks:
        project = project_crud.get_by_id(db, task.project_id)
        if project and (project.owner_id == current_user.id or current_user in project.contributors):
            accessible_tasks.append(task)
    return accessible_tasks

@router.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
def get_tasks_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all tasks assigned to a specific user (only from accessible projects)"""
    user_tasks = task_crud.get_by_user(db, user_id)
    # Filter tasks from projects current user has access to
    accessible_tasks = []
    for task in user_tasks:
        project = project_crud.get_by_id(db, task.project_id)
        if project and (project.owner_id == current_user.id or current_user in project.contributors):
            accessible_tasks.append(task)
    return accessible_tasks

