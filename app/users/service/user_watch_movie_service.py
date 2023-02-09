from app.db import SessionLocal
from app.users.models.user import UserWatchMovie
from app.users.repositories import UserWatchMovieRepository


class UserWatchMovieServices:

    @staticmethod
    def user_watch_movie(user_id: str, movie_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                fields = {"user_id": user_id, "movie_id": movie_id}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def rate_movie(user_id: str, movie_id: str, rating: int):
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                watched_movie = repository.read_user_watch_movie_by_user_id_and_movie_id(user_id, movie_id)
                if watched_movie:
                    obj = repository.update(watched_movie, {"rating": rating})
                    return obj
                else:
                    fields = {"user_id": user_id, "movie_id": movie_id, "rating": rating}
                    return repository.create(fields)
        except Exception as e:
            raise e
