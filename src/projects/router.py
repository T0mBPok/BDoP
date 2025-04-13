from fastapi import APIRouter, Depends

from src.projects.dao import ProjectDAO
from src.projects.schemas import Project_add, Project_get, Project_update
from src.projects.rb import RBProject


router = APIRouter(prefix='/projects', tags=['Работа с проектами'])

@router.get('/', summary='Get all projects', response_model = list[Project_get])
async def get_all_projects(request_body: RBProject = Depends()):
    return await ProjectDAO.find_all(**request_body.to_dict())

@router.post('/', summary='Add a project')
async def add_projects(project: Project_add):
    check = await ProjectDAO.add(**project.model_dump())
    if check:
        return {'message': 'project was succesfully added', 'project':project}
    else:
        return {'message': 'error adding project'}
    
@router.put('/', summary='Update a project')
async def update_project(project: Project_update) -> dict:
    check = await ProjectDAO.update(filter_by={'id': project.id}, 
                                    name = project.name,
                                    description = project.description,
                                    category_color = project.category_color)
    if check:
        return {'message': "Значения успешно изменены", 'project': project}
    else:
        return {'messgae': "Ошибка при изменении значений"}