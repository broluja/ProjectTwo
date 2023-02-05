from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(String(50), primary_key=True, default=uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(String(100))
    country = Column(String(100))

    user_id = Column(String(50), ForeignKey("users.id"))
    user = relationship("User", lazy='subquery')

    def __init__(self, first_name: str, last_name: str, address: str, country: str, user_id: str):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.country = country
        self.user_id = user_id
