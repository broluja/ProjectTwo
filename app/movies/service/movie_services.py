from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.db import SessionLocal

from datetime import date


class MovieServices:

    @staticmethod
    def create_new_movie(title: str, year_published: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                fields = {"title": title,
                          "date_added": date.today(),
                          "year_published": year_published}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_movies():
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movies = repository.read_all()
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def get_movie_by_id(movie_id: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movie = repository.read_by_id(movie_id)
                return movie
        except Exception as e:
            raise e
