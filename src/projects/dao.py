from fastapi import HTTPException, status
from src.dao.base import BaseDAO
from src.projects.models import Project
from src.database import async_session_maker
from sqlalchemy import select, update as sqlal_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from src.users.models import User
from src.categories.models import Category

class ProjectDAO(BaseDAO):
    model = Project
    
    @staticmethod
    async def find_by_user(user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Project)
                .join(Project.users)
                .where(User.id == user_id)
                .options(selectinload(Project.users))
            )
            result = await session.execute(query)
            projects = result.scalars().unique().all()
            return projects
        
    @classmethod
    async def add(cls, author_id: int, user_ids: list[int] = [], **values):
        async with async_session_maker() as session:            
            author = await session.get(User, author_id)

            category_id = values.get("category_id")
            if category_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Не введен id категории"
                )

            category = await session.get(Category, category_id)
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Категория с id {category_id} не найдена"
                )

            if category.author_id != author_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Нет доступа к данной категории"
                )
            
            project = cls.model(**values, author_id=author_id)
            project.users.append(author)
            
            if user_ids:
                users = await session.execute(
                    select(User).where(User.id.in_(user_ids))
                )
                project.users.extend(users.scalars().all())
            
            session.add(project)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return project
        
    @classmethod
    async def add_to_project(self, project_id: int, user_ids: list[int], user: User):
        async with async_session_maker() as session:
            if user.is_admin:
                result = await session.execute(
                    select(Project)
                    .options(selectinload(Project.users))
                    .where(Project.id == project_id)
                )
            else:
                result = await session.execute(
                    select(Project)
                    .options(selectinload(Project.users))
                    .where(Project.id == project_id, Project.author_id == user.id)
                )
            project = result.scalar_one_or_none()
            if not project:
                raise ValueError("Проект не найден")
            query = (
                select(User)
                .where(User.id.in_(user_ids))
            )
            users = await session.execute(query)
            project.users.extend(users.scalars().all())
            
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return project                
            
    @classmethod
    async def find_all_for_user(cls, user: User, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.users), selectinload(cls.model.image))

            if not user.is_admin:
                 query = select(cls.model).options(selectinload(cls.model.image), selectinload(cls.model.users)).where(cls.model.author_id == user.id)

            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            projects = result.scalars().unique().all()
            return projects