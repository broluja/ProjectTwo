"""UserWatchMovie Service module"""
from starlette.responses import Response

from app.db import SessionLocal
from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.users.models.user import UserWatchMovie
from app.users.repositories import UserWatchMovieRepository


class UserWatchMovieServices:
    """Service for UserWatchMovie routes."""
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
        except Exception as exc:
            raise exc

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
        except Exception as exc:
            raise exc

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                objects = repository.read_movies_from_user(user_id)
                if not objects:
                    return Response(content="You have not watched any Movie yet.", status_code=200)
                movie_ids = [obj.movie_id for obj in objects]
                movie_repo = MovieRepository(db, Movie)
                movie_objects = [movie_repo.read_by_id(movie_id) for movie_id in movie_ids]
                return movie_objects
        except Exception as exc:
            raise exc

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
        except Exception as exc:
            raise exc

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        try:
            with SessionLocal() as db:
                movie_repo = MovieRepository(db, Movie)
                user_watch_repo = UserWatchMovieRepository(db, UserWatchMovie)
                movie = user_watch_repo.read_movies_by_rating(best)
                response = []
                for movie_id, rating in movie:
                    movie = movie_repo.read_by_id(movie_id)
                    response.append({movie.title: rating})
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_my_recommendations(user_id, page):
        try:
            with SessionLocal() as db:
                user_watch_movie_repo = UserWatchMovieRepository(db, UserWatchMovie)
                users_affinities = user_watch_movie_repo.read_users_affinities(user_id)
                movies_repo = MovieRepository(db, Movie)
                genres = [affinity.Genre_ID for affinity in users_affinities]
                return movies_repo.read_movies_by_group_of_genres(page, genres)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_rating_for_movie(name: str):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                movie = movie_repository.read_movie_by_title(name, search=False)
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                average = user_watch_movie_repository.read_average_rating(movie.id)
                response = {"Movie": movie.title}
                response.update(average)
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_ratings():
        try:
            with SessionLocal() as db:
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                response = user_watch_movie_repository.read_average_rating_for_all_movies()
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_movies_with_higher_average_rating(rating: float):
        try:
            with SessionLocal() as db:
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                ratings = user_watch_movie_repository.read_average_rating_for_all_movies()
                response = [movie for movie in ratings if movie["Average Rating"] and movie["Average Rating"] > rating]
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_movie_rating_for_year(year: int):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                movies = movie_repository.read_movies_by_year(str(year))
                if not movies:
                    return Response(content=f"No Movies from this year: {year}", status_code=200)
                movie_ids = [movie.id for movie in movies]
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                ratings = user_watch_movie_repository.read_average_rating_for_movies(movie_ids)
                all_ratings = [rating["Average Rating"] for rating in ratings]
                response = {f"Average rating for year: {year}": round(sum(all_ratings) / len(all_ratings), 2)}
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_most_successful_movie_year():
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                query = movie_repository.read_movie_years()
                years = [obj.year_published for obj in query]
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                response = {}
                for year in years:
                    movies = movie_repository.read_movies_by_year(year)
                    ids = [movie.id for movie in movies]
                    ratings = user_watch_movie_repository.read_average_rating_for_movies(movie_ids=ids)
                    all_ratings = [rating["Average Rating"] for rating in ratings if rating["Average Rating"]]
                    avg_rating = round(sum(all_ratings) / len(all_ratings), 2) if all_ratings else None
                    if avg_rating:
                        response.update({year: avg_rating})
                return response
        except Exception as exc:
            raise exc
