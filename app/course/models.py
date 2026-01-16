from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.klass.models import Klass

class Course(SQLModel, table=True):
    __tablename__ = "course"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    klasses: List["Klass"] = Relationship(
        back_populates="course",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
