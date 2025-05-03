from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.tags_repository import TagRepository
from api.services.base_service import BaseService
from core.models import Tag, Post
from core.models import db_helper
from core.schemas.tag import TagCreate


class TagService(BaseService):

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: TagRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self, offset, limit) -> Sequence[Tag]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_by_id(self, tag_id: int) -> Tag:
        return await self.repository.get_by_id(tag_id)

    async def get_tags_by_post_id(self, post_id: int) -> Sequence[Tag]:
        return await self.repository.get_tags_by_post_id(post_id)

    async def insert_item(self, tag: TagCreate) -> Tag:
        tag = await self.repository.insert_item(tag)
        return tag

    async def update_item(self, tag_id: int, tag: TagCreate) -> Optional[Tag]:
        tag = await self.repository.update_item(tag_id, tag)
        return tag

    async def delete_item(self, tag_id: int):
        tag = await self.repository.delete_by_id(tag_id)
        return tag
