"""Series Repository module"""
from sqlalchemy import distinct

from app.base import BaseCRUDRepository
from app.config import settings
from app.series.exceptions.series_exceptions import UnknownSeriesTitleException
from app.series.models import Series, Episode
from app.users.models.user import UserWatchEpisode

PER_PAGE = settings.PER_PAGE


class SeriesRepository(BaseCRUDRepository):
    """Repository for Series Model"""

    def read_series_by_genre_id(self, genre_id: str):
        """
        Function takes a genre_id as an argument and returns all the series in that genre.

        Param genre_id:str: Filter the series by genre_id
        Return: A list of series objects that match the genre_id passed to it.
        """
        try:
            return self.db.query(Series).filter(Series.genre_id == genre_id).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_director_id(self, director_id: str):
        """
        Function takes a director_id as an argument and returns all the series that have
        the same director_id. It does this by querying the database for all
        rows in Series with a matching director_id.

        Param director_id:str: Filter the query by the director_id
        Return: A list of series objects.
        """
        try:
            return self.db.query(Series).filter(Series.director_id == director_id).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_director_ids(self, director_ids: list):
        try:
            return self.db.query(Series).filter(Series.director_id.in_(director_ids)).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_title(self, title: str, search: bool = False):
        """
        Function accepts a title as an argument and returns the Series object with that title.
        If no such series exists, it returns None.

        Param title:str: Search for a series by title.
        Param search:bool=False: Indicate whether the title is a search term or not.
        Return: A list of all the series that match the title.
        """
        try:
            if search:
                series = self.db.query(Series).filter(Series.title.like(f"%{title}%")).all()
            else:
                series = self.db.query(Series).filter(Series.title == title).first()
            if not series:
                raise UnknownSeriesTitleException
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_year(self, year):
        """
        Function accepts a year as an argument and returns all the series published in that year.

        Param year: Filter the series by a year published.
        Return: A list of all the series published in a given year.
        """
        try:
            return self.db.query(Series).filter(Series.year_published == year).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_episode_id(self, episode_id):
        """
        Function takes an episode ID as a parameter and returns the series that
        contains that episode. If no such series exists, it raises an exception.

        Param episode_id: Find the episode in the database
        Return: The series object that is associated with the episode_id.
        """
        try:
            return self.db.query(Series).join(Episode).filter(Episode.id == episode_id).first()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_latest_releases(self, date_limit: str):
        """
        The read_latest_releases function returns a list of all the series that were added to the database after
        the date limit. The date limit is passed in as an argument and must be in YYYY-MM-DD format.

        Param self: Access the database connection and other properties of the class.
        Param date-limit:str: Filter the query to only return series that were added after the specified date.
        Return: A list of series objects that have been added to the database since date-limit.
        """
        try:
            return self.db.query(Series).filter(Series.date_added >= date_limit).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_least_popular_series(self):
        """
        Function returns a list of series that have the least number of users watching
        them. The function first finds all the episodes that are watched by at least one user,
        then it joins those episodes with their respective series to find, which series has the
        fewest number of watchers. It then returns a list containing
        the ID and title for each series.

        Return: A list of series that have not been watched by any user.
        """
        try:
            sub1 = self.db.query(distinct(UserWatchEpisode.episode_id.label('episode'))).subquery('sub1')
            sub2 = self.db.query(Series.id).join(Episode).filter(
                Series.id == Episode.series_id).filter(Episode.id.in_(sub1)).distinct().subquery('sub2')
            return self.db.query(Series.id, Series.title).filter(Series.id.not_in(sub2))
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_group_of_genres(self, page, genres):
        """
        Function takes in a page number and a list of genre IDS. It then queries the database
        for all series that have one of those genres, skipping PER_PAGE * (page—1)
        results and returning PER_PAGE results. If there are no movies with any of the
        genres passed in, it returns an empty list.

        Param page: Determine, which page of the results should be returned
        Param genres: Filter the movies by a genre
        Return: A list of series that match the genres specified in the genres' parameter.
        """
        try:
            skip = (page - 1) * PER_PAGE
            return self.db.query(Series).filter(Series.genre_id.in_(genres)).offset(skip).limit(PER_PAGE).all()
        except Exception as exc:
            self.db.rollback()
            raise exc
