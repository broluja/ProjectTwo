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
                movie_repo = MovieRepository(db, Movie)
                movie = movie_repo.read_by_id(movie_id)
                watched_movie = repository.read_user_watch_movie_by_user_id_and_movie_id(user_id, movie_id)
                if watched_movie:
                    return {"message": "Watch movie again.", "link": movie.link}
                fields = {"user_id": user_id, "movie_id": movie_id}
                repository.create(fields)
                return {"message": "Watch this movie now.", "link": movie.link}
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

    @staticmethod
    def get_popular_movies():
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                movies = repository.read_movie_downloads()
                movie_repo = MovieRepository(db, Movie)
                response = {}
                for movie_id, views in movies[:10]:
                    movie = movie_repo.read_by_id(movie_id)
                    response.update({movie.title: views})
                return response
        except Exception as e:
            raise e

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        try:
            with SessionLocal() as db:
                movie_repo = MovieRepository(db, Movie)
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                movie = repository.read_movies_by_rating(best)
                response = []
                for movie_id, rating in movie:
                    movie = movie_repo.read_by_id(movie_id)
                    response.append({movie.title: rating})
                return response
        except Exception as e:
            raise e
