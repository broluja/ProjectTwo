from sqlalchemy import Column, String, Boolean, Date
from uuid import uuid4
from datetime import date

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True, default=uuid4)
    email = Column(String(100), unique=True)
    password_hashed = Column(String(100))
    username = Column(String(100))
    date_subscribed = Column(Date(), default=date.today())
    is_active = Column(Boolean)
    is_superuser = Column(Boolean, default=False)

    def __init__(self, email, password_hashed, username, date_subscribed=date.today(), is_active=True,
                 is_superuser=False):
        self.email = email
        self.password_hashed = password_hashed
        self.username = username
        self.date_subscribed = date_subscribed
        self.is_active = is_active
        self.is_superuser = is_superuser
