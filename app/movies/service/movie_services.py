from app.directors.exceptions.director_exceptions import NonExistingDirectorException
from app.directors.models import Director
from app.directors.repositories import DirectorRepository
from app.genres.exceptions.genre_exceptions import NonExistingGenreException
from app.genres.models import Genre
from app.genres.repositories import GenreRepository
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
    def get_all_movies(page: int):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                skip = (page - 1) * PER_PAGE
                movies = repository.read_many(skip=skip, limit=PER_PAGE)
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

    @staticmethod
    def search_movies_by_genre(genre: str):
        try:
            with SessionLocal() as db:
                genre_repo = GenreRepository(db, Genre)
                obj = genre_repo.read_genres_by_name(genre, search=False)
                if not obj:
                    raise NonExistingGenreException(message=f"No movies with genre: {genre}")
                repository = MovieRepository(db, Movie)
                movies = repository.read_all()
                response = [movie for movie in movies if movie.genre_id == obj.id]
                return response
        except Exception as e:
            raise e

    @staticmethod
    def get_latest_features(date_limit: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movies = repository.read_latest_releases(date_limit)
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def show_least_popular_movies():
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                movies = repository.read_unpopular_movies()
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def update_movie_data(movie_id: str, attributes: dict):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                obj = repository.read_by_id(movie_id)
                movie = repository.update(obj, attributes)
                return movie
        except Exception as e:
            raise e

    @staticmethod
    def delete_movie(movie_id: str):
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.delete(movie_id)
        except Exception as e:
            raise e
