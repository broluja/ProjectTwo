from fastapi import HTTPException, Response
from email_validator import validate_email, EmailNotValidError

from app.users.service import UserServices
from .subuser_controller import SubuserController
from app.base.base_exception import AppException
from app.users.service import sign_jwt


class UserController:

    @staticmethod
    def create_user(email, password, username):
        try:
            valid = validate_email(email)
            valid_email = valid.email
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            user = UserServices.create_new_user(valid_email, password, username)
            return user
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_users():
        try:
            users = UserServices.get_all_users()
            return users
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_user_by_id(user_id: str):
        try:
            user = UserServices.get_user_by_id(user_id)
            return user
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def login_user(email: str, password: str):
        try:
            user = UserServices.login_user(email, password)
            if user.is_superuser:
                return sign_jwt(user.id, "super_user")
            return sign_jwt(user.id, "regular_user")
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_username(user_id: str, username: str):
        try:
            user = UserServices.update_username(user_id, username)
            return user
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_user(user_id: str):
        try:
            UserServices.delete_user(user_id)
            return Response(content=f"User with ID: {user_id} deleted.", status_code=200)
        except AppException as e:
            print(str(e))
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_user_with_all_subusers(user_id):
        try:
            subusers = SubuserController.get_all_subusers()
            subusers_for_user = [subuser for subuser in subusers if subuser.user_id == user_id]
            user = UserServices.get_user_by_id(user_id)
            user.subusers = subusers_for_user
            return user
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
