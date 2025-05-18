from src.images.dao import ImageDAO
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from src.users.dependencies import get_current_user
from src.images.rb import RBImage
import os, shutil

router = APIRouter(prefix = '/images', tags=['Работа с изображениями'])
UPLOAD_DIR = "./user_image"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

@router.post('/', summary='Add image')
async def add_image(file: UploadFile = File(...), user: str = Depends(get_current_user)) -> dict:
    file_name, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение файла. Разрешены только: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        
    file_loc = f"{UPLOAD_DIR}/{file_name}{file_extension}"
    
    try:
        with open(file_loc, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении файла: {e}"
        )
        
    check = await ImageDAO.add_image(user=user, filepath=file_loc)
    if not check:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='The image did not loaded')
    return {'message': "Иконка успешно загружена"}

@router.get('/', summary='Get image')
async def get_image(request_body: RBImage = Depends(), user:str = Depends(get_current_user)):
    return await ImageDAO.find_all_for_user(user, **request_body.to_dict())
    

@router.delete('/', summary="Delete image")
async def delete_image(image_id: int, user: str = Depends(get_current_user)):
    image = await ImageDAO.find_one_or_none(id=image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Картинка не найдена')
    # Удаляем файл с диска, если он существует
    if image.filepath and os.path.isfile(image.filepath):
        try:
            os.remove(image.filepath)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при удалении файла: {e}"
            )
            
    check = await ImageDAO.delete(user=user, id=image_id)
    if check:
        return {'message':'Картинка успешно удалена'}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = 'Картинка не найдена'
        )