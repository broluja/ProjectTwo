from uuid import uuid4
from datetime import date

from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class MovieActor(Base):
    __tablename__ = "movie_actors"
    id = Column(String(50), primary_key=True, default=uuid4)
    movie_id = Column(String(50), ForeignKey('movies.id'))
    actor_id = Column(String(50), ForeignKey('actors.id'))
    rating = Column(Integer())

    def __init__(self, movie_id: str, actor_id: str, rating: str = None):
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.rating = rating


class Movie(Base):
    __tablename__ = "movies"
    id = Column(String(50), primary_key=True, default=uuid4)
    title = Column(String(100), nullable=False)
    date_added = Column(Date(), default=date.today())
    year_published = Column(String(5), nullable=False)

    actors = relationship('Actor', secondary="movie_actors", back_populates='movies', lazy='subquery')

    def __init__(self, title: str, year_published: str, date_added: str = date.today()):
        self.title = title
        self.date_added = date_added
        self.year_published = year_published
