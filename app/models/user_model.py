from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SqlEnum
from app.enums.user_enum import UserRole
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False, min_length=4)
    
    role: UserRole = Field(
        sa_column=Column(SqlEnum(UserRole), nullable=False)
    )


