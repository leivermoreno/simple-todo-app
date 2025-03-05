from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models import TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String(), nullable=False)

    tasks = relationship(
        "Task",
        cascade="all, delete-orphan",
        order_by="Task.completed, desc(Task.modified_at)",
    )
    collaborators = relationship("Collaborator", cascade="all, delete-orphan")
