from sqlmodel import SQLModel, Field
from typing import Optional


class Klass(SQLModel, table=True):
    __tablename__ = "klass"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False)
    video: str = Field(nullable=False)
    description: str = Field(nullable=False)
