from typing import Sequence, Optional

from fastapi import HTTPException, Depends
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.repositories.base_repository import BaseRepository, T
from core.models import Reaction, UserCommentReaction
from core.models import db_helper
from core.schemas.reaction import ReactionCreate


class ReactionRepository:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = Reaction

    async def get_all(self, limit, offset) -> Sequence[T]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        reaction = result.scalars().first()
        return reaction

    async def insert_item(self, reaction: ReactionCreate) -> T:
        try:
            reaction = Reaction(**reaction.model_dump())
            self.session.add(reaction)
            await self.session.commit()
            await self.session.refresh(reaction)
            return reaction
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Duplicate entry")
            raise

    async def update_item(self, reaction_id: int, reaction: ReactionCreate) -> Optional[T]:
        reaction_to_update = await self.session.get(Reaction, reaction_id)
        update_data_dict = reaction.model_dump()
        for k, v in update_data_dict.items():
            setattr(reaction_to_update, k, v)
        await self.session.commit()
        return reaction_to_update


    async def delete_by_id(self, reaction_id) -> Optional[T]:
        reaction_to_delete = await self.session.get(Reaction, reaction_id)
        await self.session.delete(reaction_to_delete)
        await self.session.commit()
        return reaction_to_delete


    async def get_all_reactions_to_comment(self, comment_id: int) -> Sequence[T]:
        stmt = (select(UserCommentReaction)
                .options(joinedload(UserCommentReaction.reaction), joinedload(UserCommentReaction.user))
                .where(UserCommentReaction.reaction_id == comment_id)
                )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def leave_reaction_to_comment(self,
                                        reaction_id: int,
                                        comment_id: int,
                                        user_id: int):

        stmt = insert(UserCommentReaction).values(comment_id=comment_id,
                                                  reaction_id=reaction_id,
                                                  user_id=user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return f'Reaction {reaction_id} has been attached to comment {comment_id}'

    async def delete_reaction_to_comment(self,
                                         comment_id: int,
                                         user_id: int):
        stmt = select(UserCommentReaction).where(
            user_id == user_id,
            comment_id == comment_id
        )

        result = await self.session.execute(stmt)
        result = result.scalars().first()
        await self.session.delete(result)
        await self.session.commit()
        return result
