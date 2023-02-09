from app.directors.repositories import DirectorRepository
from app.db.database import SessionLocal
from app.directors.models import Director


class DirectorServices:

    @staticmethod
    def create_new_director(first_name: str, last_name: str, country: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                fields = {"first_name": first_name, "last_name": last_name, "country": country}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_directors():
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_all()
        except Exception as e:
            raise e

    @staticmethod
    def get_director_by_id(director_id: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_by_id(director_id)
        except Exception as e:
            raise e

    @staticmethod
    def search_directors_by_last_name(last_name: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_last_name(last_name)
        except Exception as e:
            raise e

    @staticmethod
    def search_directors_by_country(country: str):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                return repository.read_directors_by_country(country)
        except Exception as e:
            raise e

    @staticmethod
    def update_director(**kwargs):
        try:
            with SessionLocal() as db:
                repository = DirectorRepository(db, Director)
                director_id = kwargs.pop("director_id")
                director = repository.read_by_id(director_id)
                fields = {key: value for key, value in kwargs.items() if value is not None}
                return repository.update(director, fields)
        except Exception as e:
            raise e
