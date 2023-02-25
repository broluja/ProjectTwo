"""Actor Model module"""
from uuid import uuid4

from sqlalchemy import String, Column, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Actor(Base):
    """Base Model for Actor"""
    __tablename__ = "actors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date())
    country = Column(String(50))

    movies = relationship('Movie', secondary="movie_actors", back_populates='actors', lazy="subquery")
    series = relationship('Series', secondary="series_actors", back_populates='actors', lazy="subquery")

    def __init__(self, first_name: str, last_name: str, date_of_birth: str, country: str):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.country = country
