from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import UserResponse

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse
    contributors: List[UserResponse] = []

    class Config:
        from_attributes = True