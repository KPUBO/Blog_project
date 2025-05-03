from typing import Sequence, Optional

from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from core.models import db_helper
from core.schemas.tag import TagCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import BaseRepository, T
from core.models import Tag, Post


class TagRepository(BaseRepository[Tag]):

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = Tag

    async def get_all(self, limit, offset) -> Sequence[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        tag = result.scalars().first()
        return tag

    async def get_tags_by_post_id(self, post_id: int) -> Sequence[Tag]:
        stmt = select(self.model).join(self.model.post).filter(Post.id == post_id)
        result = await self.session.execute(stmt)
        tags = result.unique().scalars().all()
        if tags is None or len(tags) == 0:
            raise HTTPException(status_code=400, detail=f"No tags found with post id={post_id}")
        return tags

    async def insert_item(self, tag: TagCreate) -> T:
        try:
            tag = Tag(**tag.model_dump())
            self.session.add(tag)
            await self.session.commit()
            await self.session.refresh(tag)
            return tag
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Duplicate entry")
            raise

    async def update_item(self, tag_id: int, tag: TagCreate) -> Optional[T]:
        tag_to_update = await self.session.get(Tag, tag_id)
        update_data_dict = tag.model_dump()
        for k, v in update_data_dict.items():
            setattr(tag_to_update, k, v)
        await self.session.commit()
        return tag_to_update


    async def delete_by_id(self, tag_id) -> Optional[T]:
        tag_to_delete = await self.session.get(Tag, tag_id)
        await self.session.delete(tag_to_delete)
        await self.session.commit()
        return tag_to_delete
