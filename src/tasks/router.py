from fastapi import APIRouter, Depends
from src.tasks.rb import RBTask
from src.tasks.dao import TaskDAO
from src.tasks.schemas import Task_add, Task_get, Task_update


router = APIRouter(prefix='/tasks', tags=['Работа с задачами'])

@router.get('/', summary='Get all tasks', response_model=list[Task_get])
async def get_all_tasks(request_body: RBTask = Depends()):
    return await TaskDAO.find_all(**request_body.to_dict())

@router.post('/', summary='Add a task')
async def add_task(task: Task_add):
    check = await TaskDAO.add(**task.model_dump())
    if check:
        return {'message': 'The task added succesfully', 'task':task}
    else:
        return {'message': 'The task was not added! ERROR!'}
    
@router.put('/', summary='Update a task')
async def update_task(task: Task_update) -> dict:
    check = await TaskDAO.update(filter_by = {'id': task.id}, **task.model_dump())
    if check:
        return {"message": "Изменения успешно сохранены", "task": task}
    else:
        return {"message": "Изменения не были сохранены"}
    
@router.delete("/", summary='Удалить задание')
async def delete_task(task_id: int) -> dict:
    check = await TaskDAO.delete(id = task_id)
    if check:
        return {'message': "Задача успешно удалена", 'id': task_id}
    else:
        return {'message': "Ошибка при удалении задачи"}