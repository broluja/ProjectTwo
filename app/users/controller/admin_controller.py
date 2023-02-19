from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.users.service import AdminServices


class AdminController:

    @staticmethod
    def create_new_admin(admin: dict):
        try:
            obj = AdminServices.create_new_admin(admin)
            return obj
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500)

    @staticmethod
    def derogate_admin(admin_id: str):
        try:
            obj = AdminServices.derogate_admin(admin_id)
            return obj
        except Exception as e:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500)

    @staticmethod
    def get_all_admins():
        try:
            admins = AdminServices.get_all_admins()
            return admins
        except Exception as e:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500)

    @staticmethod
    def get_all_admins_by_country(country: str):
        try:
            admins = AdminServices.get_all_admins_by_country(country)
            if not admins:
                return Response(content=f"No admins from country: {country}.", status_code=200)
            return admins
        except Exception as e:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500)
