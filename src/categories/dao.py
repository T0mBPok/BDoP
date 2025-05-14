from src.dao.base import BaseDAO
from src.categories.models import Category

class CategoryDAO(BaseDAO):
    model = Category