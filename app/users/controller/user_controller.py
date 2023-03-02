"""User Controller module"""

import contextlib
from fastapi import HTTPException
from email_validator import validate_email, EmailNotValidError
from starlette.responses import JSONResponse

from app.users.service import UserServices
from app.base.base_exception import AppException
from app.users.service import sign_jwt
from app.users.exceptions import UnknownProfileException, AdminLoginException, UserEmailDoesNotExistsException
from app.users.service import EmailServices
from app.utils import generate_random_int
from .subuser_controller import SubuserController


class UserController:
    """Controller for User routes"""
    @staticmethod
    def create_user(email, password, username):
        """
        Function creates a new user in the database.
        It takes as input an email, password and username. It returns a response with
        status code 200 if the creation was successful, or 400 if not.

        Param email: Receive the email address of the user
        Param password: Store the password of the user
        Param username: Identify the user in the system
        Return: A response object.
        """
        try:
            valid = validate_email(email)
            valid_email = valid.email
        except EmailNotValidError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        try:
            code = generate_random_int(5)
            user = UserServices.create_new_user(valid_email, password, username, code)
            EmailServices.send_code_for_verification(user.email, code)
            return JSONResponse(
                content="Finish your registration. Instructions are sent to your email.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def verify_user(verification_code: int):
        """
        Function is used to verify a user's email address.
        It takes in an integer as a verification code and returns
        the user object associated with that code.

        Param verification_code:int: Verify the user.
        Return: A user object.
        """
        try:
            return UserServices.verify_user(verification_code)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_users():
        """
        The get_all_users function returns all users in the database.

        Return: A list of users.
        """
        try:
            return UserServices.get_all_users()
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_active_users(active=True):
        """
        The get_all_active_users function retrieves all active users from the database.
        It takes an optional parameter, active, which defaults to True. If it is set to False,
        it will retrieve all inactive users instead.

        Param active=True: Filter the users by their active status.
        Return: A list of users that are active.
        """
        try:
            return UserServices.get_all_active_users(active=active)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_by_id(user_id: str):
        """
        Function is used to retrieve a user by their ID.
        It takes in the user_id as an argument and returns the User object associated with that ID.

        Param user_id:str: Specify the user_id of the user that is being retrieved.
        Return: A user object.
        """
        try:
            return UserServices.get_user_by_id(user_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_by_email(email: str):
        """
        The get_user_by_email function is used to retrieve a user by email.
        It takes in an email as a parameter and returns the user object associated with that email.

        Param email:str: Get the user by email
        Return: A dictionary of the user's information.
        """
        try:
            return UserServices.get_user_by_email(email)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def change_password(email: str):
        """
        Function is used to change the password of a user.
        It takes in an email as a parameter and returns the verification code
        that was sent to the user's email address.

        Param email:str: Get the user by email.
        Return: A verification code.
        """
        try:
            user = UserServices.get_user_by_email(email)
            if user:
                code = generate_random_int(5)
                obj = UserServices.generate_verification_code(user.id, code)
                EmailServices.send_code_for_password_reset(user.email, code)
                return obj
            raise UserEmailDoesNotExistsException
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def reset_password_complete(code: int, password_hashed: str):
        """
        The reset_password_complete function takes in a code and password hashed,
        and returns the user object associated with that code. If no user is found,
        it raises an HTTPException with status_code 404. If there is an error in
        the database query or if the password does not match the hashed version of
        the new password, it raises an HTTPException with status_code 400.

        Param code:int: Identify the user who is trying to reset their password
        Param password-hashed:str: Store the hashed password
        Return: The user object.
        """
        try:
            return UserServices.reset_password_complete(code, password_hashed)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_users_by_email(email: str):
        """
        The search_users_by_email function searches for users by email.
        It takes a string as an argument and returns a list of dictionaries, each dictionary representing one user.
        If no users are found, it returns the response 'No users found'.

        Param email:str: Search for users by email.
        Return: A list of users that match the given email.
        """
        try:
            users = UserServices.search_users_by_email(email)
            return users if users else JSONResponse(content="No users found", status_code=200)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_users_by_username(username: str, search: bool = True):
        """
        Function searches users by email. If search parameter is False
        then it looks for exact username match.

        Param username: string value, represent User's username.
        Param search: boolean value, defines search method.
        Return: User object if query is successful.
        """
        try:
            users = UserServices.search_users_by_username(username, search)
            return users if users else JSONResponse(content="No users found", status_code=200)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def login_user(email: str, password: str, username: str):
        """
        Function is used to authenticate a user.
        It takes in an email and password as parameters, and returns a JWT token if the login is successful.
        If the login fails, it raises an HTTPException with status code 400 (Bad Request).

        Param email:str: Identify the user
        Param password:str: Check if the password is correct
        Param username:str: Check if the user is a subuser or not
        Return: A tuple containing the jwt, and the user's ID.
        """
        try:
            user = UserServices.login_user(email, password)
            if user.is_superuser:
                raise AdminLoginException(code=400, message="Use admin login.")
            if user.username == username:
                return sign_jwt(user.id.__str__(), "regular_user"), user.id.__str__()
            user_with_subs = UserController.get_user_with_all_subusers(user.id)
            for sub in user_with_subs.subusers:
                if sub.name == username:
                    return sign_jwt(user.id, "sub_user"), sub.id
            raise UnknownProfileException
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def login_admin(email: str, password: str):
        """
        Function is used to authenticate a user and return an access token.
        It takes in the email and password of the user as parameters, then checks if it exists in the database.
        If it does exist, then we check if that user has admin privileges (is_superuser).
        If they do have admin privileges, then we create a JWT token for them using their ID as payload.
        We also return their ID so that they can be logged into
        the system without having to log back in again.

        Param email:str: Store the email of the user that is trying to log in
        Param password:str: Check if the password is correct
        Return: A tuple containing the jwt, and the user ID.
        """
        try:
            user = UserServices.login_user(email, password)
            if user.is_superuser:
                return sign_jwt(user.id.__str__(), "super_user"), user.id.__str__()
            raise AdminLoginException
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_username(user_id: str, username: str):
        """
        Function updates the username of a user with the given ID.
        It takes in two parameters, user_id and username. It returns a User object.

        Param user_id:str: Specify the user to update.
        Param username:str: Set the new username for a user.
        Return: A user object.
        """
        try:
            return UserServices.update_username(user_id, username)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def change_email(user_id: str, email: str):
        """
        Function allows a user to change their email.
        It takes two parameters, the user_id and the new email address.
        If the new email is already in use by another account, it will return an error message.
        Otherwise, it will update that users' information with their new email.

        Param user_id:str: Identify the user.
        Param email:str: Specify the email address that will be used to change the user's email.
        Return: The user object.
        """
        try:
            valid = validate_email(email)
            valid_email = valid.email
        except EmailNotValidError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        with contextlib.suppress(AppException):
            if UserServices.get_user_by_email(valid_email):
                raise HTTPException(status_code=400, detail="Email in use. You cannot change your email to this one.")
        try:
            return UserServices.change_email(user_id, valid_email)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def deactivate_user(user_id: str, activity: bool = False):
        """
        Function is used to deactivate a user.
        It takes in the user_id of the user that needs to be
        deactivated and returns the updated User object.

        Param user_id:str: Identify the user
        Param activity:bool=False: Determine if the user is active or not
        Return: The user object that was deactivated.
        """
        try:
            return UserServices.change_user_status(user_id, activity)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_with_all_subusers(user_id):
        """
        Function is used to get a user with all of their subusers.
        It takes in the user_id as an argument and returns the User object with all of its subusers.

        Param user_id: Get the user with all subusers.
        Return: A user with all subusers.
        """
        try:
            subusers = SubuserController.get_subusers_by_user_id(user_id)
            user = UserServices.get_user_by_id(user_id)
            user.subusers = subusers
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_user(user_id: str):
        """
        Function is used to delete a user from the database.
        It takes in a string parameter, which is the ID of the user that will be deleted.
        If successful, it returns a response with status code 200, and an object containing
        a message stating that the user was successfully deleted.

        Param user_id:str: Specify the user ID of the user that is to be deleted.
        Return: A response object.
        """
        try:
            UserServices.delete_user(user_id)
            return JSONResponse(content=f"User with ID: {user_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
