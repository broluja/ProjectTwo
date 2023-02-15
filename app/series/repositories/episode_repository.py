from app.base import BaseCRUDRepository
from app.series.models import Episode


class EpisodeRepository(BaseCRUDRepository):
    """Repository for Episode Model"""

    def read_by_series_id(self, series_id: str):
        try:
            episodes = self.db.query(Episode).filter(Episode.series_id == series_id).order_by(Episode.name).all()
            return episodes
        except Exception as e:
            self.db.rollback()
            raise e

    def read_by_episode_name_and_series_id(self, name: str, series_id):
        try:
            episode = self.db.query(Episode).filter(Episode.name == name).filter(Episode.series_id == series_id).first()
            return episode
        except Exception as e:
            self.db.rollback()
            raise e
