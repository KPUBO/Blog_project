from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.reactions_repository import ReactionRepository
from api.services.base_service import BaseService
from core.models import Reaction
from core.models import db_helper
from core.schemas.reaction import ReactionCreate


class ReactionService:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: ReactionRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self, offset, limit) -> Sequence[Reaction]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_by_id(self, reaction_id: int) -> Reaction:
        return await self.repository.get_by_id(reaction_id)

    async def get_all_reactions_to_comment(self, comment_id: int) -> Sequence[Reaction]:
        return await self.repository.get_all_reactions_to_comment(comment_id)

    async def insert_item(self, reaction: ReactionCreate) -> Reaction:
        reaction = await self.repository.insert_item(reaction)
        return reaction

    async def update_item(self, reaction_id: int, reaction: ReactionCreate) -> Optional[Reaction]:
        reaction = await self.repository.update_item(reaction_id, reaction)
        return reaction

    async def delete_item(self, reaction_id: int):
        reaction = await self.repository.delete_by_id(reaction_id)
        return reaction

    async def leave_reaction_to_comment(self, user_id: int,  reaction_id: int, comment_id: int):
        return await self.repository.leave_reaction_to_comment(user_id, reaction_id, comment_id)

    async def delete_reaction_to_comment(self, user_id: int, comment_id: int):
        return await self.repository.delete_reaction_to_comment(user_id, comment_id)

