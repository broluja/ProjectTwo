"""Test Actor module"""
from app.tests import TestClass, TestingSessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


class TestActorRepo(TestClass):
    """Test Actor functionalities."""
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

    def test_get_actor_by_first_name(self):
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actor = actor_repository.read_actors_by_first_name("John", search=False)
        assert actor.first_name == "John"
        assert actor.last_name == "Doe"
        assert actor.country == "USA"

    def test_get_actor_by_last_name(self):
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actor = actor_repository.read_actors_by_last_name("Doe", literal=True)
        assert actor.first_name == "John"
        assert actor.last_name == "Doe"
        assert actor.country == "USA"

    def test_get_actor_by_country(self):
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actors = actor_repository.read_actors_by_country("USA")
        assert actors[0].first_name == "John"
        assert actors[0].last_name == "Doe"
        assert actors[0].country == "USA"
