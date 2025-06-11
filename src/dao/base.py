from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, and_, exists
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload
from src.database import async_session_maker
from src.users.models import User
from src.images.models import Image
from fastapi import HTTPException, status
from src.users.auth import generate_password, get_password_hash
from src.email import send_userinfo_email


class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_all_for_user(cls, user: str, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.author_id == user.id)
            if user.is_admin:
                query = select(cls.model)
            for attr, value in filters.items():
                query = query.where(getattr(cls.model, attr) == value)

            result = await session.execute(query)
            return result.scalars().unique().all()
        
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
            new_instance = cls.model(**values, author_id=author_id)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError  as e:
                await session.rollback()
                raise e
            except IntegrityError  as e:
                await session.rollback()
                raise e
            return new_instance
            
    @classmethod
    async def update(cls, user: User, filter_by, **values):
        async with async_session_maker() as session:
            image_id = values.get('image_id')
            if image_id is not None:
                stmt = select(exists().where(Image.id == image_id))
                image_exists = await session.scalar(stmt)
                if not image_exists:
                    raise HTTPException(status_code=400, detail=f"Image with id={image_id} does not exist")

            # Проверка performer_id
            performer_id = values.get('performer_id')
            if performer_id is not None:
                stmt = select(exists().where(User.id == performer_id))
                performer_exists = await session.scalar(stmt)
                if not performer_exists:
                    raise HTTPException(status_code=400, detail=f"User (performer) with id={performer_id} does not exist")

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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Either delete_all must be True or filter_by must be provided")
        async with async_session_maker() as session:
            query = sqlalchemy_delete(cls.model)
            conditions = []

            if not user.is_admin:
                conditions.append(cls.model.author_id == user.id)

            if not delete_all:
                for key, value in filter_by.items():
                    column = getattr(cls.model, key, None)
                    if column is None:
                        raise ValueError(f"Invalid filter column: {key}")
                    conditions.append(column == value)
            if conditions:
                query = query.where(and_(*conditions))

            try:
                result = await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
        
    @staticmethod
    async def set_performer(performer_email: str):
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.email == performer_email))
            user = result.scalars().first()
            if not user:
                user_data = {"email": performer_email}
                user_data['username'] = performer_email.split('@')[0]
                password = generate_password()
                user_data['password'] = get_password_hash(password)
                user = User(**user_data)
                session.add(user)
                await session.flush()
                await send_userinfo_email(performer_email, password)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return user