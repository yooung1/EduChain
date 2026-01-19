from pydantic import BaseModel, Field, EmailStr
from app.enums.user_enum import UserRole
from typing import Optional


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    username: str = Field(..., min_length=2)
    email: EmailStr = Field(...,)

class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserPublic(UserBase):
    id: int
    role: UserRole

    model_config = {
        "from_attributes": True
    }
