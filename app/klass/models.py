from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.course.models import Course


if TYPE_CHECKING:
    from app.course.models import Course

class Klass(SQLModel, table=True):
    __tablename__ = "klass"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False)
    video: str = Field(nullable=False)
    description: str = Field(nullable=False)

    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    course: Optional["Course"] = Relationship(back_populates="klasses")