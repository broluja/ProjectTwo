"""Admin Service module"""
from app.db import SessionLocal
from app.users.exceptions import NonExistingUserIdException, AdminAlreadyCreatedException, NonExistingAdminIdException
from app.users.repositories import AdminRepository
from app.users.models import Admin
from app.users.service import UserServices


class AdminServices:
    """Service for Admin routes."""
    @staticmethod
    def create_new_admin(admin: dict):
        """
        The create_new_admin function creates a new admin in the database.
        It takes as input a dictionary containing the user_id of an existing user, and returns an Admin object.

        Param admin:dict: Pass the user_id of the admin that will be created.
        Return: A dictionary.
        """
        try:
            with SessionLocal() as db:
                user = UserServices.get_user_by_id(admin.get("user_id"))
                if not user:
                    raise NonExistingUserIdException(message=f"Non existing User ID: {admin.get('user_id')}", code=400)
                elif user.is_superuser:
                    raise AdminAlreadyCreatedException(message=f"User {user.username} is already Admin.", code=400)
                repository = AdminRepository(db, Admin)
                obj = repository.create(admin)
                UserServices.update_admin_status(admin.get("user_id"))
                return obj
        except Exception as exc:
            raise exc

    @staticmethod
    def derogate_admin(admin_id: str):
        """
        Function is used to remove the admin status from a user.
        It takes in an admin_id as a parameter and returns the updated user object.

        Param admin_id:str: Identify the admin to be derogated.
        Return: The object of the user that has been updated.
        """
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                admin = admin_repository.read_by_id(admin_id)
                if not admin:
                    raise NonExistingAdminIdException
                obj = UserServices.update_admin_status(admin.user_id, superuser=False)
                admin_repository.delete(admin_id)
                return obj
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_admins():
        """
        Function returns all the admins in the database.

        Return: A list of all the admins.
        """
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                return admin_repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_admins_by_country(country: str):
        """
        Function retrieves all the admins in a given country.
        It takes one argument, which is the name of the country to retrieve all admins from.

        Param country:str: Filter the admins by country.
        Return: A list of admin objects.
        """
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                return admin_repository.read_admins_by_country(country)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_admin(admin: dict, user_id: str):
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                obj = admin_repository.read_admin_by_user_id(user_id)
                attributes = {key: value for key, value in admin.items() if value}
                return admin_repository.update(obj, attributes)
        except Exception as exc:
            raise exc
