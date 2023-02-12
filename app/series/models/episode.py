from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Episode(Base):
    __tablename__ = "episodes"
    id = Column(String(50), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)
    series_id = Column(String(50), ForeignKey("series.id"))

    users = relationship('User', secondary="user_watch_episodes", back_populates='watched_episodes', lazy='subquery')

    def __init__(self, name: str, series_id: str):
        self.name = name
        self.series_id = series_id
