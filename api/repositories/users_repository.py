from typing import Sequence, Optional

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import BaseRepository, T
from core.models.user_models.user import User
from core.schemas.user import UserCreate
from core.models import db_helper


class UserRepository:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = User

    async def get_all(self, limit, offset) -> Sequence[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        user = result.scalars().first()
        return user

    async def insert_item(self, user: UserCreate) -> T:
        user = User(**user.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_item(self, user_id: int, user: UserCreate) -> Optional[T]:
        user_to_update = await self.session.get(User, user_id)
        update_data_dict = user.model_dump()
        for k, v in update_data_dict.items():
            setattr(user_to_update, k, v)
        await self.session.commit()
        return user_to_update


    async def delete_by_id(self, user_id) -> Optional[T]:
        user_to_delete = await self.session.get(User, user_id)
        await self.session.delete(user_to_delete)
        await self.session.commit()
        return user_to_delete


def get_user_repository(
    session: AsyncSession = Depends(db_helper.session_getter)
) -> UserRepository:
    return UserRepository(session)
