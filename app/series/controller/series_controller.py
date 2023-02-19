from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.directors.service import DirectorServices
from app.genres.service import GenreServices
from app.series.service import SeriesServices


class SeriesController:

    @staticmethod
    def create_series(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            director = DirectorServices.get_director_by_id(director_id)
            genre = GenreServices.get_genre_by_id(genre_id)
            series = SeriesServices.create_new_series(title, year_published, director_id, genre_id)
            series.director = director
            series.genre = genre
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def read_all_series(page):
        try:
            series = SeriesServices.read_all_series(page)
            if not series:
                return Response(content="End of query.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_data(title: str):
        try:
            series = SeriesServices.get_series_by_name(title, search=False)
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
    def get_series_by_director_name(director: str):
        try:
            series = SeriesServices.get_series_by_director_name(director)
            if not series:
                return Response(content=f"No Series from Director: {director}.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_by_id(series_id: str):
        try:
            series = SeriesServices.get_series_by_id(series_id)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_my_series(user_id: str):
        try:
            series = SeriesServices.get_my_series(user_id)
            if not series:
                return Response(content="You have not watched any series yet.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_by_episode_id(episode_id: str):
        try:
            series = SeriesServices.get_series_by_episode_id(episode_id)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_by_name(series: str):
        try:
            series = SeriesServices.get_series_by_name(series)
            if not series:
                return Response(content=f"No Series with name: {series}.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_series_by_genre(genre: str):
        try:
            series = SeriesServices.get_series_by_genre(genre)
            if not series:
                return Response(content=f"No Series with genre: {genre}.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_latest_features(date_limit: str):
        try:
            series = SeriesServices.get_latest_features(date_limit)
            if not series:
                return Response(content="No series in latest list.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def show_series_never_downloaded():
        try:
            series = SeriesServices.show_series_never_downloaded()
            if not series:
                return Response(content="There are no series that never have been downloaded.", status_code=200)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_series_data(series_id: str, attributes: dict):
        try:
            series = SeriesServices.update_series_data(series_id, attributes)
            return series
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_series(series_id: str):
        try:
            SeriesServices.delete_series(series_id)
            return Response(content=f"Series with ID: {series_id} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
