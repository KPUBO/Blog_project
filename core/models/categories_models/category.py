from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base
from core.models.m2m_models.post_category import post_category


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    post: Mapped[List['Post']] = relationship(
        secondary=post_category, back_populates="category"
    )
