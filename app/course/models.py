from sqlmodel import SQLModel, Field
from typing import Optional
from app.klass.models import Klass



class Course(SQLModel, table=True):
    __tablename__ = "course"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    klass: Klass


