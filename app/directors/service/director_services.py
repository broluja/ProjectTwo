"""Director Service module"""
from app.directors.repositories import DirectorRepository
from app.db.database import SessionLocal
from app.directors.models import Director


class DirectorServices:
    """Service for Director routes"""
    @staticmethod
    def create_new_director(first_name: str, last_name: str, country: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                fields = {"first_name": first_name, "last_name": last_name, "country": country}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_directors():
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_all()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_director_by_id(director_id: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_by_id(director_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_last_name(last_name)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_first_name(first_name: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_first_name(first_name)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_directors_by_country(country: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_country(country)
        except Exception as exc:
            raise exc

    @staticmethod
    def update_director(director_id, attributes):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                director = repository.read_by_id(director_id)
                return repository.update(director, attributes)
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_director(director_id):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.delete(director_id)
        except Exception as exc:
            raise exc
