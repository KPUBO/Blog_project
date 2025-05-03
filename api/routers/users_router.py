from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.dependencies.entity_finder import get_entity_by_id
from api.services.users_service import UserService
from core.models import User
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('',
            response_model=List[UserRead],
            response_model_exclude={"hashed_password", "is_superuser"})
async def read_users(
        limit: int = 10,
        offset: int = 0,
        service: UserService = Depends(),
        current_user: User = Depends(get_current_user),
):
    users = await service.get_all(limit=limit, offset=offset)
    return users




@router.get('/all_users/{user_id}',
            response_model=UserRead,
            response_model_exclude={"hashed_password", "is_superuser"},
            dependencies=[Depends(get_entity_by_id(User, 'user_id'))],)
async def read_user_by_id(
        user_id: int,
        service: UserService = Depends(),
        current_user: User = Depends(get_current_user),
):
    user = await service.get_by_id(user_id)
    return user


@router.delete('/delete_current_user', response_model=UserCreate)
async def delete_user(
        service: UserService = Depends(),
        current_user: User = Depends(get_current_user),
):
    user = await service.delete_item(user_id=current_user.id)
    return user
