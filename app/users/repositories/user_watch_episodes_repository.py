from sqlalchemy import select, distinct, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import count

from app.base import BaseCRUDRepository
from app.series.models import Episode, Series
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

    def read_users_episodes_and_series(self, user_id: str):
        try:
            series = self.db.query(UserWatchEpisode, Episode.series_id, Series.title) \
                .join(Episode, Episode.id == UserWatchEpisode.episode_id) \
                .join(Series, Episode.series_id == Series.id) \
                .filter(UserWatchEpisode.user_id == user_id).all()
            return series
        except Exception as e:
            self.db.rollback()
            raise e

    def read_episode_views(self):
        try:
            subquery = self.db.query(UserWatchEpisode.user_id.label('user'),
                                     UserWatchEpisode.episode_id.label('episode'), Episode.series_id.label('series')) \
                .join(Episode, Episode.id == UserWatchEpisode.episode_id).subquery('sq')
            sq = aliased(subquery)
            subquery2 = self.db.query(sq.c.user, sq.c.series.label('series_two')).distinct().subquery('sq2')
            sq2 = aliased(subquery2)
            result = self.db.query(sq2.c.series_two, func.count(sq2.c.series_two)).group_by(sq2.c.series_two)
            return result
        except Exception as e:
            self.db.rollback()
            raise e

    def read_best_rated_episode(self, best: bool = True):
        try:
            if best:
                subquery = self.db.query(UserWatchEpisode.episode_id.label("episode"),
                                         func.avg(UserWatchEpisode.rating).label("rating")).group_by(
                    UserWatchEpisode.episode_id.label("episode")).subquery()
                max_rating = self.db.query(func.max(subquery.c.rating.label("rating")))
                episode = self.db.query(subquery.c.episode.label("episode"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == max_rating)
            else:
                subquery = self.db.query(UserWatchEpisode.episode_id.label("episode"),
                                         func.avg(UserWatchEpisode.rating).label("rating")).group_by(
                    UserWatchEpisode.episode_id.label("episode")).subquery()
                min_rating = self.db.query(func.min(subquery.c.rating.label("rating")))
                episode = self.db.query(subquery.c.episode.label("episode"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == min_rating)
            return episode
        except Exception as e:
            self.db.rollback()
            raise e
