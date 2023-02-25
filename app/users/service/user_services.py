"""User Service module"""
from app.users.repositories import UserRepository, SubuserRepository
from app.db.database import SessionLocal
from app.users.models import User, Subuser
from app.users.exceptions import InvalidCredentialsException, UnverifiedAccountException, InactiveUserException


class UserServices:
    """Service for User routes."""
    @staticmethod
    def create_new_user(email: str, password: str, username: str, code: int):
        """
        The create_new_user function creates a new user in the database.
        It takes as input an email, password, username and verification code.
        The function returns the newly created user.

        Param email:str: Store the email of the user.
        Param password:str: Hash the password.
        Param username:str: Set the username of the new user.
        Param code:int: Verify the user’s email address.
        Return: The user object that was created.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                fields = {"email": email, "password_hashed": password, "username": username, "verification_code": code}
                return repository.create(fields)
        except Exception as exc:
            print(exc)
            raise exc

    @staticmethod
    def verify_user(verification_code: int):
        """
        Function is used to verify a user's email address.
        It takes in a verification code and checks the database for that code.
        If it exists, it updates the user's verification_code field to None.

        Param verification_code:int: Pass the verification code to the function
        Return: The user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_code(verification_code)
                if user:
                    obj = repository.update(user, {"verification_code": None})
                return obj
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_users():
        """
        The get_all_users function returns all users in the database.

        Return: All the users in the database.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_active_users(active: bool = True):
        """
        The get_all_active_users function retrieves all active users from the database.
        It takes one parameter, active, which is a boolean value that defaults to True.
        If the user is not an admin and wants to see only their own information they can set this parameter to False.

        Param active:bool=True: Filter the results of the query.
        Return: A list of all active users.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_all_active_users(active=active)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_user_by_id(user_id: str):
        """
        Function is used to retrieve a user by their ID.
        It takes in the user_id as an argument and returns the User object associated with that ID.

        Param user_id:str: Pass the user_id to the function.
        Return: A user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_by_id(user_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_user_by_email(email: str):
        """
        The get_user_by_email function is used to retrieve a user from the database by their email.
        It takes in an email as a parameter and returns the user object associated with that email.

        Param email:str: Pass the email address of the user
        Return: A user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_user_by_email(email)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_users_by_email(email: str):
        """
        The search_users_by_email function searches for a user by email and returns the user if found.
        It takes an email as a parameter, and returns the user object if found.

        Param email:str: Search for a user by email
        Return: A list of users with the same email address as the input.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.search_users_by_email(email)
        except Exception as exc:
            raise exc

    @staticmethod
    def login_user(email: str, password: str):
        """
        Function is used to authenticate a user by checking the email and password
        provided. If the credentials are valid, then it returns an object of type User.


        Param email:str: Pass the email address of the user logging in
        Param password:str: Store the password entered by the user
        Return: The user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_email(email)
                if user.password_hashed != password:
                    raise InvalidCredentialsException
                if user.verification_code is not None:
                    raise UnverifiedAccountException
                if not user.is_active:
                    raise InactiveUserException
                return user
        except Exception as exc:
            raise exc

    @staticmethod
    def update_username(user_id: str, username: str):
        """
        Function updates the username of a user.

        Param user_id:str: Identify the user to update.
        Param username:str: Update the username of a user.
        Return: The updated user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"username": username}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def change_email(user_id: str, valid_email: str):
        """
        Function is used to change the email of a user.
        It takes in two parameters, user_id and valid_email.
        The function will then check if the new email is already taken by another user or not.
        If it is not, then it will update the database with the new email.

        Param user_id:str: Identify the user to be updated.
        Param valid email:str: Validate the email address.
        Return: None.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"email": valid_email}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def change_user_status(user_id: str, activity: bool = False):
        """
        The change_user_status function is used to change the status of a user.
        It takes two parameters, user_id and activity. If activity is True, then the user will be activated
        and if it is False, the user will be deactivated.

        Param user_id:str: Identify the user to be updated
        Param activity:bool=False: Set the activity status of a user
        Return: The updated user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"is_active": activity}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_admin_status(user_id: str, superuser: bool = True):
        """
        The update_admin_status function is used to update the admin status of a user.
        It takes in two parameters, user_id and superuser. The function first checks if the
        user exists in the database by querying for it using its ID. If it does exist, then
        the function updates its admin status to True or False depending on what was passed into
        the superuser parameter.

        Param user_id:str: Specify, which user we want to update.
        Param superuser:bool=True: Set the is_superuser field to true or false.
        Return: A user object.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"is_superuser": superuser}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def generate_verification_code(user_id: str, code: int):
        """
        Function generates a random code for the user to verify their account.
        It takes in two parameters, user_id and code. The function then uses the SessionLocal() method from
        the database connection file to connect to the database and create a session. It then creates an instance
        of UserRepository using that session and User model class as parameters, which allows us to use all methods
        within that class. The function calls get_user_by_id on the user ID parameter passed into it, which returns
        a single row of data from our users table with that specific ID number (if there is one).

        Param user_id:str: Specify the user that we want to update.
        Param code:int: Generate a random number to be used as the verification code.
        Return: A user object with the verification_code attribute updated.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"verification_code": code}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def reset_password_complete(code: int, password_hashed: str):
        """
        The reset_password_complete function takes in a code and password hashed,
        and updates the user's password to be the hashed version of the new password.

        Param code:int: Identify the user.
        Param password hashed:str: Store the hashed password, and the code:int parameter is used to store
        the verification code.
        Return: A dictionary with the key &quot;success&quot; and value true.
        """
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_code(code)
                updates = {"password_hashed": password_hashed, "verification_code": None}
                return repository.update(user, updates)
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_user(user_id: str):
        """
        Function deletes a user from the database.
        It takes in a user_id as an argument and returns True if the deletion was successful, False otherwise.

        Param user_id:str: Identify the user that is to be deleted.
        Return: The amount rows deleted.
        """
        try:
            with SessionLocal() as db:
                subuser_repo = SubuserRepository(db, Subuser)
                subs = subuser_repo.read_subusers_by_user_id(user_id)
                user_repo = UserRepository(db, User)
                if subs:
                    for sub in subs:
                        subuser_repo.delete(sub.id)
                return user_repo.delete(user_id)
        except Exception as exc:
            raise exc
