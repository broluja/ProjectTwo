from app.series.models import Episode
from app.series.repositories import EpisodeRepository
from app.db import SessionLocal

PER_PAGE = 5


class EpisodeServices:

    @staticmethod
    def create_new_episode(name: str, series_id: str):
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                fields = {"name": name, "series_id": series_id}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_episodes_by_series(series_id: str):
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                return repository.read_by_series_id(series_id)
        except Exception as e:
            raise e

    @staticmethod
    def delete_episode(episode_id: str):
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                return repository.delete(episode_id)
        except Exception as e:
            raise e
