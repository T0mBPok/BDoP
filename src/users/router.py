from fastapi import APIRouter, HTTPException, Response, status, Depends
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UserDAO
from src.users.schemas import UserRegister, UserAuth, GetUserInfo
from src.users.dependencies import get_current_user


router = APIRouter(prefix='/user', tags=['Auth'])

@router.post('/register/')
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_all(email = user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с такой почтой уже существует'
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
async def get_current_user(user: str = Depends(get_current_user)):
    return user

@router.get('/find_user', summary="Find another user", response_model=GetUserInfo)
async def find_user(name: str):
    user = await UserDAO.find_user(username=name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user