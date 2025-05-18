from src.dao.base import BaseDAO
from src.images.models import Image
from src.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from src.users.models import User

class ImageDAO(BaseDAO):
    model = Image
    
    async def add_image(filepath: str, user: str):
        async with async_session_maker() as session:
            new_image = Image(filepath=filepath, author_id = user.id)
            session.add(new_image)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_image
        
    async def delete(user: User, id):
        async with async_session_maker() as session:
            query = delete(Image)

            if not user.is_admin:
                query = query.where(Image.author_id == user.id).where(Image.id == id)
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount