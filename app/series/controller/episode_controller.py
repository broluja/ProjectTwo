"""Episode Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.service import EpisodeServices


class EpisodeController:
    """Controller for Episode routes"""
    @staticmethod
    def create_episode(name: str, series_id: str):
        try:
            episode = EpisodeServices.create_new_episode(name, series_id)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_episodes_by_series(series_title: str):
        try:
            episodes = EpisodeServices.get_all_episodes_by_series(series_title)
            if not episodes:
                Response(content=f"No Episodes for Series: {series_title}.", status_code=200)
            return episodes
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_episode_by_id(episode_id: str):
        try:
            episode = EpisodeServices.get_episode_by_id(episode_id)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_best_rated_episode(best: bool = True):
        try:
            episodes = EpisodeServices.get_best_rated_episode(best=best)
            if not episodes:
                return Response(content=f"We have not generated episode popularity list yet.", status_code=200)
            return episodes
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_episode(episode_id: str, attributes: dict):
        try:
            episode = EpisodeServices.update_episode(episode_id, attributes)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_episode(episode_id: str):
        try:
            EpisodeServices.delete_episode(episode_id)
            return Response(content=f"Episode with ID: {episode_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
