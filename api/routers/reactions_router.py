from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies.deps_utils.utils import get_current_user, check_superuser
from api.dependencies.entity_finder import get_entity_by_id
from api.services.reactions_service import ReactionService
from core.models.user_models.user import User
from core.schemas.reaction import ReactionRead, ReactionCreate
from core.models import Comment, Reaction

router = APIRouter(
    prefix='/reactions',
    tags=['Reactions'],
)


@router.get('', response_model=List[ReactionRead],
            summary='Get the list of all reactions')
@cache(expire=60)
async def read_reactions(
        limit: int = 10,
        offset: int = 0,
        service: ReactionService = Depends(),
):
    reactions = await service.get_all(limit=limit, offset=offset)
    return reactions


@router.get('/comments/{comment_id}',
            response_model=List[ReactionRead],
            dependencies=[Depends(get_entity_by_id(Comment, 'comment_id'))],
            summary='Get all reactions for a comment')
async def get_reactions_by_comment(
        comment_id: int,
        service: ReactionService = Depends(),
):
    users_reactions = await service.get_all_reactions_to_comment(comment_id)
    return users_reactions


@router.get('/{reaction_id}',
            response_model=ReactionRead,
            dependencies=[Depends(get_entity_by_id(Reaction, 'reaction_id'))],
            summary='Get reaction by it\'s id')
async def read_reaction_by_id(
        reaction_id: int,
        service: ReactionService = Depends()
):
    reaction = await service.get_by_id(reaction_id)
    return reaction


@router.post('',
             response_model=ReactionRead,
             summary='Add a new reaction')
async def add_reaction(
        reaction: ReactionCreate,
        service: ReactionService = Depends(),
        admin_only: User = Depends(check_superuser)
):
    reaction = service.insert_item(reaction=reaction)
    return await reaction


@router.put('/{reaction_id}',
            response_model=ReactionRead,
            dependencies=[Depends(get_entity_by_id(Reaction, 'reaction_id'))],
            summary='Update reaction from list')
async def update_reaction(
        reaction_id: int,
        reaction: ReactionCreate,
        service: ReactionService = Depends(),
        admin_only: User = Depends(check_superuser)
):
    reaction = service.update_item(reaction_id=reaction_id, reaction=reaction)
    return await reaction


@router.delete('/{reaction_id}',
               response_model=ReactionRead,
               dependencies=[Depends(get_entity_by_id(Reaction, 'reaction_id'))],
               summary='Delete reaction from list')
async def delete_reaction(
        reaction_id: int,
        service: ReactionService = Depends(),
        admin_only: User = Depends(check_superuser)
):
    reaction = await service.delete_item(reaction_id=reaction_id)
    return reaction


@router.post('/leave_reaction/{comment_id}/{reaction_id}',
             dependencies=[Depends(get_entity_by_id(Comment, 'comment_id')),
                           Depends(get_entity_by_id(Reaction, 'reaction_id'))],
             summary='Leave reaction for comment (of current user)')
async def leave_reaction_to_comment(
        comment_id: int,
        reaction_id: int,
        service: ReactionService = Depends(),

        user: User = Depends(get_current_user)
):
    return await service.leave_reaction_to_comment(reaction_id=reaction_id, comment_id=comment_id, user_id=user.id)


@router.delete('/delete_reaction/{comment_id}',
               dependencies=[Depends(get_entity_by_id(Comment, 'comment_id'))],
               summary='Delete reaction for comment (of current user)')
async def delete_reaction_to_comment(
        comment_id: int,
        service: ReactionService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.delete_reaction_to_comment(user_id=user.id, comment_id=comment_id)
