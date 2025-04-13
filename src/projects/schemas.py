from pydantic import BaseModel
from datetime import datetime
    
    
class Project_get(BaseModel):
    id: int
    name: str
    description: str | None
    category_color: int
    created_at: datetime
    
class Project_add(BaseModel):
    name: str
    description: str | None
    category_color: int
    
class Project_update(BaseModel):
    id: int
    category_color: int | None
    name: str | None
    description: str | None       