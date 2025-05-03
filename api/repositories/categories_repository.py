from typing import Sequence, Optional

from asyncpg import UniqueViolationError
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import BaseRepository, T
from core.models import Category, Post
from core.models import db_helper
from core.schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = Category

    async def get_all(self, limit, offset) -> Sequence[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        posts = result.scalars().all()
        if len(posts) == 0:
            raise HTTPException(status_code=404, detail="No categories found")
        return posts

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        category = result.scalars().first()
        return category

    async def get_categories_by_post_id(self, post_id: int) -> Sequence[T]:
        stmt = select(self.model).join(self.model.post).filter(Post.id == post_id)
        result = await self.session.execute(stmt)
        categories = result.unique().scalars().all()
        if categories is None or len(categories) == 0:
            raise HTTPException(status_code=400, detail=f"No categories found with post id={post_id}")
        return categories

    async def insert_item(self, category: CategoryCreate) -> T:
        try:
            category = Category(**category.model_dump())
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
            return category
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Duplicate entry")
            raise


    async def update_item(self, category_id: int, category: CategoryCreate) -> Optional[T]:
        category_to_update = await self.session.get(Category, category_id)
        update_data_dict = category.model_dump()
        for k, v in update_data_dict.items():
            setattr(category_to_update, k, v)
        await self.session.commit()
        return category_to_update

    async def delete_by_id(self, category_id) -> Optional[T]:
        category_to_delete = await self.session.get(Category, category_id)

        await self.session.delete(category_to_delete)
        await self.session.commit()
        return category_to_delete

