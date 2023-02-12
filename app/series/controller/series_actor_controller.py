from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.controller import SeriesController
from app.series.service import SeriesActorService
from app.directors.service import DirectorServices
from app.genres.service import GenreServices


class SeriesActorController:

    @staticmethod
    def create_series_actor(series_id: str, actor_id: str):
        try:
            series_actor = SeriesActorService.create_new_series_actor(series_id, actor_id)
            return series_actor
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_with_actors(series_id: str):
        try:
            series = SeriesController.get_series_by_id(series_id)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_with_director_and_genre(series_id: str):
        try:
            series = SeriesController.get_series_by_id(series_id)
            director = DirectorServices.get_director_by_id(series.director_id)
            genre = GenreServices.get_genre_by_id(series.genre_id)
            series.director = director
            series.genre = genre
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_series_actor(series_id: str, actor_id: str):
        try:
            SeriesActorService.remove_series_actor(series_id, actor_id)
            return Response(content=f"Actor removed from series.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
