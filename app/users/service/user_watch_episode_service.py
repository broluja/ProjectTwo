"""UserWatchEpisode Service module"""
from starlette.responses import Response

from app.db import SessionLocal
from app.series.exceptions.series_exceptions import UnknownSeriesException
from app.series.models import Episode, Series
from app.series.repositories import EpisodeRepository, SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository


class UserWatchEpisodeServices:
    """Service for UserWatchEpisode routes."""
    @staticmethod
    def user_watch_episode(user_id: str, episode_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                episode_repo = EpisodeRepository(db, Episode)
                episode = episode_repo.read_by_id(episode_id)
                if watched_episode:
                    return {"message": "Watch episode again.", "link": episode.link}
                fields = {"user_id": user_id, "episode_id": episode_id}
                repository.create(fields)
                return {"message": "Watch this episode now.", "link": episode.link}
        except Exception as exc:
            raise exc

    @staticmethod
    def rate_episode(user_id: str, episode_id: str, rating: int):
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                if watched_episode:
                    obj = repository.update(watched_episode, {"rating": rating})
                    return obj
                else:
                    fields = {"user_id": user_id, "episode_id": episode_id, "rating": rating}
                    return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_most_popular_series():
        try:
            with SessionLocal() as db:
                repo = UserWatchEpisodeRepository(db, UserWatchEpisode)
                episodes = repo.read_episode_views()
                series_repo = SeriesRepository(db, Series)
                response = {}
                for series_id, views in episodes:
                    series = series_repo.read_by_id(series_id)
                    response.update({series.title: views})
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_users_recommendations(user_id: str, page: int):
        try:
            with SessionLocal() as db:
                user_watch_episode_repo = UserWatchEpisodeRepository(db, UserWatchEpisode)
                users_affinities = user_watch_episode_repo.read_users_affinities(user_id)
                series_repo = SeriesRepository(db, Series)
                genres = [affinity.Genre_ID for affinity in users_affinities]
                return series_repo.read_series_by_group_of_genres(page, genres)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_series_rating_for_year(year: int):
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_year(str(year))
                if not series:
                    return Response(content=f"No Series from this year: {year}", status_code=200)
                episode_ids = [episode.id for obj in series for episode in obj.episodes]
                user_watch_episode_repo = UserWatchEpisodeRepository(db, Episode)
                average = user_watch_episode_repo.read_average_rating(episode_ids)
                response = {"Year": year}
                response.update(average)
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_rating_for_series(title: str):
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_title(title, search=False)
                if not series:
                    raise UnknownSeriesException
                episode_ids = [episode.id for episode in series.episodes]
                user_watch_episode_repo = UserWatchEpisodeRepository(db, Episode)
                average = user_watch_episode_repo.read_average_rating(episode_ids)
                response = {"Series": series.title}
                response.update(average)
                return response
        except Exception as exc:
            raise exc
