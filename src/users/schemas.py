from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    username: str    
    
class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)