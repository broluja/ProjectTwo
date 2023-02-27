"""Movie-Actor Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.movies.controller import MovieController
from app.movies.service import MovieActorService
from app.directors.service import DirectorServices
from app.genres.service import GenreServices


class MovieActorController:
    """Controller for Movie-Actor routes"""
    @staticmethod
    def create_movie_actor(movie_id: str, actor_id: str):
        """
        Function creates a new movie actor record in the database.
        It takes two parameters, movie_id and actor_id, which are used to create the record.
        The function returns a MovieActor object.

        Param movie_id:str: Specify the movie that an actor is being added to
        Param actor_id:str: Identify the actor that will be linked to the movie
        Return: A movie-actor object.
        """
        try:
            return MovieActorService.create_new_movie_actor(movie_id, actor_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_with_actors(movie_id: str):
        """
        Function is used to retrieve a movie with its actors.
        It takes in the ID of the movie as an argument and returns a dictionary containing all
        information about that specific movie.

        Param movie_id:str: Specify the movie_id of the movie that will be retrieved.
        Return: A movie with actors.
        """
        try:
            return MovieController.get_movie_by_id(movie_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_with_director_and_genre(movie_id: str):
        """
        Function is used to get a movie with its director and genre.
        It takes in the ID of the movie as an argument, and returns a
        Movie object with its director and genre attributes set.

        Param movie_id:str: Pass the movie_id as a string to the get_movie_by_id function.
        Return: A movie object with the director and genre attributes set.
        """
        try:
            movie = MovieController.get_movie_by_id(movie_id)
            director = DirectorServices.get_director_by_id(movie.director_id)
            genre = GenreServices.get_genre_by_id(movie.genre_id)
            movie.director = director
            movie.genre = genre
            return movie
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_movie_actor(movie_id, actor_id):
        """
        The delete_movie_actor function removes an actor from a movie.

        Param movie_id: Identify the movie that will have an actor removed from it
        Param actor_id: Identify the actor that will be removed from the movie.
        Return: A response object with a message, and a status code.
        """
        try:
            MovieActorService.remove_movie_actor(movie_id, actor_id)
            return Response(content="Actor removed from movie.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
