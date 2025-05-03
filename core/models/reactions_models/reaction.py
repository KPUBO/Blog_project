from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from core.models.base import Base


class Reaction(Base):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
