"""Director Service module"""
from app.directors.repositories import DirectorRepository
from app.db.database import SessionLocal
from app.directors.models import Director


class DirectorServices:
    """Service for Director routes"""
    @staticmethod
    def create_new_director(first_name: str, last_name: str, country: str):
        """
        The create_new_director function creates a new director in the database.
        It takes three parameters: first_name, last_name, and country.
        The function returns the newly created director.

        Param first_name:str: Pass the first name of the director
        Param last_name:str: Pass the last name of the director
        Param country:str: Specify the country of origin for a director
        Return: The newly created director.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                fields = {"first_name": first_name, "last_name": last_name, "country": country}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_directors():
        """
        Function returns all directors in the database.

        Return: A list of all the directors.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_director_by_id(director_id: str):
        """
        Function is used to retrieve a director by their ID.
        It takes in the director_id as an argument and returns the corresponding
        director object.

        Param director_id:str: Identify the director that is being searched for
        Return: A dictionary containing the director's ID, name and birthdate.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_by_id(director_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        """
        Function searches for directors by last name. It takes a string as an argument and
        returns a list of dictionaries containing the director's first and last names,
        as well as their ID number.

        Param last_name:str: Search for directors by last name.
        Return: A list of directors with the same last name.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_last_name(last_name)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_first_name(first_name: str):
        """
        Function searches for directors by first name. It takes a string as an
        argument and returns a list of dictionaries containing the director's details.

        Param first_name:str: Pass in the first name of the director that we want to search for.
        Return: A list of director objects.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_first_name(first_name)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_country(country: str):
        """
        Function searches for directors by country. It takes a string as an argument
        and returns a list of dictionaries containing the director's name, birth year, and country.

        Param country:str: Search for directors that are from the specified country.
        Return: A list of directors that live in the country specified.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_country(country)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_director(director_id, attributes):
        """
        Function updates a director's information.

        Param director_id: Identify the director to be updated
        Param attributes: Update the director object with new values
        Return: The updated director object.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                director = repository.read_by_id(director_id)
                return repository.update(director, attributes)
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_director(director_id):
        """
        Function deletes a director from the database.
        It takes in a director_id as an argument and returns the deleted object.

        Param director_id: Identify the director to be deleted.
        Return: The number of rows deleted.
        """
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.delete(director_id)
        except Exception as exc:
            raise exc
