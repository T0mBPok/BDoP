from datetime import date, datetime
from pydantic import BaseModel, Field
from src.users.schemas import UserGet


class Task_get(BaseModel):
    id: int
    name: str
    category_color: int
    performer_id: int
    author_id: int
    description: str
    created_at: datetime
    deadline: date
    project_id: int

class Task_add(BaseModel):
    name: str
    category_color: int
    performer_id: int | None = Field(None, description='Someone or the author')
    description: str
    deadline: date
    project_id: int
    
class Task_update(BaseModel):
    id: int
    name: str | None
    performer_id: int | None
    description: str | None
    deadline: date | None