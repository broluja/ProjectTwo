import pytest

from app.base import AppException
from app.tests import TestClass, TestingSessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


class TestUserRepo(TestClass):
    actor = None

    def create_actor(self):
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            attributes = {"first_name": "John",
                          "last_name": "Doe",
                          "date_of_birth": "1983-10-10",
                          "country": "USA"}
            actor = actor_repository.create(attributes)
            self.actor = actor

    def test_create_actor(self):
        self.create_actor()
        assert self.actor.first_name == "John"
        assert self.actor.last_name == "Doe"
        assert self.actor.country == "USA"

    def test_create_actor_first_name_error(self):
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            attributes = {"first_name": "",
                          "last_name": "Doe",
                          "date_of_birth": "1983-10-10",
                          "country": "USA"}
            actor_repository.create(attributes)
