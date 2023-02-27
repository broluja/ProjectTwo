"""Genre Repository module"""
from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository
from app.genres.models import Genre
from app.genres.exceptions import GenreAlreadyExistsException


class GenreRepository(BaseCRUDRepository):
    """Repository for Genre Model"""
    def create_new_genre(self, fields: dict):
        """
        The create_new_genre function creates a new genre in the database.
        It takes one argument, fields, which is a dictionary of all the fields to be updated.
        The function checks if there is already an existing genre with that name and raises
        GenreAlreadyExistsException if so.

        Param fields:dict: Pass the name of the genre to be created.
        Return: The newly created genre instance.
        """
        try:
            return super().create(fields)
        except IntegrityError as exc:
            self.db.rollback()
            raise GenreAlreadyExistsException(message=f"Genre with name: {fields['name']} already created.") from exc

    def read_genres_by_name(self, name: str, search: bool = True):
        """
        Function accepts a name as an argument and returns all genres that match the given name.
        If no genre is found, it will return None. If multiple genres are found, it will return them all in a list.

        Param name:str: Search for a genre by name
        Param search:bool=True: Determine whether to search the database for a genre by name
        Return: A list of genre objects that match the name provided.
        """
        try:
            return self.db.query(Genre).filter(Genre.name.ilike(f"%{name}%")).all() if search \
                else self.db.query(Genre).filter(Genre.name == name.title()).first()
        except Exception as exc:
            self.db.rollback()
            raise exc
