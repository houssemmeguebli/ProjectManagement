from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.comment import CommentCreate, CommentResponse
from ..crud.comment import comment_crud
from ..crud.task import task_crud
from ..crud.project import project_crud
from ..models.user import User
from .auth import get_current_user

router = APIRouter(tags=["comments"])

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
            detail=f"Access denied. You must be the owner or a contributor of project '{project.title}' to access comments for task '{task.title}'. Contact the project owner ({project.owner.username}) to request access."
        )
    
    return task

@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse], dependencies=[Depends(get_current_user)])
def get_task_comments(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_task_access(task_id, current_user, db)
    return comment_crud.get_by_task(db, task_id)

@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, dependencies=[Depends(get_current_user)])
def create_task_comment(task_id: int, comment_create: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_task_access(task_id, current_user, db)
    # Create a new CommentCreate with the task_id set
    comment_data = comment_create.model_dump()
    comment_data['task_id'] = task_id
    return comment_crud.create(db, CommentCreate(**comment_data), current_user.id)