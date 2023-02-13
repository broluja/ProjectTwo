from fastapi import HTTPException

from app.base import AppException
from app.movies.service import MovieServices


class MovieController:

    @staticmethod
    def create_movie(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            movie = MovieServices.create_new_movie(title, year_published, director_id, genre_id)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_movies():
        try:
            movies = MovieServices.get_all_movies()
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movie_by_id(movie_id: str):
        try:
            movie = MovieServices.get_movie_by_id(movie_id)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_movies_by_name(title: str):
        try:
            movies = MovieServices.search_movies_by_name(title)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
