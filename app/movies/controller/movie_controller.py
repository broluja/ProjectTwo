from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.movies.service import MovieServices
from app.directors.service import DirectorServices
from app.genres.service import GenreServices


class MovieController:

    @staticmethod
    def create_movie(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            director = DirectorServices.get_director_by_id(director_id)
            genre = GenreServices.get_genre_by_id(genre_id)
            movie = MovieServices.create_new_movie(title, year_published, director_id, genre_id)
            movie.director = director
            movie.genre = genre
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

    @staticmethod
    def search_movies_by_director(director: str):
        try:
            movies = MovieServices.search_movies_by_director(director)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_movies_by_genre(genre: str):
        try:
            movies = MovieServices.search_movies_by_genre(genre)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_latest_features(date_limit: str):
        try:
            movie = MovieServices.get_latest_features(date_limit)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_movie_data(movie_id: str, attributes: dict):
        try:
            movie = MovieServices.update_movie_data(movie_id, attributes)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_movie(movie_id: str):
        try:
            MovieServices.delete_movie(movie_id)
            return Response(content=f"Movie with ID: {movie_id} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def show_least_popular_movies():
        try:
            movies = MovieServices.show_least_popular_movies()
            print(movies)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
