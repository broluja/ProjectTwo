from app.db import SessionLocal
from app.series.models import Episode, Series
from app.series.repositories import EpisodeRepository, SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository


class UserWatchEpisodeServices:

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
        except Exception as e:
            raise e

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
        except Exception as e:
            raise e

    @staticmethod
    def get_my_watched_series_episodes_list(user_id: str, series_id):
        pass

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
        except Exception as e:
            raise e

    @staticmethod
    def get_users_recommendations(user_id: str, page: int):
        try:
            with SessionLocal() as db:
                user_watch_episode_repo = UserWatchEpisodeRepository(db, UserWatchEpisode)
                users_affinities = user_watch_episode_repo.read_users_affinities(user_id)
                series_repo = SeriesRepository(db, Series)
                genres = [affinity.Genre_ID for affinity in users_affinities]
                return series_repo.read_movies_by_group_of_genres(page, genres)
        except Exception as e:
            raise e
