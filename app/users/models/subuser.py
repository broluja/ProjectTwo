"""Subuser Model module"""
from uuid import uuid4
from datetime import date

from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Subuser(Base):
    """Base model for Subuser"""
    __tablename__ = "subusers"
    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_subuser_name"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    date_subscribed = Column(Date(), default=date.today())

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", lazy='subquery')

    def __init__(self, name, user_id: str, date_subscribed=date.today()):
        self.name = name
        self.date_subscribed = date_subscribed
        self.user_id = user_id
