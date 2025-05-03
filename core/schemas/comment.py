from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    post_id: int
    content: str
    reply_to: Optional[int]


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    updated_at: datetime
    created_at: datetime

class CommentUpdate(BaseModel):
    content: str

class CommentCreateWithoutAuthor(CommentBase):
    pass
