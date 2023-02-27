"""UserWatchMovie Controller module"""
from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.base import AppException
from app.movies.service import MovieServices
from app.users.service import UserWatchMovieServices


class UserWatchMovieController:
    """Controller for User-Watch-Movie routes"""
    @staticmethod
    def user_watch_movie(user_id: str, title: str):
        """
        Function allows a user to watch a movie.

        Param user_id:str: Identify the user.
        Param title:str: Get the movie by its title.
        Return: A watch-movie object.
        """
        try:
            movie = MovieServices.get_movie_by_title(title)
            return UserWatchMovieServices.user_watch_movie(user_id, movie.id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def user_rate_movie(user_id: str, title: str, rating: int):
        """
        The user_rate_movie function allows a user to rate a movie.

        Param user_id:str: Identify the user
        Param title:str: Search for a movie by its title
        Param rating:int: Specify the rating of a movie by a user
        Return: A rated-movie object.
        """
        try:
            movie = MovieServices.get_movie_by_title(title)
            return UserWatchMovieServices.rate_movie(user_id, movie.id, rating)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        """
        Function returns a list of movies that the user has watched.
        It takes in a string representing the user_id and returns a list of movie objects.

        Param user_id:str: Specify the user_id of the user whose watched movies list is to be retrieved.
        Return: A list of movies that the user has watched.
        """
        try:
            movies = UserWatchMovieServices.get_my_watched_movies_list(user_id)
            return movies if movies else JSONResponse(content="You have not watched any movie yet.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_popular_movies():
        """
        Function returns a list of movies that are popular based on the number of times they have been watched.
        The function takes no arguments and returns a list of dictionaries, each dictionary representing one movie.

        Return: A list of popular movies.
        """
        try:
            movies = UserWatchMovieServices.get_popular_movies()
            return movies if movies else JSONResponse(
                content="We have not yet generated movie popularity list.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        """
        Function returns the movie with the highest rating.
        If there are no movies in our database, it will return an error message.

        Param best:bool=True: Specify whether the best or worst rated movie should be returned
        Return: The movie with the highest rating.
        """
        try:
            movie = UserWatchMovieServices.get_best_rated_movie(best)
            return movie if movie else JSONResponse(
                content="We have not yet generated movie popularity list.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_my_recommendations(user_id: str, page: int):
        """
        The get_my_recommendations function retrieves a list of movies that the user has not seen,
        but would like to see. It takes in a user_id and page number than parameters.
        It then queries the database for all movies that have been recommended to
        this particular user, and returns them on the specified page.

        Param user_id:str: Specify the user ID of the user that we want to get recommendations for
        Param page:int: Get the movies in a specific page
        Return: A list of movies.
        """
        try:
            movies = UserWatchMovieServices.get_my_recommendations(user_id, page)
            return movies if movies else MovieServices.get_all_movies(page)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_average_rating_for_movie(name: str):
        """
        The get_average_rating_for_movie function returns the average rating for a movie.
        It takes in a string name and returns an integer representing the average rating of that movie.

        Param name:str: Get the average rating for a movie.
        Return: The average rating for a movie.
        """
        try:
            return UserWatchMovieServices.get_average_rating_for_movie(name)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_average_ratings():
        """
        Function returns the average ratings for all movies in the database.

        Return: The average ratings for all movies in the database.
        """
        try:
            return UserWatchMovieServices.get_average_ratings()
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movies_with_higher_average_rating(rating: float):
        """
        The get_movies_with_higher_average_rating function returns a list of movies with an average
        rating higher than the given rating.

        Param rating:float: Filter the movies with a higher average rating than the given rating.
        Return: A list of movies with a higher average rating than the specified input.
        """
        try:
            movies = UserWatchMovieServices.get_movies_with_higher_average_rating(rating)
            return movies if movies else JSONResponse(
                content=f"No Movie with average rating higher than: {rating}.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_average_movie_rating_for_year(year: int):
        """
        Function returns the average movie rating for a given year.
        It takes in one parameter, year, which is an integer representing the year of interest.
        If no movies from that year exist in our database then it will return a response with status code 200
        and content 'No Movies from Year': 'year'
        Otherwise it will return the average movie rating for all movies released during that particular year.

        Param year:int: Specify the year for which we want to get the average movie rating.
        Return: The average rating for a movie from the given year.
        """
        try:
            average = UserWatchMovieServices.get_average_movie_rating_for_year(year)
            return average if average else JSONResponse(content=f"No Movies from year: {year}.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_most_successful_movie_year():
        """
        The get_most_successful_movie_year function returns the year with the highest average rating.

        Return: The year with the best movie feedbacks.
        """
        try:
            return UserWatchMovieServices.get_most_successful_movie_year()
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
