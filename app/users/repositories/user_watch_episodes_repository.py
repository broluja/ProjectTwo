from app.base import BaseCRUDRepository
from app.users.models.user import UserWatchEpisode


class UserWatchEpisodeRepository(BaseCRUDRepository):
    """Repository for UserWatchEpisode Model"""

    def read_by_user_id(self, user_id: str):
        try:
            episodes = self.db.query(UserWatchEpisode).filter(UserWatchEpisode.user_id == user_id).all()
            return episodes
        except Exception as e:
            self.db.rollback()
            raise e
