import os
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies.deps_utils.utils import get_current_user, verify_post_owner, check_post_status, \
    increment_post_views
from api.dependencies.entity_finder import get_entity_by_id
from api.services.posts_service import PostService
from core.models import User
from core.models.m2m_models.vote import VoteStatuses
from core.schemas.post import PostRead, PostCreate, PostsWithVotes, PostUpdate
from core.models import Post, Category, Tag

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get('',
            response_model=List[PostsWithVotes],
            summary='Get all posts with pagination')
@cache(expire=3600)
async def read_posts(
        limit: int = 10,
        offset: int = 0,
        service: PostService = Depends()
):
    posts = await service.get_all(limit=limit, offset=offset)
    return posts


@router.get('/{post_id}',
            response_model=PostsWithVotes,
            dependencies=[Depends(get_entity_by_id(Post, 'post_id'))],
            summary='Get post by it\'s id')
async def read_post_by_id(
        post_id: int,

        service: PostService = Depends(),

        views: None = Depends(increment_post_views)
):
    post = await service.get_by_id(post_id)
    return post


@router.get('/find/find_posts_by_title',
            response_model=List[PostsWithVotes],
            summary='Find all posts with similar title (context finder)')
async def find_posts_by_title(
        title: str,
        service: PostService = Depends()
):
    posts = await service.get_posts_by_title(title)
    return posts


@router.get('/find/find_posts_by_content',
            response_model=List[PostsWithVotes],
            summary='Find all posts with similar content (context finder)')
async def find_posts_by_content(
        content: str,
        service: PostService = Depends()
):
    posts = await service.get_post_by_content(content)
    return posts


@router.get('/categories/{category_id}/posts',
            response_model=List[PostsWithVotes],
            dependencies=[Depends(get_entity_by_id(Category, 'category_id'))],
            summary='Get all posts by category id')
@cache(expire=3600)
async def get_posts_by_category_id(
        category_id: int,
        service: PostService = Depends()
):
    categories = await service.get_posts_by_category_id(category_id)
    return categories


@router.get('/tags/{tag_id}/posts',
            response_model=List[PostsWithVotes],
            dependencies=[Depends(get_entity_by_id(Tag, 'tag_id'))],
            summary='Get all posts connected with tag')
@cache(expire=60)
async def get_posts_by_tag_id(
        tag_id: int,
        service: PostService = Depends()
):
    posts = await service.get_posts_by_tag_id(tag_id)
    return posts


@router.post('/link/category/{category_id}/posts/{post_id}',
             dependencies=[Depends(get_entity_by_id(Category, 'category_id')),
                           Depends(get_entity_by_id(Post, 'post_id')),
                           Depends(verify_post_owner)],
             summary='Connect post id and category id')
async def link_post_and_category(
        post_id: int,
        category_id: int,
        service: PostService = Depends(),
        post_status_verification: None = Depends(check_post_status)
):
    return await service.link_post_and_category(post_id, category_id)


@router.post('/link/tag/{tag_id}/posts/{post_id}',
             dependencies=[Depends(get_entity_by_id(Tag, 'tag_id')),
                           Depends(get_entity_by_id(Post, 'post_id')),
                           Depends(verify_post_owner)],
             summary='Connect post id and tag id')
async def link_post_and_tag(
        post_id: int,
        tag_id: int,
        service: PostService = Depends(),
        post_status_verification: None = Depends(check_post_status)

):
    return await service.link_post_and_tag(post_id, tag_id)


@router.post('',
             response_model=PostCreate,
             summary='Create post (by other users)')
async def add_post(
        post: PostCreate,
        service: PostService = Depends(),
        current_user: User = Depends(get_current_user)
):
    post = service.insert_item(post=post, author=current_user)
    return await post


@router.put('/{post_id}',
            dependencies=[Depends(verify_post_owner),
                          Depends(get_entity_by_id(Post, 'post_id')), ],
            response_model=PostRead,
            summary='Update post by it\'s id (only for author of post and admin)')
async def update_post(
        post_id: int,
        post: PostUpdate,
        service: PostService = Depends(),
        post_status_verification: None = Depends(check_post_status),
):
    post = service.update_item(post_id=post_id, post=post)
    return await post


@router.delete('/{post_id}/category/{category_id}/delete_link',
               dependencies=[
                   Depends(get_entity_by_id(Post, 'post_id')),
                   Depends(get_entity_by_id(Category, 'category_id')),
                   Depends(verify_post_owner), ],
               summary='Unlink post id and category id')
async def delete_post_category_link(
        post_id: int,
        category_id: int,
        service: PostService = Depends(),
        post_status_verification: None = Depends(check_post_status)
):
    await service.delete_post_category_link(post_id, category_id)
    return 'Link deleted'


@router.delete('/{post_id}/tag/{tag_id}/delete_link',
               dependencies=[
                   Depends(get_entity_by_id(Post, 'post_id')),
                   Depends(get_entity_by_id(Tag, 'tag_id')),
                   Depends(verify_post_owner), ],
               summary='Unlink post id and tag id')
async def delete_post_tag_link(
        post_id: int,
        tag_id: int,
        service: PostService = Depends(),
        post_status_verification: None = Depends(check_post_status)
):
    await service.delete_post_tag_link(post_id, tag_id)
    return 'Link deleted'


@router.delete('/{post_id}',
               response_model=PostRead,
               dependencies=[
                   Depends(get_entity_by_id(Post, 'post_id')),
                   Depends(verify_post_owner), ],
               summary='Delete post by it\'s id')
async def delete_post(
        post_id: int,
        service: PostService = Depends(),
):
    post = await service.delete_item(post_id=post_id)
    return post


@router.post("/scheduling_publishing/{date}",
             summary='Create post (delayed sending)')
async def schedule_post(
        post: PostCreate,
        date: datetime,
        service: PostService = Depends(),
        current_user: User = Depends(get_current_user)
):
    post.author_id = current_user.id
    await service.scheduling_post_publishing(post, date)
    return f'Post will be published at {date}'


@router.post('/vote-for-post/{post_id}',
             dependencies=[Depends(get_entity_by_id(Post, 'post_id'))],
             summary='Like/dislike post')
async def vote_for_post(
        post_id: int,
        vote: VoteStatuses,
        service: PostService = Depends(),
        current_user: User = Depends(get_current_user)
):
    await service.vote_for_post(post_id=post_id, user_id=current_user.id, vote=vote)
    if vote == VoteStatuses.like:
        return 'Liked!'
    return 'Disliked!'


@router.delete('/delete-vote-for-post/{post_id}',
               dependencies=[Depends(get_entity_by_id(Post, 'post_id')),
                             ],
               summary='Delete note of like/dislike post')
async def delete_vote_for_post(
        post_id: int,
        service: PostService = Depends(),
        current_user: User = Depends(get_current_user)
):
    await service.delete_vote_post(post_id=post_id, user_id=current_user.id)
    return 'Vote deleted'


@router.patch('/publish_post/{post_id}',
              response_model=PostRead,
              dependencies=[Depends(get_entity_by_id(Post, 'post_id')),
                            Depends(verify_post_owner)],
              summary='Change post status from draft to published')
async def publish_post(
        post_id: int,
        service: PostService = Depends(),
        current_user: User = Depends(get_current_user)
):
    return await service.publish_post(post_id=post_id, current_user=current_user)

