from fastapi import APIRouter, HTTPException, Response, status, Depends, Request
from src.users.auth import get_password_hash, create_access_token, verify_password
from src.users.dao import UserDAO
from src.users.models import User
from src.users.schemas import UserRegister, UserAuth, GetUserInfo, UserUpdate, GetAnotherUserInfo
from src.users.dependencies import get_current_user
from src.users.rb import RBUser
from src.users.schemas import ResetPass, VerifyResetPass
from src.email import send_reset_email
from src.config import redis_client


router = APIRouter(prefix='/user', tags=['Работа с пользователями'])

@router.post('/register/')
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_all(email = user_data.email)
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
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if not user or verify_password(plain_pass=user_data.password, hashed_pass=user.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(user.id)})
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
    if 'password' in update_user:
        update_user['password'] = get_password_hash(user_data.password)
    if not update_user:
        raise ValueError('Нет полей для обновления')
    
    await UserDAO.update(user, **update_user)
    return {'message': "Данные успешно обновлены"}

@router.post('/pass_reset/request')
async def pass_reset(data: ResetPass):
    check = await UserDAO.find_all(email=data.email)
    if not check:
        return {'message': 'Письмо с кодом было отправлено на почту'}
    await send_reset_email(data.email)
    return {'message': 'Письмо с кодом было отправлено на почту'}

@router.post('/pass_reset/verify')
async def verify_reset_code(response:Response, data: VerifyResetPass):
    key = f'reset_code:{data.email}'
    stored_code = await redis_client.get(key)
    if not stored_code or stored_code!=data.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Неправильный код либо закончилось время его действия')
    await redis_client.delete(key)
    user = await UserDAO.find_one_or_none(email=data.email)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.delete('/', summary = 'Delete a user')
async def delete_user(user: User = Depends(get_current_user)) -> dict:
    await UserDAO.delete(user)
    return {'message': "Пользователь успешно удален"}