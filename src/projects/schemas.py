from pydantic import BaseModel
    
    
class Project_get(BaseModel):
    id: int
    name: str
    description: str
    category_color: str
    count_tasks: int
    
class Project_add(BaseModel):
    name: str
    description: str
    category_color: str