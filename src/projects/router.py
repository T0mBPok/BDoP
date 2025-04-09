from fastapi import APIRouter

from src.projects.dao import ProjectDAO
from src.projects.schemas import Project_add


router = APIRouter(prefix='/projects', tags=['Работа с проектами'])

@router.get('/', summary='Get all the projects')
async def get_all_projects():
    return await ProjectDAO.get_all()

@router.post('/add/', summary='Add a project')
async def add_projects(project: Project_add):
    
    check = await ProjectDAO.add(**project.model_dump())
    if check:
        return {'message': 'project was succesfully added', 'project':project}
    else:
        return {'message': 'error adding project'}