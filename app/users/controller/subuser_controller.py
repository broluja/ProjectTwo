"""Subuser Controller module"""
from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.users.service import SubuserServices
from app.base.base_exception import AppException


class SubuserController:
    """Controller for Subuser routes"""
    @staticmethod
    def create_subuser(user_id, name):
        """
        Function creates a new subuser for the user with the given ID.
        It returns the newly created subuser.

        Param user_id: Identify the user who is creating a new subuser
        Param name: Set the name of the subuser
        Return: A subuser object.
        """
        try:
            return SubuserServices.create_new_subuser(user_id, name)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_subusers():
        """
        Function returns all the subusers in our database.
        It takes no parameters and returns a list of dictionaries, each dictionary representing a single subuser.

        Return: A list of all the subusers in our database.
        """
        try:
            subusers = SubuserServices.get_all_subusers()
            return subusers if subusers else JSONResponse(
                content="There are no Subusers created in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_subuser_by_id(subuser_id: str):
        """
        Function is used to retrieve a subuser by their ID.
        It takes in the subuser_id as an argument and returns the corresponding Subuser object.

        Param subuser_id:str: Identify the subuser that is to be returned.
        Return: The subuser with the given ID.
        """
        try:
            return SubuserServices.get_subuser_by_id(subuser_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))from exc

    @staticmethod
    def get_subusers_by_user_id(user_id: str):
        """
        Function is used to retrieve all subusers created by a specific user.
        It takes in the user_id of the user who created the subusers and returns a list of dictionaries,
        each dictionary representing one subuser.
        The function raises an HTTPException if there are no users with that ID or if there is another error.

        Param user_id:str: Get all the subusers created by a user with that ID.
        Return: A list of subusers made by a specific user.
        """
        try:
            return SubuserServices.get_all_subusers_for_one_user(user_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_subusers_name(subuser_id: str, name: str):
        """
        The update_subusers_name function updates the name of a subuser.

        Param subuser_id:str: Identify the subuser to be updated.
        Param name:str: Update the name of a subuser.
        Return: A subuser object.
        """
        try:
            return SubuserServices.update_subusers_name(subuser_id, name)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_subuser(user_id, subuser_name: str):
        """
        Function deletes a subuser from the database.

        Param user_id: Identify the user who owns the subuser.
        Param subuser_name:str: Specify the subuser to be deleted.
        Return: A response object.
        """
        try:
            SubuserServices.delete_subuser(user_id, subuser_name)
            return JSONResponse(content=f"Subuser: {subuser_name} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
