from pydantic import BaseModel, Field, field_validator
import re

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 72:
            raise ValueError('Password cannot exceed 72 characters (bcrypt limitation)')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=1)

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True