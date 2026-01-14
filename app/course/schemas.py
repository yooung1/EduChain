from pydantic import Field, BaseModel
from typing import Optional

class CourseSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)