from datetime import date, datetime
from pydantic import BaseModel, Field


class Task_get(BaseModel):
    id: int
    name: str
    category_color: int
    performer: str | None = Field(None)
    author: str
    description: str
    created_at: datetime
    deadline: date
    project_id: int

class Task_add(BaseModel):
    name: str
    category_color: int
    performer: str | None = Field(None, description='Someone or the author')
    description: str
    deadline: date
    project_id: int
    
class Task_update(BaseModel):
    id: int
    name: str | None
    performer: str| None
    description: str | None
    deadline: date | None