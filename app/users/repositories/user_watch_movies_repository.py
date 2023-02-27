"""UserWatchMovie Repository module"""
from sqlalchemy.sql.functions import count, func

from app.base import BaseCRUDRepository
from app.config import settings
from app.genres.models import Genre
from app.movies.exceptions import NoRatingsException
from app.movies.models import Movie
from app.users.models.user import UserWatchMovie

PER_PAGE = settings.PER_PAGE


class UserWatchMovieRepository(BaseCRUDRepository):
    """Repository for UserWatchMovie Model"""

    def read_user_watch_movie_by_user_id_and_movie_id(self, user_id: str, movie_id: str):
        """
        Function is used to retrieve a UserWatchMovie object from the database.
        It takes two parameters, user_id and movie_id, which are both strings.
        It then queries the database for a UserWatchMovie object with matching user_id and movie_id values.
        If it finds one, it returns that object; if not, it returns None.

        Param user_id:str: Specify the user_id of a particular user.
        Param movie_id:str: Specify the movie_id of the user watch movie.
        Return: A user-watch-movie object.
        """
        try:
            user_watch_movie = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).filter(
                UserWatchMovie.movie_id == movie_id).first()
            return user_watch_movie
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_from_user(self, user_id: str):
        """
        Function takes a user_id as an argument and returns all the movies that the user has watched.

        Param user_id:str: Filter the user-watch-movie table by user_id
        Return: A list of user-watch-movie objects.
        """
        try:
            user_watch_movies = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).all()
            return user_watch_movies
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movie_downloads(self):
        """
        Function returns a list of tuples containing the movie_id and number of times it has been downloaded.

        Return: A list of tuples.
        """
        try:
            movie_downloads = self.db.query(UserWatchMovie.movie_id, count()).group_by(UserWatchMovie.movie_id)
            return movie_downloads
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_rating(self, best=True):
        """
        Function takes a boolean value (best) and returns the movies with the highest or lowest ratings.
        The function first queries for all movie IDs and their average rating, then groups them by movie ID.
        It then finds either the highest or lowest rated movies depending on the best parameter passed in.

        Param best=True: Specify whether the best or worst movies should be returned.
        Return: A list of tuples with the movie_id and rating.
        """
        try:
            if best:
                subquery = self.db.query(UserWatchMovie.movie_id.label("movie"),
                                         func.avg(UserWatchMovie.rating).label("rating")).group_by(
                    UserWatchMovie.movie_id.label("movie")).subquery()
                max_rating = self.db.query(func.max(subquery.c.rating.label("rating")))
                movie = self.db.query(subquery.c.movie.label("movie"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == max_rating)
            else:
                subquery = self.db.query(UserWatchMovie.movie_id.label("movie"),
                                         func.avg(UserWatchMovie.rating).label("rating")).group_by(
                    UserWatchMovie.movie_id.label("movie")).subquery()
                min_rating = self.db.query(func.min(subquery.c.rating.label("rating")))
                movie = self.db.query(subquery.c.movie.label("movie"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == min_rating)
            return movie
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_users_affinities(self, user_id: str):
        """
        Function takes a user_id as an argument and returns the movie IDs of all movies that
        the user has watched along with their genre ID. This function is used to create the affinity matrix.

        Param user_id:str: Filter the results by user ID.
        Return: A list of tuples.
        """
        try:
            result = self.db.query(UserWatchMovie.movie_id, Genre.id.label("Genre_ID")).\
                join(Movie, UserWatchMovie.movie_id == Movie.id).\
                join(Genre, Movie.genre_id == Genre.id).filter(UserWatchMovie.user_id == user_id).all()
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating(self, movie_id):
        """
        Function takes in a movie_id and returns the average rating of that movie.
        If no ratings are found for the given movie, it raises an exception.

        Param movie_id: Filter the ratings for a particular movie.
        Return: The average rating of a movie.
        """
        try:
            average = self.db.query(func.round(func.avg(UserWatchMovie.rating), 2).label("Average Rating")).\
                filter(UserWatchMovie.movie_id == movie_id).\
                group_by(UserWatchMovie.movie_id).first()
            if not average:
                raise NoRatingsException
            return average
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating_for_all_movies(self):
        """
        Function takes in no parameters. It queries the database for all movies and
        their average ratings, then returns a list of tuples containing the movie title and their average rating.

        Return: The average rating for each movie in the database.
        """
        try:
            average = self.db.query(Movie.title.label("Movie Title"), func.round(func.avg(UserWatchMovie.rating), 2).
                                    label("Average Rating")).join(Movie, UserWatchMovie.movie_id == Movie.id).\
                group_by(Movie.title).all()
            return average
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating_for_movies(self, movie_ids: list):
        """
        Function accepts a list of movie IDs and returns the average rating for each movie.
        The function first queries the database to get all movies with their respective titles,
        then joins UserWatchMovie table to Movie table on ID. It then groups by Movie ID and finds the
        average rating for each movie, returning it as a list of tuples.

        Param movie_ids:list: Pass in a list of movie IDs.
        Return: The average rating for each movie in the list of movie IDs.
        """
        try:
            average = self.db.query(Movie.title.label("Movie Title"), func.round(func.avg(UserWatchMovie.rating), 2).
                                    label("Average Rating")).join(Movie, UserWatchMovie.movie_id == Movie.id).\
                filter(Movie.id.in_(movie_ids)).\
                group_by(Movie.title).all()
            return average
        except Exception as exc:
            self.db.rollback()
            raise exc
