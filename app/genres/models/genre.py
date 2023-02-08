from uuid import uuid4

from sqlalchemy import String, Column

from app.db import Base


class Genre(Base):
    __tablename__ = "genres"
    id = Column(String(50), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name
