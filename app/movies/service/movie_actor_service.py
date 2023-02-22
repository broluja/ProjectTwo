"""Movie-Actor service module"""
from app.db import SessionLocal
from app.movies.models import MovieActor
from app.movies.repositories import MovieActorRepository


class MovieActorService:
    """Service for Movie-Actor routes"""
    @staticmethod
    def create_new_movie_actor(movie_id: str, actor_id: str):
        """
        Function creates a new movie actor relationship.
        It takes in two parameters, movie_id and actor_id, which are both strings.
        The function returns the newly created MovieActor object.

        Param movie_id:str: Specify the movie_id of the movie that is going to be added to a specific actor.
        Param actor_id:str: Identify the actor that is being added to the movie.
        Return: A movie-actor object.
        """
        try:
            with SessionLocal() as db:
                repository = MovieActorRepository(db, MovieActor)
                fields = {"movie_id": movie_id,
                          "actor_id": actor_id}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def remove_movie_actor(movie_id: str, actor_id: str):
        """
        The remove_movie_actor function removes an actor from a movie.

        Param movie_id:str: Identify the movie that should be removed from the actor's list of movies
        Param actor_id:str: Identify the actor that will be removed from the movie
        Return: A boolean value.
        """
        try:
            with SessionLocal() as db:
                repository = MovieActorRepository(db, MovieActor)
                return repository.delete_by_movie_id_and_actor_id(movie_id, actor_id)
        except Exception as exc:
            raise exc
