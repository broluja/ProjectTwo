"""Test Genre module"""
import pytest

from sqlalchemy.exc import IntegrityError
from app.tests import TestClass, TestingSessionLocal
from app.genres.repositories import GenreRepository
from app.genres.models import Genre


class TestGenreRepo(TestClass):
    """Test Genre functionalities"""
    @staticmethod
    def create_genres_for_methods():
        """
        Function creates three genres in the database.

        Return: A list of genre objects.
        """
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre_repository.create({"name": "Action"})
            genre_repository.create({"name": "SciFi"})
            genre_repository.create({"name": "Comedy"})

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
        self.create_genres_for_methods()
        with pytest.raises(IntegrityError):
            with TestingSessionLocal() as db:
                genre_repository = GenreRepository(db, Genre)
                genre_repository.create({"name": "Action"})

    def test_read_genre_by_name(self):
        """
        Function tests retrieving genres from Database by name.
        Return: Genre object.
        """
        self.create_genres_for_methods()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre = genre_repository.read_genres_by_name("Action", search=False)

        assert genre.name == "Action"

    def test_search_genre_by_name(self):
        """
        Function creates a genre with the name &quot;a&quot; and then searches for it by name.
        It asserts that the search returns one result, which is true because
        there is only one genre with that name.

        Param self: Access the class instance inside a method
        Return: A list of genre objects that match the search query.
        """
        self.create_genres_for_methods()
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
        self.create_genres_for_methods()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genres = genre_repository.read_all()

        assert isinstance(genres, list)
        assert len(genres) == 3
