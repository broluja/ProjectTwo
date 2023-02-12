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
                watched_episodes = watched_episodes_repository.read_by_user_id(user_id)
                series = set([episode.series_id for episode in watched_episodes])
                repository = SeriesRepository(db, Series)
                series_objects = [repository.read_by_id(series_id) for series_id in series]
                return series_objects
        except Exception as e:
            raise e
