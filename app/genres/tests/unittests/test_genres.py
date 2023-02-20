import pytest

from sqlalchemy.exc import IntegrityError
from app.tests import TestClass, TestingSessionLocal
from app.genres.repositories import GenreRepository
from app.genres.models import Genre


class TestGenreRepo(TestClass):

    @staticmethod
    def create_genres_for_methods():
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre_repository.create({"name": "Action"})
            genre_repository.create({"name": "SciFi"})
            genre_repository.create({"name": "Comedy"})

    def test_create_genre(self):
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre = genre_repository.create({"name": "Thriller"})
            assert genre.name == "Thriller"

    def test_create_genre_error(self):
        self.create_genres_for_methods()
        with pytest.raises(IntegrityError):
            with TestingSessionLocal() as db:
                genre_repository = GenreRepository(db, Genre)
                genre_repository.create({"name": "Action"})

    def test_read_genre_by_name(self):
        self.create_genres_for_methods()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genre = genre_repository.read_genres_by_name("Action", search=False)
        assert genre.name == "Action"

    def test_search_genre_by_name(self):
        self.create_genres_for_methods()
        with TestingSessionLocal() as db:
            genre_repository = GenreRepository(db, Genre)
            genres = genre_repository.read_genres_by_name("a", search=True)
        assert isinstance(genres, list)
        assert len(genres) == 1
