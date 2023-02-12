from app.db import SessionLocal
from app.series.models import SeriesActor
from app.series.repositories import SeriesActorRepository


class SeriesActorService:

    @staticmethod
    def create_new_series_actor(series_id: str, actor_id: str):
        try:
            with SessionLocal() as db:
                repository = SeriesActorRepository(db, SeriesActor)
                fields = {"series_id": series_id,
                          "actor_id": actor_id}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def remove_series_actor(series_id: str, actor_id: str):
        try:
            with SessionLocal() as db:
                repository = SeriesActorRepository(db, SeriesActor)
                return repository.delete_series_actor(series_id, actor_id)
        except Exception as e:
            raise e