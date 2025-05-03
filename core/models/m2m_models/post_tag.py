from sqlalchemy import ForeignKey, Table, Column, UniqueConstraint

from core.models.base import Base

post_tag = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), index=True,),
    Column("tag_id", ForeignKey("tags.id"), index=True,),
    UniqueConstraint("post_id", "tag_id", name="uq_post_tag"),
    extend_existing=True
)