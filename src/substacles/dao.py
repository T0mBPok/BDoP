from src.dao.base import BaseDAO
from src.substacles.models import Subtit
from src.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from src.projects.models import Project
from fastapi import status, HTTPException
from src.users.models import User
from src.tasks.models import Task
from datetime import date


class SubtitDAO(BaseDAO):
    model = Subtit
    
    @classmethod
    async def add(cls, author_id: int, performer_id: int | None, task_id: int, **values):
        async with async_session_maker() as session:
            performer_id = author_id if performer_id is None else performer_id
            task = await session.get(Task, task_id)
            project_id = task.project_id
            if project_id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не все поле заполнены!")
            
            project = await session.get(Project, project_id)
            if performer_id:
                result = await session.execute(select(Project)
                                                .options(selectinload(Project.users))
                                                .where(Project.id == project_id)
                                                .order_by(Project.id))
                project = result.scalars().one()
                user = await session.get(User, performer_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Пользователь с введенным id не существует")
                if user not in project.users:
                    project.users.append(user)
            
            deadline: date = values.get('deadline')
            today = date.today()

            if deadline < today:
                raise HTTPException(
                    status_code=400,
                    detail=f"Deadline не может быть в прошлом (текущая дата: {today.isoformat()})"
                )            
            
            creation_date: date = date.today() 
            if 'importance_color' not in values or values['importance_color'] is None:
                days_left = (deadline - creation_date).days
                if days_left >= 3:
                    importance_color = 4  # зелёный
                elif days_left == 2:
                    importance_color = 2  # оранжевый
                else:
                    importance_color = 1  # красный
                values['importance_color'] = importance_color
            
            new_instance = cls.model(**values, author_id=author_id, performer_id = performer_id, task_id = task_id, category_id = project.category_id, project_id=project_id, is_completed = False)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance