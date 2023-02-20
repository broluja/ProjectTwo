from app.tests import TestClass, TestingSessionLocal
from app.genres.repositories import GenreRepository
from app.genres.models import Genre


class TestGenreRepo(TestClass):

    def create_genres_for_methods(self):
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
