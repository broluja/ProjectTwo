from fastapi import HTTPException, Response

from app.users.service import UserServices
from .subuser_controller import SubuserController
from app.base.base_exception import AppException


class UserController:

    @staticmethod
    def create_user(email, password, username):
        try:
            user = UserServices.create_new_user(email, password, username)
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
    def get_user_by_email_and_password(email: str, password: str):
        try:
            user = UserServices.get_user_by_email_and_password(email, password)
            return user
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
