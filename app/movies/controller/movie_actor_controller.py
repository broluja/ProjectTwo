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
        try:
            movie_actor = MovieActorService.create_new_movie_actor(movie_id, actor_id)
            return movie_actor
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_with_actors(movie_id: str):
        try:
            movie = MovieController.get_movie_by_id(movie_id)
            return movie
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_with_director_and_genre(movie_id: str):
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
        try:
            MovieActorService.remove_movie_actor(movie_id, actor_id)
            return Response(content=f"Actor removed from movie.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
