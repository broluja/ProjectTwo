from app.actors.exceptions.actor_exceptions import ActorDataException
from app.config import settings
from app.db import SessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


PER_PAGE = settings.PER_PAGE


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
                if not all(fields.values()):
                    raise ActorDataException(message="Please fill all the fields.")
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_actors(page: int):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                skip = (page - 1) * PER_PAGE
                actors = repository.read_many(skip=skip, limit=PER_PAGE)
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

    @staticmethod
    def get_actor_by_last_name(actor: str):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actors = repository.read_actors_by_last_name(actor)
                return actors
        except Exception as e:
            raise e

    @staticmethod
    def get_actor_movies(last_name: str):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_actors_by_last_name(last_name, literal=True)
                return actor
        except Exception as e:
            raise e

    @staticmethod
    def update_actor(actor_id, attributes):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_by_id(actor_id)
                actor = repository.update(actor, attributes)
                return actor
        except Exception as e:
            raise e

    @staticmethod
    def delete_actor(actor_id: str):
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.delete(actor_id)
                return actor
        except Exception as e:
            raise e
