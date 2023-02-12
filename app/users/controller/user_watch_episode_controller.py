from fastapi import HTTPException

from app.base import AppException
from app.series.service import EpisodeServices
from app.users.service import UserWatchEpisodeServices


class UserWatchEpisodeController:

    @staticmethod
    def user_watch_episode(user_id: str, name: str, series_title):
        try:
            episode = EpisodeServices.get_episode_by_name_and_series(name, series_title)
            watch_episode = UserWatchEpisodeServices.user_watch_episode(user_id, episode.id)
            return watch_episode
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def user_rate_episode(user_id: str, name: str, series_title: str, rating: int):
        try:
            episode = EpisodeServices.get_episode_by_name_and_series(name, series_title)
            rate_episode = UserWatchEpisodeServices.rate_episode(user_id, episode.id, rating)
            return rate_episode
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        pass