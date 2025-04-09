from fastapi import APIRouter

from src.tasks.dao import TaskDAO
from src.tasks.schemas import Task_add
from src.tasks.models import Task


router = APIRouter(prefix='/tasks', tags=['Работа с задачами'])

@router.get('/', summary='Get all tasks', response_model=list(Task))
async def get_all_tasks():
    return await TaskDAO.get_all()

@router.post('/add/', summary='Add a task')
async def add_task(task: Task_add):
    check = await TaskDAO.add_task(**task.model_dump())
    if check:
        return {'message': 'The task added succesfully', 'task':task}
    else:
        return {'message': 'The task was not added! ERROR!'}