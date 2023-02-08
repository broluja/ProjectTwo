from fastapi import HTTPException

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
    def get_all_actors():
        try:
            actors = ActorServices.get_all_actors()
            return actors
        except AppException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
