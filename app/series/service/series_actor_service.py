"""SeriesActor service module"""
from app.db import SessionLocal
from app.series.models import SeriesActor
from app.series.repositories import SeriesActorRepository


class SeriesActorService:
    """Service for SeriesActor routes"""
    @staticmethod
    def create_new_series_actor(series_id: str, actor_id: str):
        """
        The create_new_series_actor function creates a new series actor record in the database.
        It takes two parameters, series_id and actor_id, which are both strings.
        The function returns a SeriesActor object.

        Param series_id:str: Specify the ID of the series that is being added to.
        Param actor_id:str: Specify the actor that will be added to the series.
        Return: A series actor object.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesActorRepository(db, SeriesActor)
                fields = {"series_id": series_id,
                          "actor_id": actor_id}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def remove_series_actor(series_id: str, actor_id: str):
        """
        Function removes an actor from a series.
        The function takes two parameters, the ID of the series, and the ID of the actor to be removed.
        It returns a dictionary with status code 200 on success, or a dictionary with
        status code 404 if no record was found.

        Param series_id:str: Identify the series that an actor is to be removed from
        Param actor_id:str: Specify the actor to be removed from the series
        Return: The number of rows that were deleted.
        """
        try:
            with SessionLocal() as db:
                repository = SeriesActorRepository(db, SeriesActor)
                return repository.delete_series_actor(series_id, actor_id)
        except Exception as exc:
            raise exc
