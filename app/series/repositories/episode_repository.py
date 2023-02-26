"""Episode Repository module"""
from app.base import BaseCRUDRepository
from app.series.models import Episode


class EpisodeRepository(BaseCRUDRepository):
    """Repository for Episode Model"""

    def read_by_series_id(self, series_id: str):
        """
        Function accepts a series_id as an argument and returns all the episodes associated with that
        series_id. The function first queries the database for all episodes in which their
        series_id matches the one passed to the function. It then orders them by name and returns them.

        Param series_id:str: Filter the episodes by series_id
        return: A list of episodes that are associated with the series_id passed into the function.
        """
        try:
            return self.db.query(Episode).filter(Episode.series_id == series_id).order_by(Episode.name).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_episode_name_and_series_id(self, name: str, series_id):
        """
        The read_by_episode_name_and_series_id function takes in a name and series_id as parameters.
        It then queries the database for an episode with that name and series_id,
        returning it if found or None if not found.

        Param name:str: Search for the episode by name
        Param series_id: Filter the episode by series_id
        Return: The episode object if a row is found in the database with the given name and series_id.
        """
        try:
            return self.db.query(Episode).filter(Episode.name == name).filter(Episode.series_id == series_id).first()
        except Exception as exc:
            self.db.rollback()
            raise exc
