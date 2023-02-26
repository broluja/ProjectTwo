"""Series-Actor Repository module"""
from app.base import BaseCRUDRepository
from app.series.models.series import SeriesActor


class SeriesActorRepository(BaseCRUDRepository):
    """Repository for SeriesActor Model"""

    def read_by_series(self, series_id: str):
        """
        Function accepts a series_id as an argument and returns all the actors in that series.

        Param series_id:str: Filter the results by series_id.
        Return: A list of series-actor objects that are associated with the series_id passed in.
        """
        try:
            return self.db.query(SeriesActor).filter(SeriesActor.series_id == series_id).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_actor(self, actor_id: str):
        """
        Function accepts an actor_id as a parameter and returns all series associated with that actor.

        Param actor_id:str: Filter the query by actor_id.
        Return: A list of series-actor objects.
        """
        try:
            return self.db.query(SeriesActor).filter(SeriesActor.actor_id == actor_id).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def delete_series_actor(self, series_id: str, actor_id: str):
        """
        Function deletes a series actor from the database.
        It takes two arguments, series_id and actor_id. It then queries the SeriesActor
        table for a row with that series ID and
        actor ID combination, if it finds one it deletes that row from the table.

        Param series_id:str: Identify the series that will be deleted.
        Param actor_id:str: Specify, which actor is to be deleted from the series.
        Return: The series-actor object that was deleted from the database.
        """
        try:
            series_actor = self.db.query(SeriesActor).filter(SeriesActor.actor_id == actor_id).filter(
                SeriesActor.series_id == series_id).first()
            self.db.delete(series_actor)
            self.db.commit()
            self.db.refresh()
        except Exception as exc:
            self.db.rollback()
            raise exc
