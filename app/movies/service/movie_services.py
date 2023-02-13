from app.directors.exceptions.director_exceptions import NonExistingDirectorException
from app.directors.models import Director
from app.directors.repositories import DirectorRepository
from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.db import SessionLocal

from datetime import date

PER_PAGE = 5


class MovieServices:

    @staticmethod
    def create_new_movie(title: str, year_published: str, director_id: str, genre_id: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                fields = {"title": title,
                          "date_added": date.today(),
                          "year_published": year_published,
                          "director_id": director_id,
                          "genre_id": genre_id}
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

    @staticmethod
    def get_movie_by_title(title: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movie = repository.read_movie_by_title(title)
                return movie
        except Exception as e:
            raise e

    @staticmethod
    def search_movies_by_name(title: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movies = repository.read_movie_by_title(title, search=True)
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def search_movies_by_director(director: str):
        try:
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                obj = director_repo.read_directors_by_last_name(director, search=False)
                if not obj:
                    raise NonExistingDirectorException(message=f"No movies by director: {director}")
                repository = MovieRepository(db, Movie)
                movies = repository.read_all()
                response = [movie for movie in movies if movie.director_id == obj.id]
                return response
        except Exception as e:
            raise e

