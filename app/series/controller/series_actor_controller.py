"""Series-Actor Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.controller import SeriesController
from app.series.service import SeriesActorService
from app.directors.service import DirectorServices
from app.genres.service import GenreServices


class SeriesActorController:
    """Controller for Series-Actor routes"""
    @staticmethod
    def create_series_actor(series_id: str, actor_id: str):
        """
        The create_series_actor function creates a new SeriesActor object in the database.
        It takes two parameters, series_id and actor_id, which are used to create the SeriesActor object.
        The function returns a SeriesActor object.

        Param series_id:str: Specify the series that the actor is to be added to
        Param actor_id:str: Specify the actor that will be added to the series
        Return: A series-actor object.
        """
        try:
            series_actor = SeriesActorService.create_new_series_actor(series_id, actor_id)
            return series_actor
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_with_actors(series_id: str):
        """
        Function is used to retrieve a series with actors.
        It takes in a series ID and returns the series object with all of its attributes,
        including the list of actors that are associated with it.

        Param series_id:str: Specify, which series to get the actors for.
        Return: A series with actors.
        """
        try:
            series = SeriesController.get_series_by_id(series_id)
            return series
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_with_director_and_genre(series_id: str):
        """
        Function takes a series ID as an argument and returns the series object with
        the director and genre objects attached to it. It does this by calling the get_series_by_id function
        from SeriesController and then calls the get_director_by_id function from DirectorServices, which returns
        a director object. The same is done for the genre, except using GenreServices instead of DirectorServices.

        Param series_id:str: Specify the ID of the series that is to be returned.
        Return: A series with the director and genre attributes.
        """
        try:
            series = SeriesController.get_series_by_id(series_id)
            director = DirectorServices.get_director_by_id(series.director_id)
            genre = GenreServices.get_genre_by_id(series.genre_id)
            series.director = director
            series.genre = genre
            return series
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_series_actor(series_id: str, actor_id: str):
        """
        Function is used to remove an actor from a series.
        It takes in two parameters, the first being the ID of the series, and the second being
        the ID of an actor. It then removes that actor from that particular series.

        Param series_id:str: Specify the series that the actor is to be removed from
        Param actor_id:str: Identify the actor to be removed from the series
        Return: A response object with a message and status code.
        """
        try:
            SeriesActorService.remove_series_actor(series_id, actor_id)
            return Response(content=f"Actor removed from series.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
