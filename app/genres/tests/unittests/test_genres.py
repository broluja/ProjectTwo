"""Test Genre module"""
import pytest

from sqlalchemy.exc import IntegrityError

from app.base import AppException
from app.tests import TestClass, TestingSessionLocal
from app.genres.repositories import GenreRepository
from app.genres.models import Genre


class TestGenreRepo(TestClass):
    """Test Genre functionalities"""
    genre = None

    def create_genres_for_tests(self):
        """
        Function creates three genres in the database.

        Return: A list of genre objects.
        """
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre_repository.create({"name": "SciFi"})
            genre_repository.create({"name": "Comedy"})
            genre = genre_repository.create({"name": "Action"})
            self.genre = genre

    def test_create_genre(self):
        """
        Function tests the create method of the GenreRepository class.
        It creates a new genre and asserts that it has been created correctly.

        Param self: Access the class attributes and methods
        Return: A genre object with the name thriller.
        """
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre = genre_repository.create({"name": "Thriller"})

        assert genre.name == "Thriller"

    def test_create_genre_error(self):
        """
        Function tests that the create method of the GenreRepository class raises an IntegrityError
        when a duplicate genre is created.

        Return: A 'integrity-error' exception.
        """
        self.create_genres_for_tests()
        with pytest.raises(IntegrityError):
            with TestingSessionLocal() as db:
                genre_repository = GenreRepository(db, Genre)
                genre_repository.create({"name": "Action"})

    def test_read_genre_by_name(self):
        """
        Function tests retrieving genres from Database by name.
        Return: Genre object.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre = genre_repository.read_genres_by_name("Action", search=False)

        assert genre.name == "Action"

    def test_read_genre_by_id(self):
        """
        Function tests reading genre from Database by its ID.

        Return: Genre object.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            repository = GenreRepository(db, Genre)
            genre = repository.read_by_id(self.genre.id)

        assert genre.name == self.genre.name
        assert genre.id == self.genre.id

    def test_read_genre_by_id_error(self):
        """
        Function tests error on reading genre object by unknown ID.

        Return: AppException error.
        """
        self.create_genres_for_tests()
        with pytest.raises(AppException):
            with TestingSessionLocal() as db:
                repository = GenreRepository(db, Genre)
                ID = self.genre.id
                repository.delete(ID)
                repository.read_by_id(ID)

    def test_search_genre_by_name(self):
        """
        Function creates a genre with the name &quot;a&quot; and then searches for it by name.
        It asserts that the search returns one result, which is true because
        there is only one genre with that name.

        Param self: Access the class instance inside a method
        Return: A list of genre objects that match the search query.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genres = genre_repository.read_genres_by_name("a", search=True)

        assert isinstance(genres, list)
        assert len(genres) == 1
        assert genres[0].name == "Action"

    def test_read_all_genres(self):
        """
        Function tests reading all tests from Database.
        Return: A list of genres.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genres = genre_repository.read_all()

        assert isinstance(genres, list)
        assert len(genres) == 3

    def test_update_genre(self):
        """
        Function tests update of Genre object.

        Return : Genre object.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            repository = GenreRepository(db, Genre)
            obj = repository.update(self.genre, {"name": "Test Genre"})

        assert self.genre.name == obj.name
        assert self.genre.id == obj.id

    def test_delete_genre(self):
        """
        Function tests deletion of Genre.

        Return: None.
        """
        self.create_genres_for_tests()
        with TestingSessionLocal() as db:
            repository = GenreRepository(db, Genre)
            repository.delete(self.genre.id)
            genres = repository.read_all()

        assert isinstance(genres, list)
        assert len(genres) == 2
        assert "Action" not in (genre.name for genre in genres)
