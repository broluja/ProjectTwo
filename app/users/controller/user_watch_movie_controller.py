from fastapi import HTTPException

from app.base import AppException
from app.movies.service import MovieServices
from app.users.service import UserWatchMovieServices


class UserWatchMovieController:

    @staticmethod
    def user_watch_movie(user_id: str, title: str):
        try:
            movie = MovieServices.get_movie_by_title(title)
            watch_movie = UserWatchMovieServices.user_watch_movie(user_id, movie.id)
            return watch_movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def user_rate_movie(user_id: str, title: str, rating: int):
        try:
            movie = MovieServices.get_movie_by_title(title)
            rate_movie = UserWatchMovieServices.rate_movie(user_id, movie.id, rating)
            return rate_movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        try:
            movies = UserWatchMovieServices.get_my_watched_movies_list(user_id)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_popular_movies():
        try:
            movies = UserWatchMovieServices.get_popular_movies()
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        try:
            movie = UserWatchMovieServices.get_best_rated_movie(best)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
