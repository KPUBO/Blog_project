from datetime import datetime

from pydantic import BaseModel

from core.models.posts_models.post import Statuses


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    pass


class PostCreateCurrUser(PostBase):
    pass


class PostRead(PostBase):
    id: int
    status: Statuses
    updated_at: datetime
    created_at: datetime


class PostUpdate(BaseModel):
    title: str
    body: str
    status: Statuses


class PostsWithVotes(BaseModel):
    post: PostRead
    likes: int
    dislikes: int


class PostCreateScheduling(PostBase):
    published_at: datetime
