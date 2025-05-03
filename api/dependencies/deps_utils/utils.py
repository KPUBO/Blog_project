import json
import logging
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from redis import asyncio as aioredis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from core.config import settings
from core.models import Comment, Post
from core.models import User
from core.models import db_helper
from core.models.posts_models.post import Statuses
from core.schemas.user import UserRead


REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)

SECRET_KEY = settings.access_token.verification_token_secret
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/jwt/login")
redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="fastapi-users:auth")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logging.info(f'{e}')
        raise credentials_exception

    cached_user = await redis.get(f"user:{user_id}")
    if cached_user:
        return User(**json.loads(cached_user))

    user = await session.execute(
        select(User).filter(User.id == int(user_id))
    )
    user = user.scalars().first()

    if user is None:
        raise credentials_exception

    if user:
        user_cache = UserRead.model_validate(user)
        await redis.setex(f"user:{user_id}", 3600, user_cache.model_dump_json())
    return user


def check_superuser(current_user: User = Depends(get_current_user)):
    if current_user.is_superuser != True:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


async def verify_comment_owner(
        request: Request,
        comment_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Comment).filter(Comment.id == comment_id)
    )
    comment = result.scalars().first()
    post = await session.execute(
        select(Post).filter(Post.id == comment.post_id)
    )
    post = post.scalars().first()
    if request.method == 'PUT':
        if (comment.user_id != current_user.id):
            raise HTTPException(status_code=403,
                                detail=f"This comment with id = {comment_id} is forbidden to update for you")
    if request.method == 'DELETE':
        if comment.user_id != current_user.id:
            if post.author_id != current_user.id:
                if current_user.is_superuser is not True:
                    raise HTTPException(status_code=403,
                                        detail=f"This comment with id = {comment_id} is forbidden to update for you")
    return comment


async def verify_post_owner(
        post_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Post).filter(Post.id == post_id)
    )
    post = result.scalars().first()
    if post.author_id != current_user.id or current_user.is_superuser is not True:
        raise HTTPException(status_code=403,
                            detail=f"This post with id = {post.id} is forbidden to update for you")


async def check_post_status(
        post_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await session.execute(
        select(Post).filter(Post.id == post_id)
    )
    post = result.scalars().first()
    if post.status == Statuses.archived:
        raise HTTPException(status_code=400, detail="This post is archived")


async def increment_post_views(post_id: int,
                               session: AsyncSession = Depends(db_helper.session_getter)):
    stmt = (
        update(Post)
        .where(Post.id == post_id)
        .values(post_views=Post.post_views + 1)
    )
    await session.execute(stmt)
    await session.commit()
