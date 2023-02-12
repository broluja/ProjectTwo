from sqlalchemy.sql.functions import count

from app.base import BaseCRUDRepository
from app.users.models.user import UserWatchMovie


class UserWatchMovieRepository(BaseCRUDRepository):
    """Repository for UserWatchMovie Model"""

    def read_user_watch_movie_by_user_id_and_movie_id(self, user_id: str, movie_id: str):
        try:
            user_watch_movie = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).filter(
                UserWatchMovie.movie_id == movie_id).first()
            return user_watch_movie
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movies_from_user(self, user_id: str):
        try:
            user_watch_movies = self.db.query(UserWatchMovie).filter(UserWatchMovie.user_id == user_id).all()
            return user_watch_movies
        except Exception as e:
            self.db.rollback()
            raise e

    def read_movie_downloads(self):
        try:
            movie_downloads = self.db.query(UserWatchMovie.movie_id, count()).group_by(UserWatchMovie.movie_id)
            return movie_downloads
        except Exception as e:
            self.db.rollback()
            raise e
