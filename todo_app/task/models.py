from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
from models import TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
    text = Column(String(), nullable=False)
    completed = Column(Boolean(), nullable=False)

    project = relationship("Project", back_populates="tasks")
