from pydantic import BaseModel, EmailStr
from app.constants.user_registration_model_constants import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: UserRole = UserRole.STUDENT

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    user_type: UserRole