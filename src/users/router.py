from fastapi import APIRouter, File, HTTPException, Response, status, Depends, UploadFile, Request
from sqlalchemy import or_
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UserDAO
from src.users.models import User
from src.users.schemas import UserRegister, UserAuth, GetUserInfo, UserUpdate
from src.users.dependencies import get_current_user
import os, shutil


router = APIRouter(prefix='/user', tags=['Работа с пользователями'])
UPLOAD_DIR = "./user_image"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

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
async def get_user(request: Request, user: str = Depends(get_current_user)):
    image_url = None
    if user.image:
        base_url = str(request.base_url).rstrip('/')
        image_url = f"{base_url}/{user.image.filepath}"
    return GetUserInfo(
        username = user.username,
        email = user.email,
        created_at = user.created_at,
        image_url = image_url
    )

@router.get('/find_user', summary="Find another user", response_model=GetUserInfo)
async def find_user(name: str):
    user = await UserDAO.find_user(username=name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user

@router.put('/', summary = 'Change user info')
async def change_user_info(user_data: UserUpdate, user: str = Depends(get_current_user)) -> dict:
    update_user = user_data.model_dump(exclude_unset=True)
    if not update_user:
        raise ValueError('Нет полей для обновления')
    
    await UserDAO.update(user, **update_user)
    return {'message': "Данные успешно обновлены"}

@router.put('/load_icon', summary="Загрузить иконку пользователя")
async def load_icon(file: UploadFile = File(...), user: str = Depends(get_current_user)) -> dict:
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение файла. Разрешены только: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        
    file_loc = f"{UPLOAD_DIR}/{user.id}{file_extension}"
    
    try:
        with open(file_loc, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении файла: {e}"
        )
        
    await UserDAO.load_icon(user, filepath=file_loc)
    return {'message': "Иконка успешно загружена"}