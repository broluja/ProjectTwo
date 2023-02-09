from fastapi import HTTPException

from app.base import AppException
from app.movies.controller import MovieController
from app.movies.service import MovieActorService


class MovieActorController:

    @staticmethod
    def create_movie_actor(movie_id: str, actor_id: str, rating: int = None):
        try:
            movie_actor = MovieActorService.create_new_movie_actor(movie_id, actor_id, rating)
            return movie_actor
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movie_with_actors(movie_id: str):
        try:
            movie = MovieController.get_movie_by_id(movie_id)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))