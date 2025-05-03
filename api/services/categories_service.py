from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.categories_repository import CategoryRepository
from api.services.base_service import BaseService
from core.models import Category, Post
from core.models import db_helper
from core.schemas.category import CategoryCreate


class CategoryService:
    def __init__(
        self,
        session: AsyncSession = Depends(db_helper.session_getter),
        repo: CategoryRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self, offset, limit) -> Sequence[Category]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_by_id(self, category_id: int) -> Category:
        return await self.repository.get_by_id(category_id)

    async def get_categories_by_post_id(self, category_id: int) -> Sequence[Post]:
        return await self.repository.get_categories_by_post_id(category_id)

    async def insert_item(self, category: CategoryCreate) -> Category:
        category = await self.repository.insert_item(category)
        return category

    async def update_item(self, category_id: int, category: CategoryCreate) -> Optional[Category]:
        category = await self.repository.update_item(category_id, category)
        return category

    async def delete_item(self, category_id: int):
        category = await self.repository.delete_by_id(category_id)
        return category
