"""Admin Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.users.service import AdminServices


class AdminController:
    """Controller for Admin routes"""
    @staticmethod
    def create_new_admin(admin: dict):
        """
        The create_new_admin function creates a new admin in the database.
        It takes an admin dictionary as input and returns an Admin object.

        Param admin:dict: Pass in the admin details.
        Return: The newly created admin object.
        """
        try:
            obj = AdminServices.create_new_admin(admin)
            return obj
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500) from exc

    @staticmethod
    def derogate_admin(admin_id: str):
        """
        Function is used to remove admin privileges from a user.
        It takes in an admin_id as a string and returns the updated Admin object.

        Param admin_id:str: Pass the ID of the admin that is to be derogated
        Return: The object that is created when the admin is derogated.
        """
        try:
            obj = AdminServices.derogate_admin(admin_id)
            return obj
        except Exception as exc:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500) from exc

    @staticmethod
    def get_all_admins():
        """
        Function returns a list of all the admins in the database.

        Return: A list of all the admins in the database.
        """
        try:
            admins = AdminServices.get_all_admins()
            return admins
        except Exception as exc:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500) from exc

    @staticmethod
    def get_all_admins_by_country(country: str):
        """
        Function returns a list of all the admins from a specified country.
        The function takes in one parameter, which is the name of the country as a string.
        If no admins are found for that country, then an empty list is returned.

        Param country:str: Filter the admins by country
        Return: A list of all the admins from a specific country.
        """
        try:
            admins = AdminServices.get_all_admins_by_country(country)
            if not admins:
                return Response(content=f"No admins from country: {country}.", status_code=200)
            return admins
        except Exception as exc:
            raise HTTPException(detail="Unknown Error occurred. Please try again later.", status_code=500) from exc
