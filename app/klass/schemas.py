from pydantic import BaseModel, Field
from typing import Optional


class KlassSchemaPost(BaseModel):
    name: str = Field(min_length=5)
    video: str = Field(min_length=5)
    description: str = Field(min_length=10)
    course_id: Optional[int]


class KlassSchemaPublic(KlassSchemaPost):
    id: Optional[int] = None
    name: str = Field(min_length=5)
    video: str = Field(min_length=5)
    description: str = Field(min_length=10)