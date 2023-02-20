from fastapi import HTTPException
from starlette.responses import Response

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
            rated_movie = UserWatchMovieServices.rate_movie(user_id, movie.id, rating)
            return rated_movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        try:
            movies = UserWatchMovieServices.get_my_watched_movies_list(user_id)
            if not movies:
                return Response(content="You have not watched any movie yet.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_popular_movies():
        try:
            movies = UserWatchMovieServices.get_popular_movies()
            if not movies:
                return Response(content="We have not yet generated movie popularity list.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        try:
            movie = UserWatchMovieServices.get_best_rated_movie(best)
            if not movie:
                return Response(content="We have not yet generated movie popularity list.", status_code=200)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_recommendations(user_id: str, page: int):
        try:
            movies = UserWatchMovieServices.get_my_recommendations(user_id, page)
            if not movies:
                return MovieServices.get_all_movies(page)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_average_rating_for_movie(name: str):
        try:
            movie = UserWatchMovieServices.get_average_rating_for_movie(name)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_average_ratings():
        try:
            response = UserWatchMovieServices.get_average_ratings()
            return response
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movies_with_higher_average_rating(rating: float):
        try:
            movies = UserWatchMovieServices.get_movies_with_higher_average_rating(rating)
            if not movies:
                return Response(content=f"No Movie with average rating higher than: {rating}.", status_code=200)
            return movies
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_average_movie_rating_for_year(year: int):
        try:
            average = UserWatchMovieServices.get_average_movie_rating_for_year(year)
            if not average:
                return Response(content=f"No Movies from year: {year}.", status_code=200)
            return average
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

