"""User Controller module"""
from fastapi import HTTPException, Response
from email_validator import validate_email, EmailNotValidError

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
        try:
            valid = validate_email(email)
            valid_email = valid.email
        except EmailNotValidError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        try:
            code = generate_random_int(5)
            user = UserServices.create_new_user(valid_email, password, username, code)
            EmailServices.send_code_for_verification(user.email, code)
            return Response(content="Finish your registration. Instructions are sent to your email.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def verify_user(verification_code: int):
        try:
            user = UserServices.verify_user(verification_code)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_users():
        try:
            users = UserServices.get_all_users()
            return users
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_active_users(active=True):
        try:
            users = UserServices.get_all_active_users(active=active)
            return users
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_by_id(user_id: str):
        try:
            user = UserServices.get_user_by_id(user_id)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_by_email(email: str):
        try:
            user = UserServices.get_user_by_email(email)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def change_password(email: str):
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
        try:
            user = UserServices.reset_password_complete(code, password_hashed)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_users_by_email(email: str):
        try:
            users = UserServices.search_users_by_email(email)
            if not users:
                return Response(content="No users found", status_code=200)
            return users
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def login_user(email: str, password: str, username: str):
        try:
            user = UserServices.login_user(email, password)
            if user.is_superuser:
                raise AdminLoginException(code=400, message="Use admin login.")
            if user.username == username:
                return sign_jwt(user.id, "regular_user"), user.id
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
        try:
            user = UserServices.login_user(email, password)
            if user.is_superuser:
                return sign_jwt(user.id, "super_user"), user.id
            raise AdminLoginException
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_username(user_id: str, username: str):
        try:
            user = UserServices.update_username(user_id, username)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def change_email(user_id: str, email: str):
        try:
            valid = validate_email(email)
            valid_email = valid.email
        except EmailNotValidError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if UserServices.get_user_by_email(valid_email):
            raise HTTPException(status_code=400, detail="Email in use. You cannot change your email to this one.")
        try:
            user = UserServices.change_email(user_id, valid_email)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def deactivate_user(user_id: str, activity: bool = False):
        try:
            user = UserServices.change_user_status(user_id, activity)
            return user
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_user_with_all_subusers(user_id):
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
        try:
            UserServices.delete_user(user_id)
            return Response(content=f"User with ID: {user_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
