from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class TimestampMixin:
    modified_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    name = Column(String(), nullable=False)

    projects = relationship("Project", cascade="all, delete-orphan")


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


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
    text = Column(String(), nullable=False)
    completed = Column(Boolean(), nullable=False)

    project = relationship("Project", back_populates="tasks")


class Collaborator(Base, TimestampMixin):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
