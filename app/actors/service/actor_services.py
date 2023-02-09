from app.db import SessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


class ActorServices:

    @staticmethod
    def create_new_actor(first_name: str, last_name: str, date_of_birth: str, country: str):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                fields = {"first_name": first_name,
                          "last_name": last_name,
                          "date_of_birth": date_of_birth,
                          "country": country}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_actors():
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actors = repository.read_all()
                return actors
        except Exception as e:
            raise e

    @staticmethod
    def get_actor_by_id(actor_id: str):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_by_id(actor_id)
                return actor
        except Exception as e:
            raise e
