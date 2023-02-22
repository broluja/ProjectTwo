"""Subuser Service module"""
from app.config import settings
from app.users.repositories import SubuserRepository
from app.users.service import UserServices
from app.db.database import SessionLocal
from app.users.models import Subuser
from app.users.exceptions import NonExistingUserIdException, MaxLimitSubusersException, AdminSubuserException, \
    UnknownProfileException

MAX_NUMBER_SUBUSERS = settings.MAX_NUMBER_SUBUSERS


class SubuserServices:
    """Service for Subusers routes"""
    @staticmethod
    def create_new_subuser(user_id, name):
        """
        The create_new_subuser function creates a new subuser for the user with the given ID.
        It returns the newly created subuser object.

        Param user_id: Identify the user who is creating a new subuser.
        Param name: Identify the subuser.
        Return: The subuser created.
        """
        try:
            with SessionLocal() as db:
                user = UserServices.get_user_by_id(user_id)
                if not user:
                    raise NonExistingUserIdException(message=f"Non existing User ID: {user_id}", code=400)
                elif user.is_superuser:
                    raise AdminSubuserException
                subusers = SubuserServices.get_all_subusers_for_one_user(user_id)
                if len(subusers) >= MAX_NUMBER_SUBUSERS:
                    raise MaxLimitSubusersException(message="You have reached Subusers Limit.", code=400)
                repository = SubuserRepository(db, Subuser)
                fields = {"user_id": user_id, "name": name}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_subusers():
        """
        The get_all_subusers function returns all subusers in the database.

        Return: A list of all the subusers in the database.
        """
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_subuser_by_id(subuser_id: str):
        """
        The get_subuser_by_id function is used to retrieve a subuser by their ID.
        It takes in the subuser_id as an argument and returns the corresponding Subuser object.

        Param subuser_id:str: Identify the subuser.
        Return: A subuser object.
        """
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                return repository.read_by_id(subuser_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_subusers_for_one_user(user_id):
        """
        The get_all_subusers_for_one_user function retrieves all subusers for a given user.
        It takes in the user_id as an argument and returns a list of subusers.

        Param user_id: Get all subusers for a specific user.
        Return: A list of subusers for a given user.
        """
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subusers = repository.read_subusers_by_user_id(user_id)
                return subusers
        except Exception as exc:
            raise exc

    @staticmethod
    def update_subusers_name(subuser_id: str, name: str):
        """
        The update_subusers_name function updates the name of a subuser.

        Param subuser_id:str: Identify the subuser that is to be updated.
        Param name:str: Update the name of the subuser.
        Return: The updated subuser object.
        """
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subuser = repository.read_by_id(subuser_id)
                updates = {"name": name}
                obj = repository.update(subuser, updates)
                return obj
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_subuser(user_id: str, subuser_name: str):
        """
        Function will delete a subuser from the database.

        Param user_id:str: Identify the user that owns the subuser
        Param subuser_name:str: Specify the name of the subuser to be deleted
        Return: The response from the delete method.
        """
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subuser = repository.read_subusers_by_name(subuser_name, user_id)
                if not subuser:
                    raise UnknownProfileException
                response = repository.delete(subuser.id)
                return response
        except Exception as exc:
            raise exc
        