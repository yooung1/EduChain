from pydantic import Field, BaseModel
from typing import Optional, List
from app.klass.schemas import KlassSchemaPublic


class CourseSchemaPost(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)


class CourseSchemaPublic(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    klasses: List[KlassSchemaPublic] = []