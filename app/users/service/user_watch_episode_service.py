from app.db import SessionLocal
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository


class UserWatchEpisodeServices:

    @staticmethod
    def user_watch_episode(user_id: str, episode_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                if watched_episode:
                    return {"message": "Watch episode again."}
                fields = {"user_id": user_id, "episode_id": episode_id}
                repository.create(fields)
                return {"message": "Watch this episode now."}
        except Exception as e:
            raise e

    @staticmethod
    def rate_episode(user_id: str, episode_id: str, rating: int):
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                if watched_episode:
                    obj = repository.update(watched_episode, {"rating": rating})
                    return obj
                else:
                    fields = {"user_id": user_id, "episode_id": episode_id, "rating": rating}
                    return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_my_watched_series_episodes_list(user_id: str, series_id):
        pass
