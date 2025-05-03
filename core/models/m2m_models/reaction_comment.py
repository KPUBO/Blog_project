from sqlalchemy import ForeignKey, Table, Column, UniqueConstraint

from core.models.base import Base

reaction_comment = Table(
    "reactions_comments",
    Base.metadata,
    Column("reaction_id", ForeignKey("reactions.id"), index=True),
    Column("comment_id", ForeignKey("comments.id"), index=True ),
    UniqueConstraint("reaction_id", "comment_id", name="uq_reaction_comment"),
    extend_existing=True
)