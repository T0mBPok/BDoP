from src.tasks.models import Task
from src.dao.base import BaseDAO
from src.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from src.users.models import User
from sqlalchemy import select, or_
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from src.projects.models import Project
from src.users.models import User
from datetime import date

class TaskDAO(BaseDAO):
    model = Task
    
    @classmethod
    async def add(cls, author_id: int, project_id: int, **values):
        async with async_session_maker() as session:
            performer_email = values.pop('performer_email')
            if performer_email is None:
                performer_id = author_id
            else:
                user = await cls.set_performer(performer_email)
                performer_id = user.id
                
            if project_id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не все поле заполнены!")
            
            deadline: date = values.get('deadline')
            today = date.today()

            if deadline < today:
                raise HTTPException(
                    status_code=400,
                    detail=f"Deadline не может быть в прошлом (текущая дата: {today.isoformat()})"
                )
            
            project = await session.get(Project, project_id)
            if not project: 
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект с введенным id не существует")
            if performer_id:
                result = await session.execute(select(Project)
                                                .options(selectinload(Project.users))
                                                .where(Project.id == project_id)
                                                .order_by(Project.id))
                project = result.scalars().one()
                if user not in project.users:
                    project.users.append(user)
            
            creation_date: date = date.today() 

            if 'importance_color' not in values or values['importance_color'] is None:
                days_left = (deadline - creation_date).days
                if days_left >= 3:
                    importance_color = 4  # зелёный
                elif days_left == 2:
                    importance_color = 3  # жёлтый
                elif days_left == 1:
                    importance_color = 2  # оранжевый
                else:
                    importance_color = 1  # красный
                values['importance_color'] = importance_color
                
            new_instance = cls.model(**values, author_id=author_id, performer_id = performer_id, project_id = project_id, category_id = project.category_id, is_completed = False)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance
            
    @classmethod
    async def find_all_for_user(cls, user: User, **filters):
        async with async_session_maker() as session:
            query = select(cls.model)
            
            if not user.is_admin:
                query = select(cls.model).where(or_(cls.model.author_id == user.id, cls.model.performer_id == user.id))

            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            new_instance = result.scalars().unique().all()
            return new_instance
        
    # async def create_user(self, email: str):
    #     async with async_session_maker() as session:
    #         user_data = {"email": email}
    #         user_data['username'] = email.split('@')[0]
    #         user_data['password'] = generate_password()
            
            