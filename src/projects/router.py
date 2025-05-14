from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from src.users.dependencies import get_current_user
from src.projects.dao import ProjectDAO
from src.projects.schemas import Project_add, Project_get, Project_update, Project_add_users
from src.projects.rb import RBProject
from src.users.models import User
import os
import shutil


router = APIRouter(prefix='/projects', tags=['Работа с проектами'])
UPLOAD_DIR = "./project_image"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

Project_get.model_rebuild()
@router.get('/', summary='Get all projects', response_model = list[Project_get])
async def get_all_projects(request: Request, request_body: RBProject = Depends(), user: str = Depends(get_current_user)):
    projects = await ProjectDAO.find_all_for_user(user, **request_body.to_dict())

    base_url = str(request.base_url).rstrip('/')

    projects_with_image_url = []
    for project in projects:
        image_url = None
        if project.image_id:
            image_url = f"{base_url}/{project.project_image.filepath}"
        project_data = Project_get.model_validate(project).model_copy(update={'image_url': image_url})
        projects_with_image_url.append(project_data)

    return projects_with_image_url

@router.post('/', summary='Add a project')
async def add_projects(project: Project_add, user: str = Depends(get_current_user)):
    check = await ProjectDAO.add(author_id = user.id, **project.model_dump())
    if check:
        return {'message': 'project was succesfully added', 'project':project}
    else:
        return {'message': 'error adding project'}
    
@router.put('/', summary='Update a project')
async def update_project(project: Project_update, user: str = Depends(get_current_user)) -> dict:
    update_project = project.model_dump(exclude_unset=True)
    project_id = update_project.pop('id')
    if not update_project:
        raise ValueError("Нет полей для обновления")
    
    check = await ProjectDAO.update(filter_by={'id': project_id}, 
                                    user = user,
                                    **update_project)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Проект не найден или вы не являетесь автором"
    )
    return {'message': 'Проект успешно обновлен', 'project': project}

@router.put('/add_to_project', summary='add users')
async def add_to_project(project: Project_add_users, user: User = Depends(get_current_user)) -> dict:
    if not project.user_ids or not project.id:
        raise ValueError("Недостаточно данных для добавления")
    check = await ProjectDAO.add_to_project(project.id, project.user_ids, user)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Проект не найден или вы не являетесь автором"
        )
    return {'message': 'Пользователи успешно добавлены в проект'}
    
    
@router.delete('/', summary='Удалить проект')
async def delete_poject(project_id: int | None = None, delete_all: bool = False, user: str = Depends(get_current_user)) -> dict:
    check = await ProjectDAO.delete(id = project_id, user = user, delete_all=delete_all)
    if check:
        return {'message': f'Проект с id {project_id} удален успешно'}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Проект не найден или вы не являетесь автором"
        )
        
@router.put('/load_icon', summary="Загрузить иконку проекта")
async def load_icon(project_id: int, file: UploadFile = File(...), user: str = Depends(get_current_user)) -> dict:
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение файла. Разрешены только: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        
    file_loc = f"{UPLOAD_DIR}/{project_id}{file_extension}"

    try:
        with open(file_loc, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении файла: {e}"
        )
        
    await ProjectDAO.load_icon(project_id, filepath=file_loc)
    return {'message': "Иконка успешно загружена"}