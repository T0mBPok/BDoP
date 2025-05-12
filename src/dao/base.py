from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from src.database import async_session_maker
from src.users.models import User


class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_all_for_user(cls, user: User, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.author_id == user.id)

            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            new_instance = result.scalars().unique().all()
            return new_instance
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(User)
                .options(selectinload(User.image))
                .where(User.id == data_id)
            )
            return result.scalar_one_or_none()
    
    @classmethod
    async def add(cls, author_id: int, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values, author_id=author_id)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
            
    @classmethod
    async def update(cls, user: User, filter_by, **values):
        async with async_session_maker() as session:
            if user.is_admin:
                query = (sqlalchemy_update(cls.model)
                        .where(*[getattr(cls.model, key) == value for key, value in filter_by.items()])
                        .values(**values)
                    )
            else:
                query = (sqlalchemy_update(cls.model)
                        .where(*[getattr(cls.model, key) == value for key, value in filter_by.items()])
                        .where(cls.model.author_id == user.id)
                        .values(**values)
                    )
                
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
            
    @classmethod
    async def delete(cls, user: User, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Either delete_all must be True or filter_by must be provided")

        async with async_session_maker() as session:
            async with session.begin():
                if user.is_admin:
                    query = sqlalchemy_delete(cls.model)
                else:
                    query = sqlalchemy_delete(cls.model).where(cls.model.author_id == user.id)
                    
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount