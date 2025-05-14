from fastapi import APIRouter, Depends, HTTPException,status
from src.tasks.rb import RBTask
from src.tasks.dao import TaskDAO
from src.tasks.schemas import Task_add, Task_get, Task_update
from src.users.dependencies import get_current_user



router = APIRouter(prefix='/tasks', tags=['Работа с задачами'])

@router.get('/', summary='Get all tasks', response_model=list[Task_get])
async def get_all_tasks(request_body: RBTask = Depends(), user: str = Depends(get_current_user)):
    return await TaskDAO.find_all_for_user(user, **request_body.to_dict())

@router.post('/', summary='Add a task')
async def add_task(task: Task_add, user: str = Depends(get_current_user)):
    check = await TaskDAO.add(author_id = user.id, **task.model_dump())
    if check:
        return {'message': 'The task added succesfully', 'task':task}
    else:
        raise HTTPException(
            status_code=400, 
            detail="Failed to add task: not all required fields are filled."
            )
    
@router.put('/', summary='Update a task')
async def update_task(task: Task_update, user: str = Depends(get_current_user)) -> dict:
    task_update = task.model_dump(exclude_unset=True)
    check = await TaskDAO.update(user=user, filter_by = {'id': task.id}, **task_update)
    if check:
        return {"message": "Изменения успешно сохранены", "task": task}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Задача не найдена или вы не являетесь автором"
        )
    
@router.delete("/", summary='Удалить задание')
async def delete_task(task_id: int, user: str = Depends(get_current_user)) -> dict:
    check = await TaskDAO.delete(user=user, id=task_id)
    if check:
        return {'message': "Задача успешно удалена", 'id': task_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Задача не найдена или вы не являетесь автором"
        )