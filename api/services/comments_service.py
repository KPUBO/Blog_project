from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.comments_repository import CommentRepository
from api.services.base_service import BaseService
from core.models import Comment
from core.models.user_models.user import User
from core.models import db_helper
from core.schemas.comment import CommentCreate, CommentCreateWithoutAuthor


class CommentService:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: CommentRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self, offset, limit) -> Sequence[Comment]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_by_id(self, comment_id: int) -> Comment:
        return await self.repository.get_by_id(comment_id)

    async def get_comment_thread(self, comment_id: int) -> Optional[Sequence[Comment]]:
        return await self.repository.get_comment_thread(comment_id)

    async def insert_item(self, comment: CommentCreate, user: User) -> Comment:
        comment = await self.repository.insert_item(comment, user)
        return comment

    async def update_item(self, comment_id: int, comment: CommentCreate) -> Optional[Comment]:
        comment = await self.repository.update_item(comment_id, comment)
        return comment

    async def delete_item(self, comment_id: int):
        comment = await self.repository.delete_by_id(comment_id)
        return comment
