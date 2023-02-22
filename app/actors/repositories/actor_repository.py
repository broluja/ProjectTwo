"""Actor Repository module"""
from app.actors.models import Actor
from app.base import BaseCRUDRepository


class ActorRepository(BaseCRUDRepository):
    """Repository for Actor Model"""

    def read_actors_by_first_name(self, first_name: str, search: bool = True):
        """
        Function is used to retrieve all actors with a given first name.
        The function takes in the first_name as an argument and returns a
        list of actors that match the search criteria.

        Param first_name:str: Store the first name of the actor
        Param search:bool=True: Determine whether the search should be case-sensitive or not
        Return: All actors whose first name contains the first_name argument.
        """
        try:
            if search:
                actors = self.db.query(Actor).filter(Actor.first_name.ilike(f"%{first_name}%")).all()
            else:
                actors = self.db.query(Actor).filter(Actor.first_name == first_name).first()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_actors_by_last_name(self, last_name: str, literal=False):
        """
        Function takes a last name as an argument and returns all actors with that last name.
        It is case-insensitive, so it will return results even if the user enters a
        capitalized version of the same last name.

        Param last_name:str: Filter the actors by last name
        Param literal=False: Indicate whether the last_name parameter is a literal or not.
        Return: The list of actors whose last name contains the string passed as an argument.
        """
        try:
            if literal:
                actors = self.db.query(Actor).filter(Actor.last_name == last_name).first()
            else:
                actors = self.db.query(Actor).filter(Actor.last_name.ilike(f"%{last_name}%")).all()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_actors_by_country(self, country: str):
        """
        Function accepts a country name as an argument and returns all actors from that country.

        Param country:str: Filter the actors by country
        Return: A list of actors that are from the specified country
        """
        try:
            actors = self.db.query(Actor).filter(Actor.country == country).all()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc
