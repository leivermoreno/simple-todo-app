from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(), unique=True, nullable=False)  # TODO index
    password = Column(String(), nullable=False)
    name = Column(String(), nullable=False)

    projects = relationship("Project", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)  # TODO index
    name = Column(String(), nullable=False)

    tasks = relationship("Task", cascade="all, delete-orphan")
    collaborators = relationship("Collaborator", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(ForeignKey("projects.id"), nullable=False)  # TODO index
    text = Column(String(), nullable=False)
    completed = Column(Boolean(), nullable=False, default=False)


class Collaborator(Base):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    project_id = Column(ForeignKey("projects.id"), nullable=False)  # TODO index
