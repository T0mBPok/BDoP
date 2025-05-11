from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

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

class GetUserInfo(BaseModel):
    username: str
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)