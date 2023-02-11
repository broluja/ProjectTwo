from app.db import SessionLocal
from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.users.models.user import UserWatchMovie
from app.users.repositories import UserWatchMovieRepository


class UserWatchMovieServices:

    @staticmethod
    def user_watch_movie(user_id: str, movie_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                watched_movie = repository.read_user_watch_movie_by_user_id_and_movie_id(user_id, movie_id)
                print(watched_movie)
                if watched_movie:
                    return {"message": "Watch movie again."}
                fields = {"user_id": user_id, "movie_id": movie_id}
                repository.create(fields)
                return {"message": "Watch this movie now."}
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

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                objects = repository.read_movies_from_user(user_id)
                movie_ids = [obj.movie_id for obj in objects]
                movie_repo = MovieRepository(db, Movie)
                movie_objects = [movie_repo.read_by_id(movie_id) for movie_id in movie_ids]
                return movie_objects
        except Exception as e:
            raise e
