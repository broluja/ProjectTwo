from fastapi import HTTPException
from starlette.responses import Response

from app.genres.service import GenreServices
from app.base.base_exception import AppException


class GenreController:

    @staticmethod
    def create_director(name: str):
        try:
            genre = GenreServices.create_new_director(name)
            return genre
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_genres():
        try:
            genres = GenreServices.get_all_genres()
            if not genres:
                return Response(content=f"No Genres in our Database yet.", status_code=200)
            return genres
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_genre_by_id(genre_id: str):
        try:
            genre = GenreServices.get_genre_by_id(genre_id)
            return genre
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def search_genres_by_name(name: str):
        try:
            genres = GenreServices.search_genres_by_name(name)
            if not genres:
                return Response(content=f"No Genre: {name} in our Database.", status_code=200)
            return genres
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_genre(genre_id: str, name: str):
        try:
            director = GenreServices.update_genre_name(genre_id, name)
            return director
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
