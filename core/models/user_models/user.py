from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


from core.models.base import Base
from core.models.m2m_models.vote import user_post_votes


class User(Base, SQLAlchemyBaseUserTable[int]):
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))

    comment = relationship("Comment", back_populates="user", cascade="all, delete")
    post_vote: Mapped[List["Post"]] = relationship(
        secondary=user_post_votes, back_populates="user_vote"
    )

    __table_args__ = {'extend_existing': True}

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
