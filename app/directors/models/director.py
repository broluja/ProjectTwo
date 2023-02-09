from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db import Base


class Director(Base):
    __tablename__ = "directors"
    id = Column(String(50), primary_key=True, default=uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

    movies = relationship("Movie", lazy='subquery')

    def __init__(self, first_name: str, last_name: str, country: str, ):
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
