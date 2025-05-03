from sqlalchemy import ForeignKey, Column, UniqueConstraint, Integer
from sqlalchemy.orm import relationship

from core.models.base import Base


class UserCommentReaction(Base):
    __tablename__ = "users_comments_reactions"

    __table_args__ = (UniqueConstraint('user_id', 'comment_id', 'reaction_id', name='uq_users_comments_reactions'),)

    user_id = Column(Integer, ForeignKey("users.id"), index=True,)
    comment_id = Column(Integer, ForeignKey("comments.id"), index=True,)
    reaction_id = Column(Integer, ForeignKey("reactions.id"), index=True,)

    user = relationship("User", backref="users_comments_reactions")
    comment = relationship("Comment", backref="users_comments_reactions")
    reaction = relationship("Reaction", backref="users_comments_reactions")
