"""Subuser Repository module"""
from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository, AppException
from app.users.models import Subuser


class SubuserRepository(BaseCRUDRepository):
    """Repository for Subuser Model"""
    def create(self, attributes: dict):
        """
        The create function creates a new subuser in the database.
        It takes a dictionary of attributes and uses them to create a new Subuser object.
        The function then tries to commit the changes, and if it succeeds, returns the created object.
        If there is an integrity error (most likely because of duplicate subusers), it rolls back any
        changes made so far and raises an exception.

        Param attributes:dict: Pass in the parameters that are being passed into the create function.
        Return: The created object.
        """
        try:
            return super().create(attributes)
        except IntegrityError as exc:
            self.db.rollback()
            raise AppException(message="Subuser Name already taken", code=400) from exc

    def read_subusers_by_name(self, name: str, user_id: str):
        """
        The read_subusers_by_name function is used to retrieve a subuser object from the database.
        It takes in two parameters, name and user_id. The function then queries the database for a
        subuser with that name and user_id combination.
        If it finds one, it returns that object.

        Param name:str: Specify the name of the subuser.
        Param user_id:str: Filter the query by user_id.
        Return: The subuser object that has the name passed in as a parameter.
        """
        try:
            subuser = self.db.query(Subuser).filter(Subuser.name == name).filter(Subuser.user_id == user_id).first()
            return subuser
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc

    def read_subusers_by_user_id(self, user_id: str):
        """
        The read_subusers_by_user_id function is used to retrieve all subusers associated with a user.
        It takes in the user_id as an argument and returns a list of Subuser objects.

        Param user_id:str: Filter the query by user_id.
        Return: A list of subuser objects.
        """
        try:
            subuser = self.db.query(Subuser).filter(Subuser.user_id == user_id).all()
            return subuser
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc
