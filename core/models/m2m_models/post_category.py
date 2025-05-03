from sqlalchemy import ForeignKey, Table, Column, UniqueConstraint

from core.models.base import Base

post_category = Table(
    "posts_categories",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), index=True,),
    Column("category_id", ForeignKey("categories.id"), index=True,),
    UniqueConstraint("post_id", "category_id", name="uq_post_category"),
    extend_existing=True

)
