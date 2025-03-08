from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


from db import Base
from models import TimestampMixin


class Collaborator(Base, TimestampMixin):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    project_id = Column(ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="collaborators")
    user = relationship("User", back_populates="collaborations")
