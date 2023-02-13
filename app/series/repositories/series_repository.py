from app.base import BaseCRUDRepository
from app.series.models import Series, Episode


class SeriesRepository(BaseCRUDRepository):
    """Repository for Series Model"""

    def read_series_by_genre_id(self, genre_id: str):
        try:
            series = self.db.query(Series).filter(Series.genre_id == genre_id).all()
            return series
        except Exception as e:
            self.db.rollback()
            raise

    def read_series_by_director_id(self, director_id: str):
        try:
            series = self.db.query(Series).filter(Series.director_id == director_id).all()
            return series
        except Exception as e:
            self.db.rollback()
            raise e

    def read_series_by_title(self, title: str):
        try:
            series = self.db.query(Series).filter(Series.title == title).first()
            return series
        except Exception as e:
            self.db.rollback()
            raise e

    def read_series_by_episode_id(self, episode_id):
        try:
            series = self.db.query(Series).join(Episode).filter(Episode.id == episode_id).all()
            return series
        except Exception as e:
            self.db.rollback()
            raise e
