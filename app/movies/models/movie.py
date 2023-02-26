"""Movie, MovieActor Model module"""
from uuid import uuid4
from datetime import date

from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base
from app.utils import generate_fake_url


class MovieActor(Base):
    """Base Model for Movie-Actor"""
    __tablename__ = "movie_actors"
    id = Column(String(50), primary_key=True, default=uuid4)
    movie_id = Column(String(50), ForeignKey('movies.id'))
    actor_id = Column(String(50), ForeignKey('actors.id'))

    def __init__(self, movie_id: str, actor_id: str):
        self.movie_id = movie_id
        self.actor_id = actor_id


class Movie(Base):
    """Base Model for Movie"""
    __tablename__ = "movies"
    __table_args__ = (UniqueConstraint("title", "director_id", name="same_director_different_title"),)

    id = Column(String(50), primary_key=True, default=uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    date_added = Column(Date(), default=date.today())
    year_published = Column(String(5), nullable=False)
    link = Column(String(100), nullable=False, default=generate_fake_url)
    director_id = Column(String(50), ForeignKey("directors.id"))
    genre_id = Column(String(50), ForeignKey("genres.id"))

    actors = relationship('Actor', secondary="movie_actors", back_populates='movies', lazy='subquery')
    users = relationship('User', secondary="user_watch_movies", back_populates='watched_movies', lazy='subquery')

    def __init__(self, title: str, description: str, year_published: str, director_id: str, genre_id: str,
                 date_added: str = date.today()):
        self.title = title
        self.description = description
        self.date_added = date_added
        self.year_published = year_published
        self.director_id = director_id
        self.genre_id = genre_id
