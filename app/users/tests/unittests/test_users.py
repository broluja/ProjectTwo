"""Test users module"""
import pytest
from sqlalchemy.exc import IntegrityError

from app.base import AppException
from app.tests import TestClass, TestingSessionLocal
from app.users.repositories import UserRepository, SubuserRepository
from app.users.models import User, Subuser


class TestUserRepo(TestClass):
    """Test Users functionalities."""
    superuser = None
    subuser = None

    def create_superuser(self):
        """
        The create_superuser function creates a superuser in the database.
        It is used to create a superuser for testing purposes.
        
        Return: The superuser object.
        """
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            superuser = user_repository.create(
                {"email": "superuser@gmail.com", "password_hashed": "123", "username": "superuser"})
            self.superuser = superuser  # To make this test reusable
            return user_repository.update(superuser, {"is_superuser": True})

    @staticmethod
    def create_users_for_methods():
        """
        The create_users_for_methods function creates 3 users in the database.
        It is used to create a user for each the methods that will be tested.

        Return: A list of users created in the with statement.
        """
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})
            user_repository.create({"email": "dummy2@gmail.com", "password_hashed": "123", "username": "dummy2"})
            user_repository.create({"email": "dummy3@gmail.com", "password_hashed": "123", "username": "dummy3"})

    def test_create_user(self):
        """
        The test_create_user function is used to test the create user function in user.py.
        It creates a new user with dummy data and checks if the email, username and password are correct.

        Return: A user object with the email, username and is_superuser fields set.
        """
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})
            assert user.email == "dummy1@gmail.com"
            assert user.username == "dummy1"
            assert user.is_superuser is False
            assert user.is_active is True

    def test_create_user_integration_error(self):
        """
        The test_create_user_integration_error function is a test that will fail because of an AppException.
        This exception is raised when the user already exists in the database, which means that we cannot create
        a duplicate user. This test ensures that our code works as expected.

        Return: An app exception.
        """
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user_repository.create({"email": "dummy1@gmail.com", "password_hashed": "123", "username": "dummy1"})

    def test_create_superuser(self):
        """
        The test_create_superuser function is a test that creates a superuser and checks
        to see if the user has been created correctly.
        It also checks to see if the user is an admin, which should be true.

        Return: True, superuser@gmail, 'superuser'
        """
        superuser = self.create_superuser()
        assert superuser.is_superuser == True
        assert superuser.email == "superuser@gmail.com"
        assert superuser.username == "superuser"

    def test_get_all_users(self):
        """
        The test_get_all_users function is a test function that creates
        three users in the database and then checks to see if they are all there.
        It does this by creating three users, saving them to the database,
        and then checking for them using a user repository.

        Return: A list of all the users in the database.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all()
        assert len(users) == 3

    def test_get_all_active_users(self):
        """
        Function creates a user and then checks to see if the user is active.
        It does this by creating a new session, creating the users, and then querying for all active users.
        The function asserts that these users are indeed active.

        Return: All the users that are active.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all_active_users()
        assert all(user.is_active for user in users)

    def test_get_all_inactive_users(self):
        """
        The test_get_all_inactive_users function tests the get_all_inactive_users method in UserRepository.
        It creates a user, and then calls the method to retrieve all inactive users. It asserts that there is no
        user returned.

        Return: An empty list.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.read_all_active_users(active=False)
        assert len(users) == 0

    def test_get_user_by_id(self):
        """
        Function tests the get_user_by_id function in user.py by creating a superuser,
        and then using that superusers ID to query for the user and compare it to the original user.
        The test asserts that both users have matching IDs, emails, usernames and passwords.

        Return: The user with the ID of 1.
        """
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
        """
        Function tests the get_user_by_email function in user.py by creating a superuser,
        and then using that superusers email to query for the user object and compare
        it to the original object. The test asserts that both objects are equal.

        Return: The user object with the same ID, email and username as the one created in test_create_user.
        """
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
        """
        The test_get_user_by_email_error function is used to test the
        get_user_by_email function in user.py.
        It creates a new user and then attempts to retrieve that same user by email,
        which should return the newly created
        user object. However, if an unknown email is passed into the function,
        it will raise an exception.

        Return: An app exception.
        """
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user_repository.read_user_by_email("unknown_email@gmail.com")

    def test_search_users_by_email(self):
        """
        Function tests searching user by email

        Return: List of User objects.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            users = user_repository.search_users_by_email("dummy")
        emails = [user.email for user in users]
        assert all(["dummy" in email for email in emails])
        assert len(users) == 3

    def test_update_username(self):
        """
        Function tests the update method of the UserRepository class.
        It creates a user with username dummy2 and email dummy2@gmail.com,
        then updates that user's username to be 'dummy2-updated'
        The test asserts that the updated user's email is still 'dummy2@gmail.com'
        and its new username is 'dummy2-updated'.

        Return: A user object whose username has been updated to 'dummy1-updated'.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_updated = user_repository.update(user, {"username": "dummy1-updated"})
        assert user_updated.email == user.email
        assert user_updated.username == "dummy1-updated"

    def test_update_email(self):
        """
        Function is used to test the update email method in UserRepository.
        It creates a dummy user with an email of 'dummy@gmail.com'
        and then updates that user's email to 'dummy-updated@gmail.com';.
        The assert statement checks if the updated user's email is equal to 'dummy-updated@gmail.com'.

        Return: The email of the user that was updated.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_updated = user_repository.update(user, {"email": "dummy1-updated@gmail.com"})
        assert user_updated.email == "dummy1-updated@gmail.com"
        assert user_updated.username == user.username

    def test_update_email_error(self):
        """
        Function is used to test the update email method of UserRepository.
        It creates a user with email dummy@gmail.com and then tries to
        update it is email to dummy2@gmail.com
        This should raise an IntegrityError because there already exists a user with that email.

        Return: An integrity error.
        """
        self.create_users_for_methods()
        with pytest.raises(IntegrityError):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user = user_repository.read_user_by_email("dummy1@gmail.com")
                user_repository.update(user, {"email": "dummy2@gmail.com"})

    def test_deactivate_user(self):
        """
        Function tests deactivation of user.

        Return: A user object.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_inactive = user_repository.update(user, {"is_active": False})
        assert user.email == user_inactive.email
        assert user.password_hashed == user_inactive.password_hashed
        assert user_inactive.is_active is False

    def test_change_admin_status(self):
        """
        The test_change_admin_status function tests the functionality
        of changing a user's admin status.
        It creates users for the test_change_admin_status function,
        and then changes one of those users' admin status to True.
        The assert statement checks that the email address is equal to
        what was inputted the database, and that
        the password hash is equal to what was inputted the database.

        Return: True.
        """
        self.create_users_for_methods()
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db, User)
            user = user_repository.read_user_by_email("dummy1@gmail.com")
            user_is_superuser = user_repository.update(user, {"is_superuser": True})
        assert user.email == user_is_superuser.email
        assert user.password_hashed == user_is_superuser.password_hashed
        assert user_is_superuser.is_active is True

    def test_get_user_by_code(self):
        """
        Function tests the get_user_by_code function in UserRepository.py
        It creates a dummy user and then updates that user's verification code to 12345. It then checks if the
        get_user_by_code function can find this dummy user by passing in 12345 as an argument, which should return
        the same email address and username as the dummy user created earlier.

        Return: The user with the matching verification code.
        """
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
        """
        Function tests error raised when user tries
        to verify account with some random code.

        Return: AppException error.
        """
        self.create_users_for_methods()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user = user_repository.read_user_by_email("dummy1@gmail.com")
                user_repository.update(user, {"verification_code": 12345})
                user_repository.read_user_by_code(54321)

    def test_delete_user(self):
        """
        Function is used to test the delete-user method in UserRepository.py
        It creates a user with dummy data, then deletes
        that user and checks if it was deleted successfully.

        Return: None.
        """
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
        """
        Function tests creation of subuser.

        Return: A subuser object.
        """
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
        """
        The test_create_subuser_error function tests the create subuser
        function by creating a dummy user and then
        attempting to create another subuser with the same name.
        This should raise an exception.

        Return: A value error.
        """
        self.test_create_subuser()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                user_repository = UserRepository(db, User)
                user = user_repository.read_user_by_email("dummy1@gmail.com")
                subuser_repository = SubuserRepository(db, Subuser)
                attributes = {"name": "Subuser One", "date_subscribed": "2022-02-02", "user_id": user.id}
                subuser_repository.create(attributes)

    def test_read_subuser_by_name(self):
        """
        Function tests the read_subusers_by_name function in the SubuserRepository class.
        It creates a subuser, then reads that subuser using the read_subusers_by_name
        function and asserts that it is equal to self.subuser.

        Return: A subuser object.
        """
        self.test_create_subuser()
        with TestingSessionLocal() as db:
            subuser_repository = SubuserRepository(db, Subuser)
            subuser = subuser_repository.read_subusers_by_name(self.subuser.name, self.subuser.user_id)
        assert subuser.name == self.subuser.name
        assert subuser.user_id == self.subuser.user_id

    def test_read_subuser_by_user_id(self):
        """
        Function tests retrieving subuser by ID.

        Return: A subuser object.
        """
        self.test_create_subuser()
        with TestingSessionLocal() as db:
            subuser_repository = SubuserRepository(db, Subuser)
            subusers = subuser_repository.read_subusers_by_user_id(self.subuser.user_id)
        assert any([subuser.name == self.subuser.name for subuser in subusers])
        assert any([subuser.user_id == self.subuser.user_id for subuser in subusers])
