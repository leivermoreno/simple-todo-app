from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base
from models import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    name = Column(String(), nullable=False)

    projects = relationship("Project", cascade="all, delete-orphan")
    collaborations = relationship(
        "Collaborator", order_by="desc(Collaborator.modified_at)"
    )
