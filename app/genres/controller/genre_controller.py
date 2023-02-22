"""Genre Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.genres.service import GenreServices
from app.base.base_exception import AppException


class GenreController:
    """Controller for Genre routes"""
    @staticmethod
    def create_director(name: str):
        """
        Function creates a new director in the database.
        It takes one argument, name, which is the name of the director to be created.
        The function returns a dictionary containing information about that newly created genre.

        Param name:str: Specify the name of the director.
        Return: The genre that was created.
        """
        try:
            genre = GenreServices.create_new_genre(name)
            return genre
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_genres():
        """
        Function returns a list of all genres in the database.
        If there are no genres, it returns an empty list.

        Return: A list of all genres in the database.
        """
        try:
            genres = GenreServices.get_all_genres()
            if not genres:
                return Response(content="No Genres in our Database yet.", status_code=200)
            return genres
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_genre_by_id(genre_id: str):
        """
        Function is used to retrieve a genre by its ID.
        It takes in the genre_id as an argument and returns the Genre object with that ID.

        Param genre_id:str: Identify the genre to be retrieved.
        Return: A genre object.
        """
        try:
            genre = GenreServices.get_genre_by_id(genre_id)
            return genre
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_genres_by_name(name: str):
        """
        Function searches for a genre by name and returns the genre if it exists.
        If no genres are found, it returns an error message.

        Param name:str: Search for a genre by name.
        Return: A list of genre objects that match the name provided.
        """
        try:
            genres = GenreServices.search_genres_by_name(name)
            if not genres:
                return Response(content=f"No Genre: {name} in our Database.", status_code=200)
            return genres
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_genre(genre_id: str, name: str):
        """
        Function updates the name of a genre.

        Param genre_id:str: Identify the genre to be updated
        Param name:str: Update the name of a genre
        Return: The updated genre object.
        """
        try:
            director = GenreServices.update_genre_name(genre_id, name)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
