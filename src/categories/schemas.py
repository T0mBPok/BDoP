from pydantic import BaseModel, field_validator
import re

HEX_COLOR_RE = re.compile(r'^#([A-Fa-f0-9]{6})$')

class CategoryAdd(BaseModel):
    name: str
    color: str
    @field_validator('color')
    @classmethod
    def validate_color(cls, value):
        if not HEX_COLOR_RE.match(value):
            raise ValueError('Неверный формат цвета. Должен быть hex-формат.')
        return value
    
    
class CategoryGet(BaseModel):
    id: int
    name: str
    color: str
    
class CategoryUpdate(BaseModel):
    id: int | None = None
    name: str | None = None
    color: str | None = None
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not HEX_COLOR_RE.match(value):
            raise ValueError('Неверный формат цвета. Должен быть hex-формат.')
        return value