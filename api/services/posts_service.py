import json
from datetime import datetime
from typing import Sequence, Optional

from celery.result import AsyncResult
from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.deps_utils.utils import get_current_user
from api.repositories.posts_repository import PostRepository
from api.services.base_service import BaseService
from core.models import Post, Category
from core.models.m2m_models.vote import VoteStatuses
from core.models import User, db_helper
from core.schemas.post import PostCreate, PostUpdate

from api.scheduling.celery_worker import create_post_task, celery_app


class PostService:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: PostRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self, offset, limit):
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_by_id(self, post_id: int):
        return await self.repository.get_by_id(post_id)

    async def get_posts_by_title(self, title: str) -> Optional[Sequence[Post]]:
        return await self.repository.get_posts_by_title(title)

    async def get_post_by_content(self, content: str) -> Optional[Sequence[Post]]:
        return await self.repository.get_post_by_content(content)

    async def get_posts_by_category_id(self, post_id: int) -> Sequence[Post]:
        return await self.repository.get_posts_by_category_id(post_id)

    async def link_post_and_category(self, post_id: int, category_id: int):
        return await self.repository.link_post_and_category(post_id, category_id)

    async def get_posts_by_tag_id(self, tag_id: int) -> Sequence[Post]:
        return await self.repository.get_posts_by_tag_id(tag_id)

    async def link_post_and_tag(self, post_id: int, tag_id: int):
        return await self.repository.link_post_and_tag(post_id, tag_id)

    async def insert_item(self, post: PostCreate, author: User) -> Post:
        post = await self.repository.insert_item(post, author)
        return post

    async def update_item(self, post_id: int, post: PostUpdate) -> Optional[Post]:
        post = await self.repository.update_item(post_id, post)
        return post

    async def delete_post_category_link(self, post_id: int, category_id: int):
        return await self.repository.delete_post_category_link(post_id, category_id)

    async def delete_post_tag_link(self, post_id: int, tag_id: int):
        return await self.repository.delete_post_tag_link(post_id, tag_id)

    async def delete_item(self, post_id: int):
        post = await self.repository.delete_by_id(post_id)
        return post

    async def scheduling_post_publishing(self, post: PostCreate, date: datetime):
        if await self.repository.get_posts_by_title(post.title) is None:
            delay_seconds = (date - datetime.utcnow()).total_seconds()
            dict_post = jsonable_encoder(post)
            task = create_post_task.apply_async(args=[dict(dict_post)], countdown=delay_seconds)
            result = AsyncResult(task.id, app=celery_app)
            return result
        else:
            raise HTTPException(status_code=400, detail='Post is already published')

    async def vote_for_post(self, post_id: int, user_id: int, vote: VoteStatuses):
        vote = await self.repository.vote_for_post(post_id=post_id, user_id=user_id, vote=vote.value)
        return vote

    async def delete_vote_post(self, post_id: int, user_id: int):
        vote = await self.repository.delete_vote_post(post_id=post_id, user_id=user_id)
        return vote

    async def publish_post(self, post_id: int, current_user: User):
        post = await self.repository.publish_post(post_id, current_user)
        return post
