"""Director Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.directors.service import DirectorServices
from app.base.base_exception import AppException


class DirectorController:
    """Controller for Director routes"""
    @staticmethod
    def create_director(first_name: str, last_name: str, country: str):
        try:
            director = DirectorServices.create_new_director(first_name, last_name, country)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_directors():
        try:
            directors = DirectorServices.get_all_directors()
            if not directors:
                return Response("No directors in our Database yet.", status_code=200)
            return directors
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_director_by_id(director_id: str):
        try:
            director = DirectorServices.get_director_by_id(director_id)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        try:
            director = DirectorServices.search_directors_by_last_name(last_name)
            if not director:
                return Response(content=f"No Director with last name: {last_name} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_first_name(first_name: str):
        try:
            director = DirectorServices.search_directors_by_first_name(first_name)
            if not director:
                return Response(content=f"No Director with first name: {first_name} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_directors_by_country(country: str):
        try:
            director = DirectorServices.search_directors_by_country(country)
            if not director:
                return Response(content=f"No Director with first name: {country} in our Database.", status_code=200)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_director(director_id: str, attributes: dict):
        try:
            director = DirectorServices.update_director(director_id, attributes)
            return director
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_director(director_id: str):
        try:
            DirectorServices.delete_director(director_id)
            return Response(content=f"Director with ID: {director_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
