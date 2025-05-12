from sqlalchemy import select, update as sqlal_update
from src.dao.base import BaseDAO
from src.users.models import User
from src.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from src.users.models import User, Image

class UserDAO(BaseDAO):
    model = User
    
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
    
    async def find_user(username: str):
        async with async_session_maker() as session:
            check = await session.execute(select(User).where(User.username == username))
            user = check.scalar_one_or_none()
            return user
        
    async def update(user: str, **values):
        async with async_session_maker() as session:
            async with session.begin():
                await session.execute(sqlal_update(User)
                                      .where(User.id==user.id)
                                      .values(**values))

    async def load_icon(user: str, filepath: str):
        async with async_session_maker() as session:
            async with session.begin():
                image = Image(filepath=filepath)
                session.add(image)
                await session.flush()
                await session.execute(sqlal_update(User)
                                      .where(User.id == user.id)
                                      .values(image_id=image.id))