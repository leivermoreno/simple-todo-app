from sqlalchemy import (
    Column,
    Integer,
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
