"""Movie Service module"""
from datetime import date

from app.config import settings
from app.directors.exceptions.director_exceptions import NonExistingDirectorException
from app.directors.models import Director
from app.directors.repositories import DirectorRepository
from app.genres.exceptions.genre_exceptions import NonExistingGenreException
from app.genres.models import Genre
from app.genres.repositories import GenreRepository
from app.movies.exceptions import NoMoviesFromDirectorException
from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.db import SessionLocal


PER_PAGE = settings.PER_PAGE


class MovieServices:
    """Service for movie routes"""
    @staticmethod
    def create_new_movie(title: str, description: str, year_published: str, director_id: str, genre_id: str):
        """
        Function creates a new movie in the database.
        It takes as input the title, year_published, director_id and genre_id of the movie to be created.
        The function returns a dictionary with information about the newly created movie.

        Param title:str: Store the title of the movie
        Param description:str: Store the description of the movie
        Param year-published:str: Store the year in which the movie was published
        Param director_id:str: Store the ID of the director that created this movie
        Param genre_id:str: Specify, which genre the movie belongs to
        Return: The newly created movie object.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                fields = {"title": title,
                          "description": description,
                          "date_added": date.today(),
                          "year_published": year_published,
                          "director_id": director_id,
                          "genre_id": genre_id}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_all_movies(page: int):
        """
        Function returns a list of all movies in the database.
        The function accepts an optional page parameter, which allows you to specify,
        which 'page' of results you want returned. The default page is 1.

        Param page:int: Specify the page number of the movies to be returned
        Return: A list of movies.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                skip = (page - 1) * PER_PAGE
                return repository.read_many(skip=skip, limit=PER_PAGE)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_movie_by_id(movie_id: str):
        """
        Function is used to retrieve a movie by its ID.
        It takes in the movie_id as an argument and returns the movie object.

        Param movie_id:str: Pass the ID of the movie that we want to get from the database.
        Return: A movie object.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.read_by_id(movie_id)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_movie_by_title(title: str):
        """
        Function takes a movie title as an argument and returns the movie object associated with that title.

        Param title:str: Search for a movie by title
        Return: A movie object.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.read_movie_by_title(title)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_movies_by_name(title: str):
        """
        Function searches for movies by title.
        It takes a string as an argument and returns a list of movie objects.

        Param title:str: Search for a movie by its title.
        Return: A list of movies that match the title passed to it.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.read_movie_by_title(title, search=True)
        except Exception as exc:
            raise exc

    @staticmethod
    def search_movies_by_director_first_name(first_name: str):
        try:
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                response = director_repo.read_directors_by_first_name(first_name, search=False)
                if not response:
                    raise NonExistingDirectorException(message=f"No movies by director: '{first_name}'")
                repository = MovieRepository(db, Movie)
                movies = repository.read_movies_by_director_ids([director.id for director in response])
                if not movies:
                    raise NoMoviesFromDirectorException
                return movies
        except Exception as exc:
            raise exc

    @staticmethod
    def search_movies_by_director_last_name(director: str):
        """
        Function searches for all movies by a given director.
        It takes in the name of the director as an argument and returns a list of Movie objects.

        Param director:str: Search for movies by the director's last name.
        Return: A list of movie objects.
        """
        try:
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                response = director_repo.read_directors_by_last_name(director, search=False)
                if not response:
                    raise NonExistingDirectorException(message=f"No movies by director: '{director}'")
                repository = MovieRepository(db, Movie)
                movies = repository.read_movies_by_director_ids([director.id for director in response])
                if not movies:
                    raise NoMoviesFromDirectorException
                return movies
        except Exception as exc:
            raise exc

    @staticmethod
    def search_movies_by_director_full_name(full_name: str):
        try:
            first_name = " ".join(full_name.split()[:-1])
            last_name = full_name.split()[-1]
            with SessionLocal() as db:
                director_repo = DirectorRepository(db, Director)
                director = director_repo.read_director_by_full_name(first_name, last_name)
                if not director:
                    raise NonExistingDirectorException(message=f"No movies by director: '{full_name}'")
                repository = MovieRepository(db, Movie)
                movies = repository.read_movies_by_director_id(director.id)
                if not movies:
                    raise NoMoviesFromDirectorException
                return movies
        except Exception as exc:
            raise exc

    @staticmethod
    def search_movies_by_genre(genre: str):
        """
        Function searches for movies by a genre.
        It takes a string as an argument and returns a list of movie objects that match the genre.

        Param genre:str: Search for movies with a specific genre.
        Return: A list of movies that have the genre passed as a parameter.
        """
        try:
            with SessionLocal() as db:
                genre_repo = GenreRepository(db, Genre)
                obj = genre_repo.read_genres_by_name(genre, search=False)
                if not obj:
                    raise NonExistingGenreException(message=f"No movies with genre: {genre}")
                repository = MovieRepository(db, Movie)
                movies = repository.read_all()
                return [movie for movie in movies if movie.genre_id == obj.id]
        except Exception as exc:
            raise exc

    @staticmethod
    def get_movies_by_year(year: int):
        """
        Function returns a list of movies that were released in the given year.
        The function accepts one argument, year, which is an integer representing the release year of the movie.

        Param year:int: Filter the movies by a year.
        Return: A list of movies for a given year.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                return movie_repository.read_movies_by_year(str(year))
        except Exception as exc:
            raise exc

    @staticmethod
    def get_latest_features(date_limit: str):
        """
        Function returns a list of movies that were released after the date limit.
        The date limit is passed in as an argument to the function, and it should be formatted as YYYY-MM-DD.

        Param date_limit:str: Filter the results by date.
        Return: A list of dictionaries.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.read_latest_releases(date_limit)
        except Exception as exc:
            raise exc

    @staticmethod
    def show_least_popular_movies():
        """
        Function returns a list of movies that have been rated the least amount of times.

        Return: A list of movies that have a rating less than 3.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.read_unpopular_movies()
        except Exception as exc:
            raise exc

    @staticmethod
    def update_movie_data(movie_id: str, attributes: dict):
        """
        Function updates a movie's data.

        Param movie_id:str: Identify the movie to be updated.
        Param attributes:dict: Update the movie with the given ID.
        Return: The updated movie object.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                obj = repository.read_by_id(movie_id)
                return repository.update(obj, attributes)
        except Exception as exc:
            raise exc

    @staticmethod
    def delete_movie(movie_id: str):
        """
        Function deletes a movie from the database.
        It takes in a movie_id as an argument and returns the deleted Movie object.

        Param movie_id:str: Identify the movie to be deleted.
        Return: A dictionary with a success message.
        """
        try:
            with SessionLocal() as db:
                repository = MovieRepository(db, Movie)
                return repository.delete(movie_id)
        except Exception as exc:
            raise exc
