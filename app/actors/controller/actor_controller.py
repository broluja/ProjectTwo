from fastapi import HTTPException
from starlette.responses import Response

from app.actors.service import ActorServices
from app.base import AppException


class ActorController:

    @staticmethod
    def create_actor(first_name: str, last_name: str, date_of_birth: str, country: str):
        try:
            actor = ActorServices.create_new_actor(first_name, last_name, date_of_birth, country)
            return actor
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_actors(page: int):
        try:
            actors = ActorServices.get_all_actors(page)
            if not actors:
                return Response(content="End of query.", status_code=200)
            return actors
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_actor_by_id(actor_id: str):
        try:
            actor = ActorServices.get_actor_by_id(actor_id)
            return actor
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_actor_by_last_name(actor: str):
        try:
            actors = ActorServices.get_actor_by_last_name(actor)
            if not actors:
                return Response(content=f"No actor with last name: {actor}", status_code=200)
            return actors
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_actor_by_first_name(actor: str):
        try:
            actors = ActorServices.get_actor_by_first_name(actor)
            if not actors:
                return Response(content=f"No actor with first name: {actor}", status_code=200)
            return actors
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_actor_movies(last_name: str):
        try:
            actor = ActorServices.get_actor_movies(last_name)
            return [movie.title for movie in actor.movies]
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_actor(actor_id: str, attributes: dict):
        try:
            actor = ActorServices.update_actor(actor_id, attributes)
            return actor
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_actor(actor_id: str):
        try:
            ActorServices.delete_actor(actor_id)
            return Response(content=f"Actor with ID: {actor_id} deleted.", status_code=200)
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
