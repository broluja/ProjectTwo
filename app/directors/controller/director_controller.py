from fastapi import HTTPException
from starlette.responses import Response

from app.directors.service import DirectorServices
from app.base.base_exception import AppException


class DirectorController:

    @staticmethod
    def create_director(first_name: str, last_name: str, country: str):
        try:
            director = DirectorServices.create_new_director(first_name, last_name, country)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_directors():
        try:
            directors = DirectorServices.get_all_directors()
            return directors
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_director_by_id(director_id: str):
        try:
            director = DirectorServices.get_director_by_id(director_id)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        try:
            director = DirectorServices.search_directors_by_last_name(last_name)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_directors_by_country(country: str):
        try:
            director = DirectorServices.search_directors_by_country(country)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_director(director_id: str, attributes: dict):
        try:
            director = DirectorServices.update_director(director_id, attributes)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_director(director_id: str):
        try:
            DirectorServices.delete_director(director_id)
            return Response(content=f"Director with ID: {director_id} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
