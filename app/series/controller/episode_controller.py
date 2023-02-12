from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.service import EpisodeServices


class EpisodeController:

    @staticmethod
    def create_episode(name: str, series_id: str):
        try:
            episode = EpisodeServices.create_new_episode(name, series_id)
            return episode
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_episodes_by_series(series_title: str):
        try:
            episodes = EpisodeServices.get_all_episodes_by_series(series_title)
            return episodes
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_episode(episode_id: str):
        try:
            EpisodeServices.delete_episode(episode_id)
            return Response(content=f"Episode with ID: {episode_id} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
