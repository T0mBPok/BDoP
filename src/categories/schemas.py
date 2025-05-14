from pydantic import BaseModel

class CategoryAdd(BaseModel):
    name: str
    color: int
    
class CategoryGet(BaseModel):
    id: int | None = None
    name: str | None = None
    color: int | None = None