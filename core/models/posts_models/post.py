import enum
from datetime import datetime
from typing import List

from sqlalchemy import String, Enum, text, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base
from core.models.categories_models.category import Category
from core.models.m2m_models.post_category import post_category
from core.models.m2m_models.post_tag import post_tag
from core.models.m2m_models.vote import user_post_votes
from core.models.tags.tag import Tag


class Statuses(enum.Enum):
    draft = 'draft'
    published = 'published'
    archived = 'archived'


class Post(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Statuses] = mapped_column(Enum(Statuses), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True,
                                           nullable=False)
    post_views: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))

    category: Mapped[List["Category"]] = relationship(
        secondary=post_category, back_populates="post"
    )
    tag: Mapped[List["Tag"]] = relationship(
        secondary=post_tag, back_populates="post"
    )
    user_vote: Mapped[List["User"]] = relationship(
        secondary=user_post_votes, back_populates="post_vote"
    )

    comment = relationship("Comment", back_populates="post", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint('title', name='unique_post'),
    )



