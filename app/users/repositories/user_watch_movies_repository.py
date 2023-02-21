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
        try:
            user_watch_movie = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).filter(
                UserWatchMovie.movie_id == movie_id).first()
            return user_watch_movie
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_from_user(self, user_id: str):
        try:
            user_watch_movies = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).all()
            return user_watch_movies
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movie_downloads(self):
        try:
            movie_downloads = self.db.query(UserWatchMovie.movie_id, count()).group_by(UserWatchMovie.movie_id)
            return movie_downloads
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_rating(self, best=True):
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
        try:
            result = self.db.query(UserWatchMovie.movie_id, Genre.id.label("Genre_ID")).\
                join(Movie, UserWatchMovie.movie_id == Movie.id).\
                join(Genre, Movie.genre_id == Genre.id).filter(UserWatchMovie.user_id == user_id).all()
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating(self, movie_id):
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
        try:
            average = self.db.query(Movie.title.label("Movie Title"), func.round(func.avg(UserWatchMovie.rating), 2).
                                    label("Average Rating")).join(Movie, UserWatchMovie.movie_id == Movie.id).\
                group_by(UserWatchMovie.movie_id).all()
            return average
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating_for_movies(self, movie_ids: list):
        try:
            average = self.db.query(Movie.title.label("Movie Title"), func.round(func.avg(UserWatchMovie.rating), 2).
                                    label("Average Rating")).join(Movie, UserWatchMovie.movie_id == Movie.id).\
                filter(Movie.id.in_(movie_ids)).\
                group_by(UserWatchMovie.movie_id).all()
            return average
        except Exception as exc:
            self.db.rollback()
            raise exc
