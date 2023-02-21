"""Director Repository module"""
from app.base import BaseCRUDRepository
from app.directors.models import Director


class DirectorRepository(BaseCRUDRepository):
    """Repository for Director Model"""

    def read_directors_by_country(self, country: str):
        try:
            directors = self.db.query(Director).filter(Director.country == country).all()
            return directors
        except Exception as e:
            self.db.rollback()
            raise e

    def read_directors_by_last_name(self, last_name: str, search: bool = True):
        try:
            if search:
                result = self.db.query(Director).filter(Director.last_name.ilike(f"%{last_name}%")).all()
            else:
                result = self.db.query(Director).filter(Director.last_name == last_name).first()
            return result
        except Exception as e:
            self.db.rollback()
            raise e

    def read_directors_by_first_name(self, first_name: str, search: bool = True):
        try:
            if search:
                directors = self.db.query(Director).filter(Director.first_name.ilike(f"%{first_name}%")).all()
            else:
                directors = self.db.query(Director).filter(Director.first_name == first_name).first()
            return directors
        except Exception as e:
            self.db.rollback()
            raise e
