from sqlalchemy import Column, String, Boolean, Date, ForeignKey, Integer
from uuid import uuid4
from datetime import date

from sqlalchemy.orm import relationship

from app.db import Base


class UserWatchMovie(Base):
    __tablename__ = "user_watch_movies"
    id = Column(String(50), primary_key=True, default=uuid4)
    user_id = Column(String(50), ForeignKey("users.id"))
    movie_id = Column(String(50), ForeignKey("movies.id"))
    rating = Column(Integer(), nullable=True)

    def __init__(self, user_id: str, movie_id: str, rating: int = None):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True, default=uuid4)
    email = Column(String(100), unique=True)
    password_hashed = Column(String(100))
    username = Column(String(100))
    date_subscribed = Column(Date(), default=date.today())
    is_active = Column(Boolean)
    is_superuser = Column(Boolean, default=False)

    watched_movies = relationship('Movie', secondary="user_watch_movies", back_populates='users', lazy='subquery')

    def __init__(self, email: str, password_hashed: str, username: str, date_subscribed: str = date.today(),
                 is_active: bool = True, is_superuser: bool = False):
        self.email = email
        self.password_hashed = password_hashed
        self.username = username
        self.date_subscribed = date_subscribed
        self.is_active = is_active
        self.is_superuser = is_superuser
