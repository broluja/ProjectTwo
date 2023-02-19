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
    def get_all_movies(page: int):
        try:
            movies = MovieServices.get_all_movies(page)
            if not movies:
                return Response(content=f"End of query.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movie_data(title: str):
        try:
            movie = MovieServices.get_movie_by_title(title)
            genre = GenreServices.get_genre_by_id(movie.genre_id)
            director = DirectorServices.get_director_by_id(movie.director_id)
            movie.genre = genre
            movie.director = director
            return movie
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
            if not movies:
                return Response(content=f"No Movie with title: {title} in our Database.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_movies_by_director(director: str):
        try:
            movies = MovieServices.search_movies_by_director(director)
            if not movies:
                return Response(content=f"No Movie from Director: {director} in our Database.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_movies_by_genre(genre: str):
        try:
            movies = MovieServices.search_movies_by_genre(genre)
            if not movies:
                return Response(content=f"No Movie with genre: {genre} in our Database.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_latest_features(date_limit: str):
        try:
            movie = MovieServices.get_latest_features(date_limit)
            if not movie:
                return Response(content="No movies in latest list.", status_code=200)
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
            if not movies:
                return Response(content="There are no movies that never have been downloaded.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
