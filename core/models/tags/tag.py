from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base
from core.models.m2m_models.post_tag import post_tag


class Tag(Base):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    post: Mapped[List["Post"]] = relationship(
        secondary=post_tag, back_populates="tag"
    )
