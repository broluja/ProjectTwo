import pytest

from app.base import AppException
from app.tests import TestClass, TestingSessionLocal
from app.users.repositories import UserRepository, SubuserRepository
from app.users.models import User, Subuser


class TestUserRepo(TestClass):

    def create_superuser(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            superuser = user_repository.create(
                {"email": "superuser@gmail.com", "password_hashed": "123", "username": "superuser"})
            self.superuser = superuser  # To make this test reusable
            return user_repository.update(superuser, {"is_superuser": True})

    @staticmethod
    def create_users_for_methods():
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

    def test_create_user_integration_error(self):
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})

    def test_create_superuser(self):
        superuser = self.create_superuser()
        assert superuser.is_superuser == True
        assert superuser.email == "superuser@gmail.com"
        assert superuser.username == "superuser"

    def test_get_all_users(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all()
        assert len(users) == 3

    def test_get_all_active_users(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all_active_users()
        assert all(user.is_active for user in users)

    def test_get_all_inactive_users(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all_active_users(active=False)
        assert len(users) == 0

    def test_get_user_by_id(self):
        self.create_superuser()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all()
            user = user_repository.read_by_id(users[0].id)
        assert users[0].id == user.id
        assert users[0].email == user.email
        assert users[0].username == user.username
        assert users[0].password_hashed == user.password_hashed

    def test_get_user_by_email(self):
        self.create_superuser()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all()
            user = user_repository.read_user_by_email(users[0].email)
        assert users[0].id == user.id
        assert users[0].email == user.email
        assert users[0].username == user.username
        assert users[0].password_hashed == user.password_hashed

    def test_get_user_by_email_error(self):
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user_repository.read_user_by_email("unknown_email@gmail.com")

    def test_search_users_by_email(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.search_users_by_email("dummy")
        emails = [user.email for user in users]
        assert all(["dummy" in email for email in emails])
        assert len(users) == 3

    def test_update_username(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_updated = user_repository.update(user, {"username": "dummy1-updated"})
        assert user_updated.email == user.email
        assert user_updated.username == "dummy1-updated"

    def test_deactivate_user(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_inactive = user_repository.update(user, {"is_active": False})
        assert user.email == user_inactive.email
        assert user.password_hashed == user_inactive.password_hashed
        assert user_inactive.is_active == False

    def test_change_admin_status(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_is_superuser = user_repository.update(user, {"is_superuser": True})
        assert user.email == user_is_superuser.email
        assert user.password_hashed == user_is_superuser.password_hashed
        assert user_is_superuser.is_active == True

    def test_get_user_by_code(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_with_code = user_repository.update(user, {"verification_code": 12345})
            obj = user_repository.read_user_by_code(12345)
        assert user_with_code.email == obj.email
        assert user_with_code.username == obj.username
        assert user_with_code.password_hashed == obj.password_hashed

    def test_get_user_by_code_error(self):
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user = user_repository.read_user_by_email("dummy1@gmail.com")
                user_repository.update(user, {"verification_code": 12345})
                user_repository.read_user_by_code(54321)

    def test_delete_user(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_repository.delete(user.id)
            users = user_repository.read_all()
        assert len(users) == 2
        for obj in users:
            assert obj.email != user.email
            assert obj.username != user.username

    def test_create_subuser(self):
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            subuser_repository = SubuserRepository(db, Subuser)
            attributes = {"name": "Subuser One", "date_subscribed": "2022-02-02", "user_id": user.id}
            subuser = subuser_repository.create(attributes)
            self.subuser = subuser  # To make this test reusable
        assert subuser.name == "Subuser One"
        assert subuser.user_id == user.id

    def test_create_subuser_error(self):
        self.test_create_subuser()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user = user_repository.read_user_by_email("dummy1@gmail.com")
                subuser_repository = SubuserRepository(db, Subuser)
                attributes = {"name": "Subuser One", "date_subscribed": "2022-02-02", "user_id": user.id}
                subuser_repository.create(attributes)

    def test_read_subuser_by_name(self):
        self.test_create_subuser()
        with TestingSessionLocal() as db:
            subuser_repository = SubuserRepository(db, Subuser)
            subuser = subuser_repository.read_subusers_by_name(self.subuser.name, self.subuser.user_id)
        assert subuser.name == self.subuser.name
        assert subuser.user_id == self.subuser.user_id

    def test_read_subuser_by_user_id(self):
        self.test_create_subuser()
        with TestingSessionLocal() as db:
            subuser_repository = SubuserRepository(db, Subuser)
            subusers = subuser_repository.read_subusers_by_user_id(self.subuser.user_id)
        assert any([subuser.name == self.subuser.name for subuser in subusers])
        assert any([subuser.user_id == self.subuser.user_id for subuser in subusers])
