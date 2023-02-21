"""Series-Actor Repository module"""
from app.base import BaseCRUDRepository
from app.series.models.series import SeriesActor


class SeriesActorRepository(BaseCRUDRepository):
    """Repository for SeriesActor Model"""

    def read_by_series(self, series_id: str):
        try:
            series_actors = self.db.query(SeriesActor).filter(SeriesActor.series_id == series_id).all()
            return series_actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_actor(self, actor_id: str):
        try:
            series = self.db.query(SeriesActor).filter(SeriesActor.actor_id == actor_id).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def delete_series_actor(self, series_id: str, actor_id: str):
        try:
            series_actor = self.db.query(SeriesActor).filter(SeriesActor.actor_id == actor_id).filter(
                SeriesActor.series_id == series_id).first()
            self.db.delete(series_actor)
            self.db.commit()
            self.db.refresh()
        except Exception as exc:
            self.db.rollback()
            raise exc
