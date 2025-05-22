from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime, date

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    username: str    
    
class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    
class UserGet(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    importance_color: int
    category_id: int
    performer_id: int
    author_id: int
    project_id: int
    deadline: date
    model_config = ConfigDict(from_attributes=True)
    
class SubtitResponse(BaseModel):
    id: int
    name: str
    description: str
    importance_color: int
    category_id: int
    performer_id: int
    author_id: int
    task_id: int
    deadline: date
    model_config = ConfigDict(from_attributes=True)

class GetUserInfo(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    image_url: str | None = None
    attached_tasks: list[TaskResponse] = []
    attached_substacles: list[SubtitResponse] = []
    model_config = ConfigDict(from_attributes=True)
    
class GetAnotherUserInfo(BaseModel):
    username: str
    email: str
    created_at: datetime
    image_url: str | None = None
    
class UserUpdate(BaseModel):
    username:str | None = None
    email: EmailStr | None = None
    image_id: int | None = None
    password: str | None = Field(min_length=8, max_length=16, default=None)
    
class ResetPass(BaseModel):
    email: EmailStr
    
class VerifyResetPass(BaseModel):
    email: EmailStr
    code: str
    
class NewPass(BaseModel):
    new_pass: str
    token: str