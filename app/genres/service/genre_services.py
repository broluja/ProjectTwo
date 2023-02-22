"""Genre Service module"""
from app.genres.repositories import GenreRepository
from app.db.database import SessionLocal
from app.genres.models import Genre


class GenreServices:
    """Service for Genre routes"""
    @staticmethod
    def create_new_genre(name: str):
        """
        Function creates a new genre in the database.
        It takes one argument, name, which is the name of the genre to be created.
        The function returns a dictionary with two keys: 'id' and 'name'.
        The ID key contains an integer value representing
        the ID of the newly created genre.

        Param name:str: Set the name of the genre.
        Return: A dictionary of the new genre's.
        """
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                fields = {"name": name}
                return repository.create_new_genre(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_genres():
        """
        Function returns all genres in the database.

        Return: A list of all the genres in the database.
        """
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_genre_by_id(genre_id: str):
        """
        Function accepts a genre_id as an argument and returns the Genre object associated with that ID.
        If no Genre object is found, it raises a NotFound exception.

        Param genre_id:str: Pass the genre_id as a string to the get_genre_by_id function.
        Return: A genre object.
        """
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_by_id(genre_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_genres_by_name(name: str):
        """
        Function searches for a genre by name.
        It takes one argument, the name of the genre to search for.
        It returns a list of Genre objects that match the search criteria.

        Param name:str: Search for a genre by name.
        Return: A list of genre objects.
        """
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_genres_by_name(name)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_genre_name(genre_id: str, name: str):
        """
        Function updates the name of a genre.

        Param genre_id:str: Identify the genre that is to be updated.
        Param name:str: Set the new name of the genre.
        Return: A dictionary containing the updated genre.
        """
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                genre = repository.read_by_id(genre_id)
                updates = {"name": name}
                return repository.update(genre, updates)
        except Exception as exc:
            raise exc
