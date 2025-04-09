from src.tasks.models import Task
from src.dao.base import BaseDAO

class TaskDAO(BaseDAO):
    model = Task