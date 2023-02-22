"""Series Model module"""
from uuid import uuid4
from datetime import date

from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class SeriesActor(Base):
    """Base Series-Actor model"""
    __tablename__ = "series_actors"
    id = Column(String(50), primary_key=True, default=uuid4)
    series_id = Column(String(50), ForeignKey('series.id'))
    actor_id = Column(String(50), ForeignKey('actors.id'))

    def __init__(self, series_id: str, actor_id: str):
        self.series_id = series_id
        self.actor_id = actor_id


class Series(Base):
    """Base Series model"""
    __tablename__ = "series"
    __table_args__ = (UniqueConstraint("title", "director_id", name="same_director_different_title"),)

    id = Column(String(50), primary_key=True, default=uuid4)
    title = Column(String(100), nullable=False)
    date_added = Column(Date(), default=date.today())
    year_published = Column(String(5), nullable=False)
    director_id = Column(String(50), ForeignKey("directors.id"))
    genre_id = Column(String(50), ForeignKey("genres.id"))

    actors = relationship("Actor", secondary="series_actors", back_populates='series', lazy='subquery')
    episodes = relationship("Episode", cascade="all,delete", backref="series")

    def __init__(
            self,
            title: str,
            year_published: str,
            director_id: str,
            genre_id: str,
            date_added: str = date.today()
                 ):
        self.title = title
        self.date_added = date_added
        self.year_published = year_published
        self.director_id = director_id
        self.genre_id = genre_id
