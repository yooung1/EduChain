from pydantic import BaseModel, Field
from typing import Optional


class KlassSchema(BaseModel):
    name: str = Field(min_length=5, nullable=False)
    video: str = Field(min_length=5, nullable=False)
    description: str = Field(min_length=10, nullable=False)
    course_id: Optional[int]