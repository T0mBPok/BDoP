from src.dao.base import BaseDAO
from src.projects.models import Project
from src.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from src.users.models import User

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
            async with session.begin():
                project = cls.model(**values, author_id=author_id)
                
                author = await session.get(User, author_id)
                if not author:
                    raise ValueError(f"User with id {author_id} not found")
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
    async def find_all_for_user(cls, user: User, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.users))

            if not user.is_admin:
                query = query.join(cls.model.users).where(User.id == user.id)

            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            projects = result.scalars().unique().all()
            return projects