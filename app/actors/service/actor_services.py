"""Actor Service module"""
from app.actors.exceptions.actor_exceptions import ActorDataException
from app.config import settings
from app.db import SessionLocal
from app.actors.repositories import ActorRepository
from app.actors.models import Actor


PER_PAGE = settings.PER_PAGE


class ActorServices:
    """Service for actor routes"""
    @staticmethod
    def create_new_actor(first_name: str, last_name: str, date_of_birth: str, country: str):
        """
        Function creates a new actor in the database.
        It takes four parameters: first_name, last_name, date_of_birth and country.
        If any of these fields are left blank or if they do not meet the
        requirements for each field an ActorDataException is raised.

        Param first_name:str: Store the first name of the actor
        Param last_name:str: Store the last name of the actor
        Param date_of_birth:str: Store the date of birth of the actor
        Param country:str: Specify the country of origin for an actor
        Return: The object created in the database.
        """
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
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_actors(page: int):
        """
        Function retrieves all actors from the database.
        It takes a page number as an argument, and returns a list of actors on that page.

        Param page:int: Skip the first n results and return the next n
        Return: A list of actors.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                skip = (page - 1) * PER_PAGE
                actors = repository.read_many(skip=skip, limit=PER_PAGE)
                return actors
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actor_by_id(actor_id: str):
        """
        Function is used to retrieve a single actor from the database by their ID.
        It takes in an actor_id as a string and returns an Actor object.

        Param actor_id:str: Identify the actor that is to be returned
        Return: An actor object with the given ID.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_by_id(actor_id)
                return actor
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actor_by_last_name(actor: str, search: bool):
        """
        Function is used to retrieve all actors with a given last name.
        It takes in the actor as a string and returns an array of actors that match the last name.

        Param actor:str: Search the actor by last name.
        Return: A list of actors with the same last name.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actors = repository.read_actors_by_last_name(actor, search)
                return actors
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actor_by_first_name(actor: str, search: bool):
        """
        Function is used to retrieve a list of actors from the database that have the same first name.
        The function takes in one argument, which is the actor's first name.
        The function returns a list of actors with matching names.

        Param actor:str: Search for a specific actor by first name
        Return: A list of actors that match the first name provided.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actors = repository.read_actors_by_first_name(actor, search)
                return actors
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actor_by_country(country: str, search: bool):
        """
        Function returns a list of actors from the database that match the country provided.
        The search parameter is optional and if true, will return all actors from matching country.

        Param country:str: Filter the actors by country.
        Param search:bool: Search for a specific actor by name.
        Return: A list of actors filtered by country.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                return repository.read_actors_by_country(country, search)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actors_by_year_of_birth(year: int):
        """
        Function returns a list of actors who were born in the given year.
        The function accepts one argument, year, which is an integer representing the birth year to search for.

        Param year:int: Filter the actors by a year of birth.
        Return: A list of actors that have their birth year set to the specified year.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                return repository.read_actors_by_year_of_birth(year)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_actor_movies(last_name: str):
        """
        Function returns a list of movies that the actor has been in.
        The function takes one argument, last_name, which is the last name of an actor.

        Param last_name:str: Specify the last name of the actor that is being searched for
        Return: A list of movies that the actor has starred in.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_actors_by_last_name(last_name, literal=True)
                return actor
        except Exception as exc:
            raise exc

    @staticmethod
    def update_actor(actor_id, attributes):
        """
        Function updates an actor's information.

        Param actor_id: Identify the actor to update.
        Param attributes: Update the actor with new values.
        Return: The updated actor object.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.read_by_id(actor_id)
                actor = repository.update(actor, attributes)
                return actor
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_actor(actor_id: str):
        """
        Function deletes an actor from the database.

        Param actor_id:str: Identify the actor that is to be deleted
        Return: The deleted actor.
        """
        try:
            with SessionLocal() as db:
                repository = ActorRepository(db, Actor)
                actor = repository.delete(actor_id)
                return actor
        except Exception as exc:
            raise exc
