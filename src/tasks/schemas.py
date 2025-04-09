from datetime import date
from pydantic import BaseModel, Field


class Task_get(BaseModel):
    id: int
    name: str
    category_color: str
    importance_color: str
    perfomer: str
    author: str
    description: str
    created_at: date
    deadline: date
    project_id: int

class Task_add(BaseModel):
    name: str
    category_color: str
    importance_color: str
    perfomer: str = Field(None, description='Someone or the author')
    author: str
    description: str
    deadline: date
    project_id: int    