"""User Repository module"""
from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository, AppException
from app.users.exceptions import InvalidCredentialsException, InvalidVerificationCode
from app.users.models import User


class UserRepository(BaseCRUDRepository):
    """Repository for User Model"""
    def create(self, attributes: dict):
        """
        The create function creates a new user in the database.
        It takes an attributes dictionary as its only parameter, and returns the created User object.
        If a user with this email already exists, it raises an AppException with code 400.

        Param attributes:dict: Pass in the attributes that are being passed into the create function.
        Return: The created object.
        """
        try:
            return super().create(attributes)
        except IntegrityError as exc:
            self.db.rollback()
            raise AppException(message="User with this email is already registered.", code=400) from exc

    def read_user_by_email(self, email: str):
        """
        Function takes an email address as a string and returns the user object associated with that email.
        If no user is found, it raises an InvalidCredentialsException.

        Param email:str: Query the database for a user with that email address.
        Return: A user object.
        """
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                self.db.rollback()
                raise InvalidCredentialsException
            return user
        except Exception as exc:
            self.db.rollback()
            raise exc

    def search_users_by_email(self, email: str):
        """
        Function searches for users by email.
        It takes in an email as a string and returns a list of User objects that match the search query.

        Param self: Access the database connection.
        Param email:str: Search for a user with the given email.
        Return: A list of users that match the search criteria.
        """
        try:
            return self.db.query(User).filter(User.email.ilike(f"%{email}%")).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def search_user_by_username(self, username: str, search: bool):
        """
        Function searches users by email. If search parameter is False
        then it looks for exact username match.

        Param username: string value, represent User's username.
        Param search: boolean value, defines search method.
        Return: User object if query is successful.
        """
        try:
            if search:
                return self.db.query(User).filter(User.username.ilike(f"%{username}%")).all()
            else:
                return self.db.query(User).filter(User.username == username).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_user_by_code(self, verification_code: int):
        """
        Function takes a verification code as an argument and returns the user object associated with that
        verification code. If no such user exists, it raises an InvalidVerificationCode exception.

        Param verification_code:int: Find the user with that verification code.
        Return: A user object if the verification code is valid.
        """
        try:
            user = self.db.query(User).filter(User.verification_code == verification_code).first()
            if not user:
                self.db.rollback()
                raise InvalidVerificationCode
            return user
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_all_active_users(self, active=True):
        """
        The read_all_active_users function returns all active users in the database.

        Param active=True: Filter the users to only return active users.
        Return: A list of users that are active.
        """
        try:
            return self.db.query(User).filter(User.is_active == active).all()
        except Exception as exc:
            self.db.rollback()
            raise exc
