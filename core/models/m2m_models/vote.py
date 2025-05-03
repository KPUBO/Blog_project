import enum

from sqlalchemy import ForeignKey, Table, Column, Enum, Integer, UniqueConstraint

from core.models.base import Base


class VoteStatuses(int, enum.Enum):
    like = 1
    dislike = -1


user_post_votes = Table(
    "user_post_votes", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), index=True,),
    Column("post_id", Integer, ForeignKey("posts.id"), index=True,),
    Column('vote_type', Enum(VoteStatuses)),
    UniqueConstraint("user_id", "post_id", name="uq_user_post"),
    extend_existing=True
)
