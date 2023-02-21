from app.base import BaseCRUDRepository
from app.movies.models import Movie
from app.movies.exceptions import NonExistingMovieTitleException
from app.users.models.user import UserWatchMovie
from app.config import settings

PER_PAGE = settings.PER_PAGE


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

    def read_unpopular_movies(self):
        try:
            sub = self.db.query(UserWatchMovie.movie_id.label('movie')).subquery('sub')
            result = self.db.query(Movie.title.label("Movie"), Movie.id.label('ID')).filter(Movie.id.not_in(sub)).all()
            return result
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movies_by_group_of_genres(self, page: int, genres: list):
        try:
            skip = (page - 1) * PER_PAGE
            movies = self.db.query(Movie).filter(Movie.genre_id.in_(genres)).offset(skip).limit(PER_PAGE).all()
            return movies
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movies_by_year(self, year: str):
        try:
            result = self.db.query(Movie).filter(Movie.year_published == year).all()
            return result
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movie_years(self):
        try:
            years = self.db.query(Movie.year_published).distinct().all()
            return years
        except Exception as e:
            self.db.rollback()
            raise e
