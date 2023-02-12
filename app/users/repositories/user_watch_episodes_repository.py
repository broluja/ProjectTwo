from app.base import BaseCRUDRepository
from app.users.models.user import UserWatchEpisode


class UserWatchEpisodeRepository(BaseCRUDRepository):
    """Repository for UserWatchEpisode Model"""

    def read_user_watch_episode_by_user_id_and_episode_id(self, user_id: str, episode_id: str):
        try:
            user_watch_episode = self.db.query(UserWatchEpisode).filter(UserWatchEpisode.user_id == user_id).filter(
                UserWatchEpisode.episode_id == episode_id).first()
            return user_watch_episode
        except Exception as e:
            self.db.rollback()
            raise e

    def read_by_user_id(self, user_id: str):
        try:
            episodes = self.db.query(UserWatchEpisode).filter(UserWatchEpisode.user_id == user_id).all()
            return episodes
        except Exception as e:
            self.db.rollback()
            raise e
