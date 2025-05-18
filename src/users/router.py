from fastapi import APIRouter, File, HTTPException, Response, status, Depends, UploadFile, Request
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UserDAO
from src.users.models import User
from src.users.schemas import UserRegister, UserAuth, GetUserInfo, UserUpdate, GetAnotherUserInfo
from src.users.dependencies import get_current_user
from src.users.rb import RBUser
import os, shutil


router = APIRouter(prefix='/user', tags=['Работа с пользователями'])

@router.post('/register/')
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_all(email = user_data.email, username = user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с такими данными уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': "Вы успешно зарегистрировались"}

@router.post('/login/')
async def auth_user(response: Response, user_data: UserAuth) -> dict:
    check = await authenticate_user(email=user_data.email, password = user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}
    
@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/current_user", summary="Get current user info", response_model=GetUserInfo)
async def get_user(request: Request, user: User = Depends(get_current_user), is_completed: bool = False):
    user_with_tasks = await UserDAO.get_user_with_attached_tasks(user.id, is_completed)
    if not user_with_tasks:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    image_url = None
    if user_with_tasks.image:
        base_url = str(request.base_url).rstrip('/')
        image_url = f"{base_url}/{user_with_tasks.image.filepath}"

    return GetUserInfo(
        username=user_with_tasks.username,
        email=user_with_tasks.email,
        created_at=user_with_tasks.created_at,
        image_url=image_url,
        attached_tasks=user_with_tasks.attached_tasks,
        attached_substacles=user_with_tasks.attached_substacles
    )

@router.get('/find_user', summary="Find another user", response_model=list[GetAnotherUserInfo])
async def find_user(request_body: RBUser = Depends(), user: str = Depends(get_current_user)):
    users = await UserDAO.find_all_for_user(**request_body.to_dict())
    return users

@router.put('/', summary = 'Change user info')
async def change_user_info(user_data: UserUpdate, user: str = Depends(get_current_user)) -> dict:
    update_user = user_data.model_dump(exclude_unset=True)
    if not update_user:
        raise ValueError('Нет полей для обновления')
    
    await UserDAO.update(user, **update_user)
    return {'message': "Данные успешно обновлены"}
