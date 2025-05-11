from fastapi import APIRouter, Depends, HTTPException, status
from src.users.dependencies import get_current_user
from src.projects.dao import ProjectDAO
from src.projects.schemas import Project_add, Project_get, Project_update, Project_add_users
from src.projects.rb import RBProject
from src.users.models import User


router = APIRouter(prefix='/projects', tags=['Работа с проектами'])
Project_get.model_rebuild()
@router.get('/', summary='Get all projects', response_model = list[Project_get])
async def get_all_projects(request_body: RBProject = Depends(), user: str = Depends(get_current_user)):
    return await ProjectDAO.find_all_for_user(user, **request_body.to_dict())

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
async def delete_poject(project_id: int, user: str = Depends(get_current_user)) -> dict:
    check = await ProjectDAO.delete(id = project_id, user = user)
    if check:
        return {'message': f'Проект с id {project_id} удален успешно'}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Проект не найден или вы не являетесь автором"
        )