from typing import Sequence, Optional

import sqlalchemy
from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, func, case
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import T
from core.models import Category, post_tag, Tag, Post
from core.models import User, db_helper
from core.models.m2m_models.post_category import post_category
from core.models.m2m_models.vote import user_post_votes, VoteStatuses
from core.models.posts_models.post import Statuses
from core.schemas.post import PostCreate, PostsWithVotes, PostUpdate


class PostRepository:

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
    ):
        self.session = session
        self.model = Post

    async def get_all(self, limit, offset) -> Sequence[T]:
        stmt = (
            select(
                Post,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            )
            .join(user_post_votes, Post.id == user_post_votes.c.post_id, isouter=True)
            .group_by(Post.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            PostsWithVotes(
                post=jsonable_encoder(row[0]),
                likes=row[1],
                dislikes=row[2]
            )
            for row in rows
        ]

    async def get_by_id(self, item_id) -> Optional[T]:
        stmt = (
            select(
                self.model,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            ).filter(self.model.id == item_id)
            .join(user_post_votes, self.model.id == user_post_votes.c.post_id, isouter=True)
            .group_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        post = result.first()
        result = PostsWithVotes(
            post=jsonable_encoder(post[0]),
            likes=post[1],
            dislikes=post[2]
        )
        return result

    async def get_posts_by_title(self, title: str) -> Optional[T]:
        stmt = await self.session.execute(
            select(
                self.model,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            ).where(self.model.title.ilike(f'%{title}%'))
            .join(user_post_votes, self.model.id == user_post_votes.c.post_id, isouter=True)
            .group_by(self.model.id)
        )
        result = stmt.all()
        if len(result) == 0:
            raise HTTPException(status_code=404, detail=f"Posts with title {title} not found")
        return [
            PostsWithVotes(
                post=jsonable_encoder(row[0]),
                likes=row[1],
                dislikes=row[2]
            )
            for row in result
        ]

    async def get_post_by_content(self, content: str) -> Optional[Sequence[T]]:
        stmt = await self.session.execute(
            select(
                self.model,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            ).where(self.model.body.ilike(f'%{content}%'))
            .join(user_post_votes, self.model.id == user_post_votes.c.post_id, isouter=True)
            .group_by(self.model.id)
        )
        result = stmt.all()
        if len(result) == 0:
            raise HTTPException(status_code=404, detail=f"Posts with content {content} not found")
        return [
            PostsWithVotes(
                post=jsonable_encoder(row[0]),
                likes=row[1],
                dislikes=row[2]
            )
            for row in result
        ]

    async def get_posts_by_category_id(self, category_id: int) -> Sequence[T]:
        stmt = (
            select(
                self.model,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            ).join(self.model.category).filter(Category.id == category_id)
            .join(user_post_votes, self.model.id == user_post_votes.c.post_id, isouter=True)

            .group_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        posts = result.all()
        if posts is None or len(posts) == 0:
            raise HTTPException(status_code=404, detail=f"There is no posts with category id={category_id}")
        return [
            PostsWithVotes(
                post=jsonable_encoder(row[0]),
                likes=row[1],
                dislikes=row[2]
            )
            for row in posts
        ]

    async def link_post_and_category(self, post_id: int, category_id: int):
        try:
            stmt = insert(post_category).values(post_id=post_id, category_id=category_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return f'Category {category_id} and post {post_id} are linked'
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Post and category link already exists")

    async def get_posts_by_tag_id(self, tag_id: int) -> Sequence[T]:
        stmt = (
            select(
                self.model,
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.like, 1))).label("likes"),
                func.count(case((user_post_votes.c.vote_type == VoteStatuses.dislike, 1))).label("dislikes")
            ).join(self.model.tag).filter(Tag.id == tag_id)
            .join(user_post_votes, self.model.id == user_post_votes.c.post_id, isouter=True)

            .group_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        posts = result.all()
        if posts is None or len(posts) == 0:
            raise HTTPException(status_code=404, detail=f"No posts found with tag id={tag_id}")
        return [
            PostsWithVotes(
                post=jsonable_encoder(row[0]),
                likes=row[1],
                dislikes=row[2]
            )
            for row in posts
        ]

    async def link_post_and_tag(self, post_id: int, tag_id: int) -> T:
        try:
            stmt = insert(post_tag).values(post_id=post_id, tag_id=tag_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return f'Tag with id={tag_id} and post with id={post_id} are linked'
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Post and tag link already exists")

    async def insert_item(self, post: PostCreate, author: User) -> T:
        try:
            post = Post(**post.model_dump())
            post.author_id = author.id
            post.status = Statuses.draft
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
            return post
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Post is already exists")

    async def update_item(self, post_id: int, post: PostUpdate) -> Optional[T]:

        post_to_update = await self.session.get(Post, post_id)
        try:
            update_data_dict = post.model_dump()
            result = await self.session.execute(
                select(Category).where(Category.name == post.title)
            )
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(status_code=409, detail="Category with this name already exists")
            for k, v in update_data_dict.items():
                setattr(post_to_update, k, v)
            await self.session.commit()
            return post_to_update
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="Post is already exists")

    async def delete_post_category_link(self, post_id: int, category_id: int):
        stmt = delete(post_category).where(
            post_category.c.post_id == post_id,
            post_category.c.category_id == category_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_post_tag_link(self, post_id: int, tag_id: int):
        stmt = delete(post_tag).where(
            post_tag.c.post_id == post_id,
            post_tag.c.tag_id == tag_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_by_id(self, post_id) -> Optional[T]:
        post_to_delete = await self.session.get(Post, post_id)
        await self.session.delete(post_to_delete)
        await self.session.commit()
        return post_to_delete

    async def scheduling_post_publishing(self, post: dict):
        try:
            post = Post(**post)
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Post is already published")

    async def vote_for_post(self, post_id: int, vote: int, user_id: int) -> T:
        try:
            stmt = insert(user_post_votes).values(
                user_id=user_id,
                post_id=post_id,
                vote_type=vote
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return stmt

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=409, detail=f"You have voted for this post!")

    async def delete_vote_post(self, post_id: int, user_id: int):

        stmt = select(user_post_votes).where(user_post_votes.c.post_id == post_id,
                                           user_post_votes.c.user_id == user_id)
        result = await self.session.execute(stmt)

        if result.scalar() is None:
            raise HTTPException(status_code=404, detail=f"No votes for this post!")

        stmt = delete(user_post_votes).where(
            user_post_votes.c.post_id == post_id,
            user_post_votes.c.user_id == user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()


    async def show_votes_for_posts(self, post_id: int):
        stmt = select(user_post_votes).where(user_post_votes.c.post_id == post_id)
        result = await self.session.execute(stmt)
        posts = result.scalars().all()
        likes, dislikes = 0, 0

        for post in posts:
            if post.vote_type == VoteStatuses.like:
                likes += 1
            if post.vote_type == VoteStatuses.dislike:
                dislikes += 1
        return likes, dislikes

    async def publish_post(self, post_id: int, current_user: User):
        stmt = (
            select(
                self.model
            ).filter(self.model.id == post_id)
        )
        result = await self.session.execute(stmt)
        post = result.scalars().first()

        if post.author_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not authorized to publish this post')

        if post.status == Statuses.draft:
            post.status = Statuses.published
            await self.session.commit()
            return post

        if post.status == Statuses.published:
            raise HTTPException(status_code=400, detail=f"Post is already published")
        if post.status == Statuses.archived:
            raise HTTPException(status_code=400, detail=f"Post is archived")
