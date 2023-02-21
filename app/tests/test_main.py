"""Test Class module"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db import Base
from app.main import app

MYSQL_URL_TEST = \
    f"{settings.DB_HOST}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:" \
    f"{settings.DB_PORT}/{settings.DB_NAME_TEST}"

engine = create_engine(MYSQL_URL_TEST, echo=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


class TestClass:
    """Class for running tests."""

    @staticmethod
    def setup_method():
        """Setup any state tied to the execution of the given method in a class.
        This method is invoked for every test method of a class.
        """
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def teardown_method():
        """Teardown any state that was previously setup with a setup method call."""
        Base.metadata.drop_all(bind=engine)
