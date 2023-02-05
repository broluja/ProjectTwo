from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Subuser(Base):
    __tablename__ = "subusers"
    id = Column(String(50), primary_key=True, default=uuid4)
    name = Column(String(100))
    date_subscribed = Column(DateTime(), default=datetime.now())

    user_id = Column(String(50), ForeignKey("users.id"))
    user = relationship("User", lazy='subquery')

    def __init__(self, name, user_id: str, date_subscribed=datetime.now()):
        self.name = name
        self.date_subscribed = date_subscribed
        self.user_id = user_id
