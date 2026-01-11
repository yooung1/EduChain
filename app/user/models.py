from app.enums.user_enum import UserRole
from app.auth.service import get_password_hash
from sqlmodel import Session
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SqlEnum
from typing import Optional
from app.models.user_model import User


# class User(SQLModel, table=True):
#     __tablename__ = "users"

#     id: Optional[int] = Field(default=None, primary_key=True, index=True)
    
#     first_name: str = Field(nullable=False)
#     last_name: str = Field(nullable=False)
#     username: str = Field(unique=True, nullable=False)
#     email: str = Field(unique=True, index=True, nullable=False)
#     hashed_password: str = Field(nullable=False, min_length=4)
    
#     role: UserRole = Field(
#         sa_column=Column(SqlEnum(UserRole), nullable=False)
#     )









