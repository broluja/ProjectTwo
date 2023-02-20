from app.config import settings
from app.directors.exceptions.director_exceptions import NonExistingDirectorException
from app.directors.models import Director
from app.directors.repositories import DirectorRepository
from app.genres.exceptions.genre_exceptions import NonExistingGenreException
from app.genres.models import Genre
from app.genres.repositories import GenreRepository
from app.series.models import Series
from app.series.repositories import SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository
from app.db import SessionLocal

from datetime import date

PER_PAGE = settings.PER_PAGE


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
    def read_all_series(page):
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                skip = (page - 1) * PER_PAGE
                return repository.read_many(skip=skip, limit=PER_PAGE)
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
    def get_series_by_director_name(director: str):
        try:
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                obj = director_repo.read_directors_by_last_name(director, search=False)
                if not obj:
                    raise NonExistingDirectorException(message=f"We do not have {director} in our Database.")
                series_repo = SeriesRepository(db, Series)
                return series_repo.read_series_by_director_id(obj.id)
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
    def get_series_by_year(year: int):
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_year(str(year))
                return series
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
    def get_series_by_name(series: str, search: bool = True):
        try:
            with SessionLocal() as db:
                repo = SeriesRepository(db, Series)
                series = repo.read_series_by_title(series, search=search)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def get_series_by_genre(genre):
        try:
            with SessionLocal() as db:
                genre_repo = GenreRepository(db, Genre)
                genre_obj = genre_repo.read_genres_by_name(genre, search=False)
                if not genre_obj:
                    raise NonExistingGenreException
                series_repo = SeriesRepository(db, Series)
                series = series_repo.read_series_by_genre_id(genre_obj.id)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def get_latest_features(date_limit: str):
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                series = repository.read_latest_releases(date_limit)
                return series
        except Exception as e:
            raise e

    @staticmethod
    def show_series_never_downloaded():
        try:
            with SessionLocal() as db:
                repository = SeriesRepository(db, Series)
                series = repository.read_least_popular_series()
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
