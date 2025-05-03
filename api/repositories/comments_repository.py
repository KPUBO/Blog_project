from typing import Sequence, Optional

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import T
from core.models import Comment
from core.models import db_helper
from core.schemas.comment import CommentCreate
from core.models import User


class CommentRepository:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = Comment

    async def get_all(self, limit, offset) -> Sequence[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        comment = result.scalars().first()
        return comment

    async def get_comment_thread(self, comment_id) -> Optional[Sequence[T]]:
        comment_hierarchy = select(Comment).where(Comment.id == comment_id).cte(recursive=True)

        recursive_query = select(
            Comment
        ).join(
            comment_hierarchy,
            Comment.reply_to == comment_hierarchy.c.id
        )

        comment_hierarchy = comment_hierarchy.union_all(recursive_query)

        final_query = select(Comment).join(comment_hierarchy, Comment.id == comment_hierarchy.c.id)

        result = await self.session.execute(final_query)

        return result.scalars().all()

    async def insert_item(self, comment: CommentCreate, user: User) -> T:
        comment = Comment(**comment.model_dump())
        comment.user_id = user.id
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update_item(self, comment_id: int, comment: CommentCreate) -> Optional[T]:
        comment_to_update = await self.session.get(Comment, comment_id)
        update_data_dict = comment.model_dump()
        for k, v in update_data_dict.items():
            setattr(comment_to_update, k, v)
        await self.session.commit()
        return comment_to_update


    async def delete_by_id(self, comment_id) -> Optional[T]:
        comment_to_delete = await self.session.get(Comment, comment_id)
        comment_thread = await self.get_comment_thread(comment_to_delete.id)
        if comment_thread is not None:
            for comment in comment_thread:
                await self.session.delete(comment)
        await self.session.delete(comment_to_delete)
        await self.session.commit()
        return comment_to_delete

