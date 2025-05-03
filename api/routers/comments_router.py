from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.deps_utils.utils import get_current_user, verify_comment_owner
from api.dependencies.entity_finder import get_entity_by_id
from api.services.comments_service import CommentService
from core.models import User
from core.models import db_helper
from core.schemas.comment import CommentRead, CommentCreate, CommentUpdate
from core.models import Comment

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


@router.get('',
            response_model=List[CommentRead],
            summary='Get all comments')
@cache(expire=3600)
async def read_comments(
        limit: int = 10,
        offset: int = 0,
        service: CommentService = Depends()
):

    comments = await service.get_all(limit=limit, offset=offset)
    return comments


@router.get('/{comment_id}',
            dependencies=[Depends(get_entity_by_id(Comment, 'comment_id'))],
            response_model=CommentRead,
            summary='Get comment by id')
async def read_comment_by_id(
        comment_id: int,
        service: CommentService = Depends()
):
    comment = await service.get_by_id(comment_id)
    return comment


@router.get('/threads/{comment_id}',
            dependencies=[Depends(get_entity_by_id(Comment, 'comment_id'))],
            response_model=List[CommentRead],
            summary='Get get a comment and thread attached to this comment')
@cache(expire=60)
async def get_threads_by_comment_id(
        comment_id: int,
        service: CommentService = Depends()
):
    thread = await service.get_comment_thread(comment_id)
    return thread


@router.post('',
             response_model=CommentRead,
             summary='Attach new comment to post')
async def add_comment(
        comment: CommentCreate,
        service: CommentService = Depends(),
        user: User = Depends(get_current_user)
):
    comment = await service.insert_item(user=user, comment=comment)
    return comment


@router.put('/{comment_id}',
            response_model=CommentRead,
            dependencies=[Depends(get_entity_by_id(Comment, 'comment_id')), Depends(verify_comment_owner)],
            summary='Update comment by id (for comment author)')
async def update_comment(
        comment_id: int,
        comment: CommentUpdate,
        service: CommentService = Depends(),
        user: User = Depends(get_current_user),
):
    comment = service.update_item(comment_id=comment_id, comment=comment)
    return await comment


@router.delete('/{comment_id}',
               response_model=CommentRead,
               dependencies=[Depends(get_entity_by_id(Comment, 'comment_id')), Depends(verify_comment_owner)],
               summary='Update comment by id (for comment author, post owner and admin)')
async def delete_comment(
        comment_id: int,
        service: CommentService = Depends()
):
    comment = await service.delete_item(comment_id=comment_id)
    return comment
