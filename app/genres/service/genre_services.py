"""Genre Service module"""
from app.genres.repositories import GenreRepository
from app.db.database import SessionLocal
from app.genres.models import Genre


class GenreServices:
    """Service for Genre routes"""
    @staticmethod
    def create_new_genre(name: str):
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                fields = {"name": name}
                return repository.create_new_genre(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_genres():
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_genre_by_id(genre_id: str):
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_by_id(genre_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_genres_by_name(name: str):
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                return repository.read_genres_by_name(name)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_genre_name(genre_id: str, name: str):
        try:
            with SessionLocal() as db:
                repository = GenreRepository(db, Genre)
                genre = repository.read_by_id(genre_id)
                updates = {"name": name}
                return repository.update(genre, updates)
        except Exception as exc:
            raise exc
