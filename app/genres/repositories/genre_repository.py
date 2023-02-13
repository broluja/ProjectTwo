from app.base import BaseCRUDRepository
from app.genres.models import Genre


class GenreRepository(BaseCRUDRepository):
    """Repository for Genre Model"""

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
