from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from src.users.schemas import UserGet
    
class Project_get(BaseModel):
    id: int
    name: str
    description: str | None
    category_id: int
    author_id: int
    created_at: datetime
    image_url: str | None = None
    
    users: List["UserGet"] = []
    
    model_config = ConfigDict(from_attributes=True)
    
class Project_add(BaseModel):
    name: str
    description: str | None
    category_id: int
    user_ids: list[int] | None = []
    
class Project_update(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None 
    image_id: int | None = None
    
class Project_add_users(BaseModel):
    id: int
    user_ids: list[int]