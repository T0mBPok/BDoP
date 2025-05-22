from datetime import date
from pydantic import BaseModel, EmailStr


class Task_get(BaseModel):
    id: int
    name: str
    category_id: int
    performer_id: int
    author_id: int
    description: str
    created_at: date
    deadline: date
    project_id: int
    is_completed: bool

class Task_add(BaseModel):
    name: str
    performer_email: EmailStr | None = None
    description: str
    deadline: date
    project_id: int
    importance_color: int | None = None
    
class Task_update(BaseModel):
    id: int
    name: str | None = None
    performer_id: int | None = None
    description: str | None = None
    deadline: date | None = None
    is_completed: bool | None = None
    importance_color: int | None = None