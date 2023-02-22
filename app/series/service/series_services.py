"""Series Service module"""
from datetime import date

from app.config import settings
from app.directors.exceptions.director_exceptions import NonExistingDirectorException
from app.directors.models import Director
from app.directors.repositories import DirectorRepository
from app.genres.exceptions.genre_exceptions import NonExistingGenreException
from app.genres.models import Genre
from app.genres.repositories import GenreRepository
from app.series.models import Series
from app.series.repositories import SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository
from app.db import SessionLocal

PER_PAGE = settings.PER_PAGE


class SeriesServices:
    """Service for Series routes"""
    @staticmethod
    def create_new_series(title: str, year_published: str, director_id: str, genre_id: str):
        """
        Function creates a new series in the database.
        It takes as input a title, year_published, director_id and genre_id.
        The function returns the newly created series.

        Param title:str: Store the title of the series.
        Param year published:str: Store the year that the series was published.
        Param director_id:str: Link the series to a director.
        Param genre_id:str: Identify the genre of the series.
        Return: A series object.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                fields = {"title": title,
                          "date_added": date.today(),
                          "year_published": year_published,
                          "director_id": director_id,
                          "genre_id": genre_id}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def read_all_series(page):
        """
        Function returns all series in the database.

        Param page: Determine, which page of results to return.
        Return: A list of series objects.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                skip = (page - 1) * PER_PAGE
                return repository.read_many(skip=skip, limit=PER_PAGE)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_id(series_id: str):
        """
        Function takes a series_id as an argument and returns the Series object associated with that ID.

        Param series_id:str: Specify the series_id of the series that is to be returned.
        Return: A series object.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                return repository.read_by_id(series_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_director_name(director: str):
        """
        Function takes a director name as an argument and returns all the series that
        the director has directed. If no such director exists, it raises NonExistingDirectorException.

        Param director:str: Get the director object from the database.
        Return: A list of series objects.
        """
        try:
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                obj = director_repo.read_directors_by_last_name(director, search=False)
                if not obj:
                    raise NonExistingDirectorException(message=f"We do not have Director: {director} in our Database.")
                series_repo = SeriesRepository(db, Series)
                return series_repo.read_series_by_director_id(obj.id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_my_series(user_id: str):
        """
        Function returns a set of all the series that the user has watched.
        The function takes in a user_id as an argument and uses it to query the database for all episodes
        that have been watched by this particular user. It then uses these episodes to create a set of
        all series that have been watched by this particular user.

        Param user_id:str: Identify the user.
        Return: A set of all the series titles that a user has watched.
        """
        try:
            with SessionLocal() as db:
                watched_episodes_repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episodes = watched_episodes_repository.read_users_episodes_and_series(user_id)
                my_series = set(obj.title for obj in watched_episodes)
                return my_series
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_year(year: int):
        """
        Function returns a list of series that were published in the given year.
        The function takes one argument, which is an integer representing the year to search for.

        Param year:int: Filter the series by year.
        Return: A list of series that were released in a specific year.
        """
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_year(str(year))
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_episode_id(episode_id: str):
        """
        Function takes an episode_id as a parameter and returns the series that is associated with that episode.

        Param episode_id:str: Identify the series.
        Return: A dictionary.
        """
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                series = repo.read_series_by_episode_id(episode_id)
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_name(series: str, search: bool = True):
        """
        Function takes a series name as an argument and returns the Series object associated with that
        name. If search is set to True, it will return all results for that series name.
        If search is set to False, it will only return the first result.

        Param series:str: Search for a series by name.
        Param search:bool=True: Indicate whether the function should search for a series by name or
        return the series with same name in the database.
        Return: A series object.
        """
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                series = repo.read_series_by_title(series, search=search)
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def get_series_by_genre(genre):
        """
        Function takes a genre name as an argument and returns all the series that belong to that genre.
        If no such genre exists, it raises a NonExistingGenreException.

        Param genre: Search for the genre in our database.
        Return: A list of series that have the genre passed as a parameter.
        """
        try:
            with SessionLocal() as db:
                genre_repo = GenreRepository(db, Genre)
                genre_obj = genre_repo.read_genres_by_name(genre, search=False)
                if not genre_obj:
                    raise NonExistingGenreException(message=f"Genre with name: {genre} does not exist in our Database.")
                series_repo = SeriesRepository(db, Series)
                series = series_repo.read_series_by_genre_id(genre_obj.id)
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def get_latest_features(date_limit: str):
        """
        The get_latest_features function returns a list of the latest series releases.
        The date limit parameter is used to filter out any series that have been
        released after the specified date.

        Param date_limit:str: Limit the date range for which to return the data.
        Return: A list of series objects.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                series = repository.read_latest_releases(date_limit)
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def show_series_never_downloaded():
        """
        Function returns a list of series that have never been downloaded.
        The function takes no arguments and returns a list of dictionaries,
        each dictionary representing one series.

        Return: A list of all the series that have not been downloaded yet.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                series = repository.read_least_popular_series()
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def update_series_data(series_id: str, attributes: dict):
        """
        Function updates a series in the database.

        Param series_id:str: Identify the series to be updated.
        Param attributes:dict: Update the values of a series.
        Return: The updated series object.
        """
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                obj = repo.read_by_id(series_id)
                series = repo.update(obj, attributes)
                return series
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_series(series_id: str):
        """
        Function deletes a series from the database.

        Param series_id:str: Specify, which series to delete.
        Return: The number of rows deleted.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                return repository.delete(series_id)
        except Exception as exc:
            raise exc
