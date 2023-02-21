"""Subuser Model module"""
from uuid import uuid4
from datetime import date

from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class Subuser(Base):
    """Base model for Subuser"""
    __tablename__ = "subusers"
    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_subuser_name"),)
    id = Column(String(50), primary_key=True, default=uuid4)
    name = Column(String(100), default="Subuser")
    date_subscribed = Column(Date(), default=date.today())

    user_id = Column(String(50), ForeignKey("users.id"))
    user = relationship("User", lazy='subquery')

    def __init__(self, name, user_id: str, date_subscribed=date.today()):
        self.name = name
        self.date_subscribed = date_subscribed
        self.user_id = user_id
