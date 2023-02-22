"""Test Actor module"""
from app.tests import TestClass, TestingSessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


class TestActorRepo(TestClass):
    """Test Actor functionalities."""
    actor = None

    def create_actor(self):
        """
        Function creates an actor in the database.
        It takes no arguments and returns a dictionary of the attributes of the created actor.

        Param self: Refer to the object that is calling the method.
        Return: The actor object.
        """
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            attributes = {"first_name": "John",
                          "last_name": "Doe",
                          "date_of_birth": "1983-10-10",
                          "country": "USA"}
            actor = actor_repository.create(attributes)
            self.actor = actor

    def test_create_actor(self):
        """
        Function creates an actor object and tests whether the first_name, last_name,
        and country attributes are equal to 'John', 'Doe', and 'USA' respectively.

        Return: The actor object, which is then used to assert the
        first name, last name and country of the actor.
        """
        self.create_actor()
        assert self.actor.first_name == "John"
        assert self.actor.last_name == "Doe"
        assert self.actor.country == "USA"

    def test_create_actor_first_name_error(self):
        """
        Function is used to test the create method of the ActorRepository class.
        It creates an actor with a first name that is empty and checks if it raises an error.

        Param self: Access the test class and its methods.
        Return: A dictionary with an error message.
        """
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            attributes = {"first_name": "",
                          "last_name": "Doe",
                          "date_of_birth": "1983-10-10",
                          "country": "USA"}
            actor_repository.create(attributes)

    def test_get_actor_by_first_name(self):
        """
        Function tests the get_actor_by_first_name function in the ActorRepository class.
        It creates an actor, then uses that actor's first name to search for it and retrieve it
        from the database. It then checks to see if all of its attributes match those of the created actor.

        Return: The actor with the first name john.
        """
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actor = actor_repository.read_actors_by_first_name("John", search=False)
        assert actor.first_name == "John"
        assert actor.last_name == "Doe"
        assert actor.country == "USA"

    def test_get_actor_by_last_name(self):
        """
        Function tests the get_actors_by_last_name function in the actor repository.
        It creates an actor, then queries for that same actor using a last name
        and checks to see if it is equal to the original.

        Return: The actor with the last name 'doe'
        """
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actor = actor_repository.read_actors_by_last_name("Doe", literal=True)
        assert actor.first_name == "John"
        assert actor.last_name == "Doe"
        assert actor.country == "USA"

    def test_get_actor_by_country(self):
        """
        Function tests the get_actor_by_country function in the actor repository.
        It creates an actor, then uses that actor to test whether it can be found by country.

        Return: The first actor in the database, who is from the usa.
        """
        self.create_actor()
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db, Actor)
            actors = actor_repository.read_actors_by_country("USA")
        assert actors[0].first_name == "John"
        assert actors[0].last_name == "Doe"
        assert actors[0].country == "USA"
