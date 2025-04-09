from src.dao.base import BaseDAO
from src.projects.models import Project


class ProjectDAO(BaseDAO):
    model = Project