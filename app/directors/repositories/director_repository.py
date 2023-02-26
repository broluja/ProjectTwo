"""Director Repository module"""
from app.base import BaseCRUDRepository
from app.directors.models import Director


class DirectorRepository(BaseCRUDRepository):
    """Repository for Director Model"""

    def read_directors_by_country(self, country: str):
        """
        Function takes a country as an argument and returns all the directors who have directed
        a movie in that country. It does this by querying the database for all directors
        with a given country, then returning them.

        Param country:str: Filter the query by country.
        Return: A list of director objects that have the same country as the input parameter.
        """
        try:
            return self.db.query(Director).filter(Director.country == country).all()
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_directors_by_last_name(self, last_name: str, search: bool = True):
        """
        Function is used to retrieve a list of directors from the database by last name.
        It accepts two parameters, last_name and search. If search is set to True, it will return
        a list of all directors with that last name in the database. If search is set to False,
        it will return the first director with that exact last name in the database.

        Param last_name:str: Search for directors by last name
        Param search:bool=True: Indicate whether the function is being used to search for a director or not
        Return: A list of director objects.
        """
        try:
            if search:
                result = self.db.query(Director).filter(Director.last_name.ilike(f"%{last_name}%")).all()
            else:
                result = self.db.query(Director).filter(Director.last_name == last_name).first()
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_directors_by_first_name(self, first_name: str, search: bool = True):
        """
        Function is used to retrieve all directors with a given first name.
        It takes in the first_name as an argument and returns a list of directors
        that match the search criteria.

        Param first_name:str: Store the first name of the director we want to search for.
        Param search:bool=True: Determine whether to search for the first name in the database.
        Return: A list of directors with the first name that matches the parameter first_name.
        """
        try:
            if search:
                directors = self.db.query(Director).filter(Director.first_name.ilike(f"%{first_name}%")).all()
            else:
                directors = self.db.query(Director).filter(Director.first_name == first_name).first()
            return directors
        except Exception as exc:
            self.db.rollback()
            raise exc
