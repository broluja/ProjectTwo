"""Director Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.directors.service import DirectorServices
from app.base.base_exception import AppException


class DirectorController:
    """Controller for Director routes"""
    @staticmethod
    def create_director(first_name: str, last_name: str, country: str):
        """
        Function creates a new director in the database.
        It takes three parameters: first_name, last_name and country.
        The function returns a Director object.

        Param first_name:str: Specify the first name of the director.
        Param last_name:str: Specify the last name of the director.
        Param country:str: Specify the country of the director.
        Return: The new director object created by the director services.
        """
        try:
            director = DirectorServices.create_new_director(first_name, last_name, country)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_directors():
        """
        Function returns all directors in our Database.
        It takes no parameters and returns a list of dictionaries, each dictionary representing a director.

        Return: A list of all directors in our database.
        """
        try:
            directors = DirectorServices.get_all_directors()
            if not directors:
                return Response("No directors in our Database yet.", status_code=200)
            return directors
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_director_by_id(director_id: str):
        """
        Function is used to retrieve a director by their ID.
        It takes in the parameter of the director_id and returns a dictionary
        with all of that directors' information.

        Param director_id:str: Pass the ID of the director that we want to retrieve.
        Return: A director object based on the ID passed in.
        """
        try:
            director = DirectorServices.get_director_by_id(director_id)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        """
        Function searches for a Director by last name in the database.
        It returns a list of Directors with that last name, or an
        empty list if no Director is found.

        Param last_name:str: Search for a director with the given last name
        Return: A list of director objects.
        """
        try:
            director = DirectorServices.search_directors_by_last_name(last_name)
            if not director:
                return Response(content=f"No Director with last name: {last_name} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_first_name(first_name: str):
        """
        Function searches for a Director in the database by first name.
        It returns a list of Directors that match the search criteria.
        If no Director is found, it returns an empty list.

        Param first_name:str: Pass the first name of the director that is being searched for.
        Return: A list of directors with the first name specified.
        """
        try:
            director = DirectorServices.search_directors_by_first_name(first_name)
            if not director:
                return Response(content=f"No Director with first name: {first_name} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_country(country: str):
        """
        Function searches for a director by country.
        It takes in a string representing the country and returns all
        directors with that country as their nationality.

        Param country:str: Search for directors by country.
        Return: A list of directors that have the country name in their description.
        """
        try:
            director = DirectorServices.search_directors_by_country(country)
            if not director:
                return Response(content=f"No Director with first name: {country} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_director(director_id: str, attributes: dict):
        """
        Function updates a director's information.

        Param director_id:str: Identify the director to be updated.
        Param attributes:dict: Update the director's attributes.
        Return: A dictionary of the updated director.
        """
        try:
            director = DirectorServices.update_director(director_id, attributes)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_director(director_id: str):
        """
        Function deletes a director from the database.
        It takes in a string representing the ID of the director to be deleted,
        and returns an HTTP response with either
        a 200 status code if successful or 500 if unsuccessful.

        Param director_id:str: Identify the director to be deleted
        Return: A response object with the content of the response, and a status code of 200.
        """
        try:
            DirectorServices.delete_director(director_id)
            return Response(content=f"Director with ID: {director_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
