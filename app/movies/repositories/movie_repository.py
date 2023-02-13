from sqlalchemy import distinct

from app.base import BaseCRUDRepository
from app.movies.models import Movie
from app.movies.exceptions import NonExistingMovieTitleException
from app.users.models.user import UserWatchMovie


class MovieRepository(BaseCRUDRepository):
    """Repository for Movie Model"""

    def read_movie_by_title(self, title: str, search=False):
        try:
            if search:
                movie = self.db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
            else:
                movie = self.db.query(Movie).filter(Movie.title == title).first()
            if not movie:
                self.db.rollback()
                raise NonExistingMovieTitleException
            return movie
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movies_from_specific_year(self, year: str):
        try:
            movies = self.db.query(Movie).filter(Movie.year == year).all()
            return movies
        except Exception as e:
            self.db.rollback()
            raise e

    def read_latest_releases(self, date_limit: str):
        try:
            movies = self.db.query(Movie).filter(Movie.date_added >= date_limit).all()
            return movies
        except Exception as e:
            self.db.rollback()
            raise e

    def read_least_popular_movies(self):
        try:
            subquery = self.db.query(UserWatchMovie.movie_id).distinct().all()
            ids = [obj.movie_id for obj in subquery]
            result = self.db.query(Movie).filter(Movie.id.not_in(ids)).all()
            return result
        except Exception as e:
            self.db.rollback()
            raise e
