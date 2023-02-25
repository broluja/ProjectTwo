"""Admin Model module"""
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Admin(Base):
    """Base Model for Admin"""
    __tablename__ = "admins"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", lazy='subquery')

    def __init__(self, first_name: str, last_name: str, address: str, country: str, user_id: str):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.country = country
        self.user_id = user_id
