from sqlalchemy import Column, String, Boolean, DateTime
from uuid import uuid4
from datetime import datetime

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True, default=uuid4)
    email = Column(String(100), unique=True)
    password_hashed = Column(String(100))
    username = Column(String(100))
    date_subscribed = Column(DateTime(), default=datetime.now())
    is_active = Column(Boolean)
    is_superuser = Column(Boolean, default=False)

    def __init__(self, email, password_hashed, username, date_subscribed=datetime.now(), is_active=True,
                 is_superuser=False):
        self.email = email
        self.password_hashed = password_hashed
        self.username = username
        self.date_subscribed = date_subscribed
        self.is_active = is_active
        self.is_superuser = is_superuser
