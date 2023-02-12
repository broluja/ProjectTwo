from fastapi import HTTPException

from app.base import AppException
from app.series.service import SeriesServices


class SeriesController:

    @staticmethod
    def create_series(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            movie = SeriesServices.create_new_series(title, year_published, director_id, genre_id)
            return movie
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def read_all_series():
        try:
            series = SeriesServices.read_all_series()
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_series(user_id: str):
        try:
            series = SeriesServices.get_my_series(user_id)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
