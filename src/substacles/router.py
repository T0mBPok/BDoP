from fastapi import APIRouter, Depends, HTTPException, status
from src.users.dependencies import get_current_user
from src.substacles.schemas import add_subtit
from src.substacles.dao import SubtitDAO
from src.substacles.rb import RBSubtit
from src.substacles.schemas import GetSubtit, UpdateSubtit


router = APIRouter(prefix='/substicles', tags=["Работа с подзадачами"])

@router.post('/', summary="Add a subtit")
async def add_subtit(subtit: add_subtit, user: str = Depends(get_current_user)):
    check = await SubtitDAO.add(author_id = user.id, **subtit.model_dump())
    if check:
        return {'message': 'The subtit added succesfully', 'subtit':subtit}
    else:
        raise HTTPException(
            status_code=400, 
            detail="Failed to add subtit: not all required fields are filled."
            )
        
@router.get('/', summary='Get a subtit', response_model=list[GetSubtit])
async def get_substacles(request_body: RBSubtit = Depends(), user: str = Depends(get_current_user)):
    return await SubtitDAO.find_all_for_user(user, **request_body.to_dict())

@router.put('/', summary='Update a subtit')
async def update_subtit(subtit: UpdateSubtit, user: str = Depends(get_current_user)):
    subtit_update = subtit.model_dump(exclude_unset=True)
    check = await SubtitDAO.update(user=user, filter_by = {'id': subtit.id}, **subtit_update)
    if check:
        return {"message": "Изменения успешно сохранены", "task": subtit}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Задача не найдена или вы не являетесь автором"
        )
        
@router.delete('/', summary='Delete a subtit')
async def delete_subtit(subtit_id: int | None = None, delete_all: bool = False, user:str = Depends(get_current_user)):
    check = await SubtitDAO.delete(user=user, id=subtit_id, delete_all=delete_all)
    if check:
        return {'message': "Задача успешно удалена", 'id': subtit_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Задача не найдена или вы не являетесь автором"
        )