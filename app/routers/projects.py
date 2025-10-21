from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ..crud.project import project_crud
from ..crud.user import user_crud
from ..models.user import User
from .auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

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
            detail=f"Access denied. You must be the project owner or a contributor to access project '{project.title}'. Contact the project owner ({project.owner.username}) to request access."
        )
    
    return project

@router.post("/", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
def create_project(project_create: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return project_crud.create(db, project_create, current_user.id)

@router.get("/", response_model=List[ProjectResponse], dependencies=[Depends(get_current_user)])
def get_user_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return project_crud.get_user_projects(db, current_user.id)

@router.get("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
def get_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return check_project_access(project_id, current_user, db)

@router.put("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
def update_project(project_id: int, project_update: ProjectUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_crud.get_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=404, 
            detail=f"Project with ID {project_id} not found"
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied. Only the project owner ({project.owner.username}) can update project '{project.title}'. You are currently a contributor with read-only access."
        )
    return project_crud.update(db, project, project_update)
@router.post("/{project_id}/contributors/{user_id}", dependencies=[Depends(get_current_user)])
def add_contributor(project_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_crud.get_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=404, 
            detail=f"Project with ID {project_id} not found"
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied. Only the project owner ({project.owner.username}) can add contributors to project '{project.title}'. You are currently a contributor with limited permissions."
        )
    
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found. Please verify the user ID and try again."
        )
    
    project_crud.add_contributor(db, project, user)
    return {"message": f"User '{user.username}' has been successfully added as a contributor to project '{project.title}'"}

@router.get("/users/{user_id}/projects", response_model=List[ProjectResponse])
def get_projects_by_user_id(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all projects for a specific user (only accessible projects for current user)"""
    user_projects = project_crud.get_projects_by_user_id(db, user_id)
    # Filter projects current user has access to
    accessible_projects = []
    for project in user_projects:
        if project.owner_id == current_user.id or current_user in project.contributors:
            accessible_projects.append(project)
    return accessible_projects


