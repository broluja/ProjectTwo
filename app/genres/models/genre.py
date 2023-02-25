"""Genre Model module"""
from uuid import uuid4

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Genre(Base):
    """Base Model for Genre"""
    __tablename__ = "genres"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)

    movies = relationship("Movie", lazy='subquery')

    def __init__(self, name: str):
        self.name = name
