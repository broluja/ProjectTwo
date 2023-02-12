from app.base import BaseCRUDRepository
from app.series.models import Episode


class EpisodeRepository(BaseCRUDRepository):
    """Repository for Episode Model"""

    def read_by_series_id(self, series_id: str):
        try:
            episodes = self.db.query(Episode).filter(Episode.series_id == series_id).all()
            return episodes
        except Exception as e:
            self.db.rollback()
            raise e

