from app.tests import TestClass, TestingSessionLocal
from app.users.repositories import UserRepository
from app.users.models import User


class TestUserRepo(TestClass):

    def create_users_for_methods(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})
            user_repository.create({"email": "dummy2@gmail.com", "password_hashed": "123", "username": "dummy2"})
            user_repository.create({"email": "dummy3@gmail.com", "password_hashed": "123", "username": "dummy3"})

    def test_create_user(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})
            assert user.email == "dummy1@gmail.com"
            assert user.username == "dummy1"
            assert user.is_superuser is False
            assert user.is_active is True
