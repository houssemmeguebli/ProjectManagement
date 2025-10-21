from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.task import TaskStatus
from .user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: int
    assigned_user_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_user_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    project_id: int
    assigned_user_id: Optional[int] = None
    assigned_user: Optional[UserResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True