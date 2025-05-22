from pydantic import BaseModel, EmailStr
from datetime import date


class add_subtit(BaseModel):
    name: str
    description: str | None = None
    importance_color: int | None = None
    performer_email: EmailStr | None = None
    deadline: date
    task_id: int

class GetSubtit(BaseModel):
    id: int
    name: str
    description: str | None = None
    importance_color: int | None = None
    performer_id: int
    author_id: int
    deadline: date
    task_id: int
    created_at: date
    is_completed: bool
    
class UpdateSubtit(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    importance_color: int | None = None
    performer_id: int | None = None
    deadline: date | None = None
    is_completed: bool | None = None