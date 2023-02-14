from app.series.exceptions.series_exceptions import UnknownSeriesException, UnknownEpisodeException
from app.series.models import Episode, Series
from app.series.repositories import EpisodeRepository, SeriesRepository
from app.db import SessionLocal
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository

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
    def get_all_episodes_by_series(series_title: str):
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_title(series_title)
                if not series:
                    raise UnknownSeriesException
                repository = EpisodeRepository(db, Episode)
                return repository.read_by_series_id(series.id)
        except Exception as e:
            raise e

    @staticmethod
    def get_episode_by_name_and_series(name: str, title: str):
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
        except Exception as e:
            raise e

    @staticmethod
    def get_episode_by_id(episode_id: str):
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                return repository.read_by_id(episode_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_best_rated_episode(best: bool = True):
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                episode = repository.read_best_rated_episode(best=best)
                episode_repository = EpisodeRepository(db, Episode)
                response = []
                for episode_id, rating in episode:
                    obj = episode_repository.read_by_id(episode_id)
                    response.append({obj.name: round(rating, 2)})
                return response
        except Exception as e:
            raise e

    @staticmethod
    def update_episode(episode_id: str, attributes: dict):
        try:
            with SessionLocal() as db:
                repository = EpisodeRepository(db, Episode)
                obj = repository.read_by_id(episode_id)
                return repository.update(obj, attributes)
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
