from sqlalchemy import select, update as sqlal_update, delete
from sqlalchemy.orm import selectinload
from src.dao.base import BaseDAO
from src.users.models import User
from src.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from src.users.schemas import ResetPass, VerifyResetPass
from src.email import send_reset_email
from src.config import redis_client
from fastapi import HTTPException, status
from src.tasks.models import Task
from src.substacles.models import Subtit

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
        
    async def update(user: str, **values):
        async with async_session_maker() as session:
            async with session.begin():
                await session.execute(sqlal_update(User)
                                      .where(User.id==user.id)
                                      .values(**values))
                
    @staticmethod
    async def get_user_with_attached_tasks(user_id: int, is_completed: bool | None = None):
        async with async_session_maker() as session:
            query = select(User).options(
                selectinload(User.image),
                selectinload(User.attached_tasks),
                selectinload(User.attached_substacles),
            ).where(User.id == user_id)

            result = await session.execute(query)
            user = result.scalars().first()
            if not user:
                return None

            def filter_completed(items):
                if is_completed is None:
                    return [item for item in items if not item.is_completed]
                else:
                    return [item for item in items if item.is_completed == is_completed]

            user.attached_tasks = filter_completed(user.attached_tasks)
            user.attached_substacles = filter_completed(user.attached_substacles)

            return user
        
    @classmethod
    async def find_all_for_user(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model)
            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            return result.scalars().unique().all()
        
    async def pass_reset(data: ResetPass):
        async with async_session_maker() as session:
            check = session.get(User, data.email)
            if not check:
                return {'message': "Код восстановления пароля отправлен на почту"}
            await send_reset_email(data.email)
            return {'message': "Код восстановления пароля отправлен на почту"}
        
    async def verify_code(data: VerifyResetPass):
        key = f"reset_code:{data.email}"
        stored_code = await redis_client.get(key)
        if not stored_code or stored_code!=data.code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неправильный код либо закончилось время его действия')
        await redis_client.delete(key)
        
    @staticmethod
    async def ressign_tasks(user_id: int, session):
        await session.execute(sqlal_update(Task)
                              .where(Task.performer_id == user_id)
                              .values(performer_id = Task.author_id))
        await session.execute(sqlal_update(Subtit)
                              .where(Subtit.performer_id == user_id)
                              .values(performer_id = Subtit.author_id))
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        
    @classmethod
    async def delete(cls, user: str):
        async with async_session_maker() as session:
            await cls.ressign_tasks(user.id, session)
            await session.execute(delete(User).where(User.id == user.id))
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e