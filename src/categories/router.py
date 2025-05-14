from fastapi import APIRouter, Depends, HTTPException, status
from src.users.dependencies import get_current_user
from src.categories.schemas import CategoryAdd, CategoryGet
from src.categories.dao import CategoryDAO
from src.users.models import User
from src.categories.rb import RBCategory

router = APIRouter(prefix='/categories', tags=["РаБота с категориями"])
@router.post('/', summary="Add a category")
async def add_category(category: CategoryAdd, user: str = Depends(get_current_user)):
    check = await CategoryDAO.add(author_id=user.id, **category.model_dump())
    if check:
        return{"mesage": "Категория успешно добавлена"}
    else:
        raise HTTPException(
            status_code=400, 
            detail="Failed to add category: not all required fields are filled."
            )

@router.get('/', summary="Get all categories", response_model=list[CategoryGet])
async def get_all_categories(requset_body: RBCategory = Depends(), user: User = Depends(get_current_user)):
    return await CategoryDAO.find_all_for_user(user, **requset_body.to_dict())

@router.put('/', summary="Update a category")
async def update_category(category: CategoryGet, user: User = Depends(get_current_user)):
    update_category = category.model_dump(exclude_unset=True)
    category_id = update_category.pop('id')
    if not update_category:
        raise ValueError("Нет полей для обновления")
    check = await CategoryDAO.update(filter_by={'id': category_id}, 
                                    user = user,
                                    **update_category)
    if check:
        return {"message": "Категория успешно обновлена"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Category is not found or you do not have permission to it."
        )

@router.delete('/', summary='Delete a category')
async def delete_category(category_id: int, user: str = Depends(get_current_user)):
    check = await CategoryDAO.delete(id = category_id, user = user)
    if check:
        return {"message": "Категория успешно удалена"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Category is not found or you are do not have permission to it."
        )