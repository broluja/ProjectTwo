"""Episode Service module"""
from app.config import settings
from app.series.exceptions.series_exceptions import UnknownSeriesException, UnknownEpisodeException
from app.series.models import Episode, Series
from app.series.repositories import EpisodeRepository, SeriesRepository
from app.db import SessionLocal
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository

PER_PAGE = settings.PER_PAGE


class EpisodeServices:
    """Service for Episode routes"""
    @staticmethod
    def create_new_episode(name: str, series_id: str):
        """
        Function creates a new episode in the database.
        It takes two parameters, name and series_id. It returns an Episode object.

        Param name:str: Set the name of the episode.
        Param series_id:str: Specify the series that the episode is associated with.
        Return: The ID of the newly created episode.
        """
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                fields = {"name": name, "series_id": series_id}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_episodes_by_series(series_title: str):
        """
        Function returns all episodes for a given series.
        The function takes one argument, the title of the series to be searched.
        If no such series exists in the database, an UnknownSeriesException is raised.

        Param series_title:str: Get the series from the database.
        Return: A list of all episodes for a given series.
        """
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_title(series_title)
                if not series:
                    raise UnknownSeriesException
                repository = EpisodeRepository(db, Episode)
                return repository.read_by_series_id(series.id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_episode_by_name_and_series(name: str, title: str):
        """
        Function takes a name and title of an episode as parameters.
        It then searches the database for that episode, returning it if found. If not found, it raises an exception.

        Param name:str: Search for the episode name.
        Param title:str: Search for a series.
        Return: An episode object.
        """
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_title(title)
                if not series:
                    raise UnknownSeriesException
                episodes_repository = EpisodeRepository(db, Episode)
                episode = episodes_repository.read_by_episode_name_and_series_id(name, series.id)
                if not episode:
                    raise UnknownEpisodeException
                return episode
        except Exception as exc:
            raise exc

    @staticmethod
    def get_episode_by_id(episode_id: str):
        """
        Function is used to retrieve a single episode from the database.
        It takes one argument, which is the ID of the episode you want to retrieve.
        The function returns an Episode object.

        Param episode_id:str: Pass the ID of the episode that is to be returned.
        Return: A single episode object based on the ID passed in.
        """
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                return repository.read_by_id(episode_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_best_rated_episode(best: bool = True):
        """
        Function returns the best rated episode from the database.
        The function takes one parameter, best, which is a boolean value that defaults to True.
        If best is set to False then it will return the worst rated episode.

        Param best:bool=True: Determine whether the best rated or worst rated episode should be returned.
        Return: The best rated episode from the database.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                episode = repository.read_best_rated_episode(best=best)
                episode_repository = EpisodeRepository(db, Episode)
                response = []
                for episode_id, rating in episode:
                    obj = episode_repository.read_by_id(episode_id)
                    response.append({obj.name: {"Rating": round(rating, 2), "Series": obj.series_id}})
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def update_episode(episode_id: str, attributes: dict):
        """
        Function updates an episode with the given attributes.

        Param episode_id:str: Identify the episode that is to be updated.
        Param attributes:dict: Update the episode with new values.
        Return: A dict with the updated episode object.
        """
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                obj = repository.read_by_id(episode_id)
                return repository.update(obj, attributes)
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_episode(episode_id: str):
        """
        Function deletes an episode from the database.

        Param episode_id:str: Identify the episode to be deleted.
        Return: A dictionary.
        """
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                return repository.delete(episode_id)
        except Exception as exc:
            raise exc
