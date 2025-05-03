from datetime import datetime

from sqlalchemy import String, text, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base


class Comment(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    post_id = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    reply_to: Mapped[int] = mapped_column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), index=True,
                                          nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    post = relationship("Post", back_populates="comment")
    user = relationship("User", back_populates="comment")

    replies = relationship("Comment", backref="parent", remote_side=[id])
