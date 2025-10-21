from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .user import UserResponse

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    task_id: Optional[int] = None

class CommentResponse(CommentBase):
    id: int
    author_id: int
    task_id: int
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True