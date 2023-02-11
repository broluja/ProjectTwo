from fastapi import HTTPException
from starlette.responses import Response

from app.users.service import SubuserServices
from app.base.base_exception import AppException


class SubuserController:

    @staticmethod
    def create_subuser(user_id, name):
        try:
            subuser = SubuserServices.create_new_subuser(user_id, name)
            return subuser
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_subusers():
        try:
            subusers = SubuserServices.get_all_subusers()
            return subusers
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_subuser_by_id(subuser_id: str):
        try:
            subuser = SubuserServices.get_subuser_by_id(subuser_id)
            return subuser
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_subusers_by_user_id(user_id: str):
        try:
            subusers = SubuserServices.get_all_subusers_for_one_user(user_id)
            return subusers
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_subusers_name(subuser_id: str, name: str):
        try:
            subuser = SubuserServices.update_subusers_name(subuser_id, name)
            return subuser
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_subuser(user_id, subuser_name: str):
        try:
            SubuserServices.delete_subuser(user_id, subuser_name)
            return Response(content=f"Subuser: {subuser_name} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
