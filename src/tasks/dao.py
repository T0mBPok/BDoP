from src.tasks.models import Task
from src.dao.base import BaseDAO
from src.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from src.users.models import User
from sqlalchemy import select, or_

class TaskDAO(BaseDAO):
    model = Task
    
    @classmethod
    async def add(cls, author_id: int, performer_id: int | None, **values):
        async with async_session_maker() as session:
            async with session.begin():
                performer_id = author_id if performer_id is None else performer_id
                new_instance = cls.model(**values, author_id=author_id, performer_id = performer_id)
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