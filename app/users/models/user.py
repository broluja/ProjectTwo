from sqlalchemy import Column, String, Boolean, Date, ForeignKey, Integer, UniqueConstraint
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

    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="one_user_one_rating"),)

    def __init__(self, user_id: str, movie_id: str, rating: int = None):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


class UserWatchEpisode(Base):
    __tablename__ = "user_watch_episodes"
    id = Column(String(50), primary_key=True, default=uuid4)
    user_id = Column(String(50), ForeignKey("users.id"))
    episode_id = Column(String(50), ForeignKey("episodes.id"))
    rating = Column(Integer(), nullable=True)

    __table_args__ = (UniqueConstraint("user_id", "episode_id", name="one_user_one_rate"),)

    def __init__(self, user_id: str, episode_id: str, rating: int = None):
        self.user_id = user_id
        self.episode_id = episode_id
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
    verification_code = Column(Integer(), nullable=True)

    watched_movies = relationship('Movie', secondary="user_watch_movies", back_populates='users', lazy='subquery')
    watched_episodes = relationship('Episode', secondary="user_watch_episodes", back_populates='users', lazy='subquery')

    def __init__(self, email: str, password_hashed: str, username: str, date_subscribed: str = date.today(),
                 is_active: bool = True, is_superuser: bool = False, verification_code: int = None):
        self.email = email
        self.password_hashed = password_hashed
        self.username = username
        self.date_subscribed = date_subscribed
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.verification_code = verification_code
