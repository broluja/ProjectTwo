from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.service import EpisodeServices, SeriesServices
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
    def get_most_popular_series():
        try:
            series = UserWatchEpisodeServices.get_most_popular_series()
            if not series:
                return Response(content=f"We have not generated series popularity list yet.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_users_recommendations(user_id: str, page: int):
        try:
            series = UserWatchEpisodeServices.get_users_recommendations(user_id, page)
            if not series:
                return SeriesServices.read_all_series(page)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_average_series_rating_for_year(year: int):
        try:
            average = UserWatchEpisodeServices.get_average_series_rating_for_year(year)
            if not average:
                return Response(content=f"No Series from year: {year}.", status_code=200)
            return average
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_average_rating_for_series(title: str):
        try:
            avg_rating = UserWatchEpisodeServices.get_average_rating_for_series(title)
            return avg_rating
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))