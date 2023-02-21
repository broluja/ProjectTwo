from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository
from app.genres.models import Genre
from app.genres.exceptions import GenreAlreadyExistsException


class GenreRepository(BaseCRUDRepository):
    """Repository for Genre Model"""
    def create_new_genre(self, fields: dict):
        try:
            return super().create(fields)
        except IntegrityError as e:
            self.db.rollback()
            raise GenreAlreadyExistsException(message=f"Genre with name: {fields.get('name')} already created.") from e

    def read_genres_by_name(self, name: str, search: bool = True):
        try:
            if search:
                genres = self.db.query(Genre).filter(Genre.name.ilike(f"%{name}%")).all()
            else:
                genres = self.db.query(Genre).filter(Genre.name == name).first()
            return genres
        except Exception as e:
            self.db.rollback()
            raise e
