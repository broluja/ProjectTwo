"""Genre Model module"""
from uuid import uuid4

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from app.db import Base


class Genre(Base):
    """Base Model for Genre"""
    __tablename__ = "genres"
    id = Column(String(50), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)

    movies = relationship("Movie", lazy='subquery')

    def __init__(self, name: str):
        self.name = name
