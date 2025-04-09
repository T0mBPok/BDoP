from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from src.tasks.models import Task
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.projects.models import Project

class TaskDAO(BaseDAO):
    model = Task
    
    @classmethod
    async def add_task(cls, **task_data):
        async with async_session_maker() as session:
            async with session.begin():
                new_task = cls.model(**task_data)
                session.add(new_task)
                
                update_project = (
                    update(Project)
                    .where(Project.id == task_data['project_id'])
                    .values(count_tasks = Project.count_tasks+1)
                )
                await session.execute(update_project)
                
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_task