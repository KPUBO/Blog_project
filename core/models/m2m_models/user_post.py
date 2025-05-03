from sqlalchemy import ForeignKey, Table, Column, UniqueConstraint

from core.models.base import Base

user_post = Table(
    "users_posts",
    Base.metadata,
    Column("author_id", ForeignKey("users.id"), index=True,),
    Column("post_id", ForeignKey("posts.id"), index=True,),
    UniqueConstraint("author_id", "post_id", name="uq_author_post"),
    extend_existing=True
)