from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
)
from datetime import datetime

from db import Base


class TimestampMixin:
    modified_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )


class Collaborator(Base, TimestampMixin):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
