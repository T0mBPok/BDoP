from datetime import date, datetime
from pydantic import BaseModel, Field


class Task_get(BaseModel):
    id: int
    name: str
    category_color: int
    importance_color: int
    perfomer: str | None = Field(None)
    author: str
    description: str
    created_at: datetime
    deadline: date
    project_id: int

class Task_add(BaseModel):
    name: str
    category_color: int
    importance_color: int
    perfomer: str | None = Field(None, description='Someone or the author')
    author: str
    description: str
    deadline: date
    project_id: int    