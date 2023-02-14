from app.series.models import Series
from app.series.repositories import SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository
from app.db import SessionLocal

from datetime import date

PER_PAGE = 5


class SeriesServices:

    @staticmethod
    def create_new_series(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                fields = {"title": title,
                          "date_added": date.today(),
                          "year_published": year_published,
                          "director_id": director_id,
                          "genre_id": genre_id}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def read_all_series():
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                return repository.read_all()
        except Exception as e:
            raise e

    @staticmethod
    def get_series_by_id(series_id: str):
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                return repository.read_by_id(series_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_my_series(user_id: str):
        try:
            with SessionLocal() as db:
                watched_episodes_repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episodes = watched_episodes_repository.read_users_episodes_and_series(user_id)
                my_series = set(obj.title for obj in watched_episodes)
                return my_series
        except Exception as e:
            raise e

    @staticmethod
    def get_series_by_episode_id(episode_id: str):
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                series = repo.read_series_by_episode_id(episode_id)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def get_series_by_name(series: str):
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                series = repo.read_series_by_title(series, search=True)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def update_series_data(series_id: str, attributes: dict):
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                obj = repo.read_by_id(series_id)
                series = repo.update(obj, attributes)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def delete_series(series_id: str):
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                return repository.delete(series_id)
        except Exception as e:
            raise e
