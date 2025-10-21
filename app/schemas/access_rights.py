from pydantic import BaseModel
from ..models.access_rights import AccessRole
from .user import UserResponse

class AccessRightsBase(BaseModel):
    role: AccessRole

class AccessRightsCreate(AccessRightsBase):
    user_id: int
    project_id: int

class AccessRightsResponse(AccessRightsBase):
    id: int
    user_id: int
    project_id: int
    user: UserResponse

    class Config:
        from_attributes = True