"""Database settings module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings as sttg

DATABASE_URL = f"postgresql://{sttg.DB_USER}:{sttg.DB_PASSWORD}@{sttg.DB_HOST}:{sttg.DB_PORT}/{sttg.DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
