from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime  

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Job Schemas
class JobCreate(BaseModel):
    title: str
    company: str
    status: Optional[str] = "Applied"

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    status: str
    user_id: int

    class Config:
        from_attributes = True