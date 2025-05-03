from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies.entity_finder import get_entity_by_id
from api.services.tags_service import TagService
from core.schemas.tag import TagRead, TagCreate
from core.models import Tag, Post

router = APIRouter(
    prefix='/tags',
    tags=['Tags'],
)


@router.get('',
            response_model=List[TagRead],
            summary='Get list of all tags')
@cache(expire=60)
async def read_tags(
        limit: int = 10,
        offset: int = 0,
        service: TagService = Depends(),
):
    tags = await service.get_all(limit=limit, offset=offset)
    return tags


@router.get('/{tag_id}',
            response_model=TagRead,
            dependencies=[Depends(get_entity_by_id(Tag, 'tag_id'))],
            summary='Get tag by id')
async def read_tag_by_id(
        tag_id: int,
        service: TagService = Depends(),
):
    tag = await service.get_by_id(tag_id)
    return tag


@router.get('/{post_id}/tags',
            response_model=List[TagRead],
            dependencies=[Depends(get_entity_by_id(Post, 'post_id'))],
            summary='Get all tags connected with post')
async def get_tags_by_post_id(
        post_id: int,
        service: TagService = Depends(),
):
    posts = await service.get_tags_by_post_id(post_id)
    return posts


@router.post('',
             response_model=TagRead,
             summary='Add a new tag'
             )
async def add_tag(
        tag: TagCreate,
        service: TagService = Depends(),
):
    tag = service.insert_item(tag=tag)
    return await tag


@router.put('/{tag_id}',
            response_model=TagRead,
            dependencies=[Depends(get_entity_by_id(Tag, 'tag_id'))],
            summary='Update tag')
async def update_tag(
        tag_id: int,
        tag: TagCreate,
        service: TagService = Depends(),
):
    tag = service.update_item(tag_id=tag_id, tag=tag)
    return await tag


@router.delete('/{tag_id}',
               response_model=TagRead,
               dependencies=[Depends(get_entity_by_id(Tag, 'tag_id'))],
               summary='Delete tag')
async def delete_tag(
        tag_id: int,
        service: TagService = Depends(),
):
    tag = await service.delete_item(tag_id=tag_id)
    return tag
