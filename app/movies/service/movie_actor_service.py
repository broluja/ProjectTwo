"""Movie-Actor service module"""
from app.db import SessionLocal
from app.movies.models import MovieActor
from app.movies.repositories import MovieActorRepository


class MovieActorService:
    """Service for Movie-Actor routes"""
    @staticmethod
    def create_new_movie_actor(movie_id: str, actor_id: str):
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
        try:
            with SessionLocal() as db:
                repository = MovieActorRepository(db, MovieActor)
                return repository.delete_by_movie_id_and_actor_id(movie_id, actor_id)
        except Exception as exc:
            raise exc
