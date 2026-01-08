from pydantic import BaseModel, Field, EmailStr
from app.enums.user_enum import UserRole

class UserBase(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    username: str = Field(min_length=2)
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class Student(UserCreate):
    role: UserRole = UserRole.STUDENT

class Teacher(UserCreate):
    role: UserRole = UserRole.TEACHER

class Admin(UserCreate):
    role: UserRole = UserRole.ADMIN


class UserPublic(UserBase):
    id: int
    role: UserRole

    model_config = {
        "from_attributes": True
    }