"""Movie Repository module"""
from app.base import BaseCRUDRepository
from app.movies.models import Movie
from app.movies.exceptions import NonExistingMovieTitleException, NoMovieFromYearException, NoLatestReleasesException
from app.users.models.user import UserWatchMovie
from app.config import settings

PER_PAGE = settings.PER_PAGE


class MovieRepository(BaseCRUDRepository):
    """Repository for Movie Model"""

    def read_movie_by_title(self, title: str, search=False):
        """
        Function takes a title as an argument and returns the movie object with that title.
        If no such movie exists, it raises NonExistingMovieTitleException.

        Param title:str: Get the movie title from the database.
        Param search=False: Determine if the movie title is being searched for or not.
        Return: A movie object.
        """
        try:
            if search:
                movie = self.db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
            else:
                movie = self.db.query(Movie).filter(Movie.title == title.title()).first()
            if not movie:
                self.db.rollback()
                raise NonExistingMovieTitleException
            return movie
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_director_id(self, director_id: str):
        try:
            return self.db.query(Movie).filter(Movie.director_id == director_id).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_director_ids(self, director_ids: list):
        try:
            return self.db.query(Movie).filter(Movie.director_id.in_(director_ids)).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_latest_releases(self, date_limit: str):
        """
        Function returns a list of all movies added to the database after the date-limit.
        The date-limit is passed in as an argument and must be in YYYY-MM-DD format.

        Param date limit:str: Limit the query to only those movies that were added after the date-limit.
        Return: A list of movie objects.
        """
        try:
            movies = self.db.query(Movie).filter(Movie.date_added >= date_limit).all()
            if not movies:
                raise NoLatestReleasesException
            return movies
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_unpopular_movies(self):
        """
        Function returns a list of movies that have been watched by fewer than five users.

        Return: A list of tuples with the movie title and ID that have not been watched by any user.
        """
        try:
            sub = self.db.query(UserWatchMovie.movie_id.label('movie')).subquery('sub')
            return self.db.query(Movie.title.label("Movie"), Movie.id.label('ID')).filter(Movie.id.not_in(sub)).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_group_of_genres(self, page: int, genres: list):
        """
        Function takes a page number and a list of genres as arguments.
        It queries the database for all movies that have one of the genres in the list,
        then returns them in a paginated format.

        Param page:int: Skip the movies that are not in the current page.
        Param genres:list: Filter the movies by a genre.
        Return: A list of movie objects.
        """
        try:
            skip = (page - 1) * PER_PAGE
            return self.db.query(Movie).filter(Movie.genre_id.in_(genres)).offset(skip).limit(PER_PAGE).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movies_by_year(self, year: str):
        """
        Function accepts a year as input and returns all movies that were published in that year.

        Param year:str: Filter the movies by a year.
        Return: A list of movie objects.
        """
        try:
            movies = self.db.query(Movie).filter(Movie.year_published == year).all()
            if not movies:
                raise NoMovieFromYearException
            return movies
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_movie_years(self):
        """
        Function returns a list of all the years in which movies were published.

        Return: A list of tuples containing the years in which movies were published.
        """
        try:
            return self.db.query(Movie.year_published).distinct().all()
        except Exception as exc:
            self.db.rollback()
            raise exc
