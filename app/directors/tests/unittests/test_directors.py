"""Test Director module"""
from app.tests import TestClass, TestingSessionLocal
from app.directors.repositories import DirectorRepository
from app.directors.models import Director


class TestDirectorRepo(TestClass):
    """Test Director functionalities."""
    director = None

    def create_director(self):
        """
        Function creates a director in the database.
        It takes no arguments and returns a dictionary of the attributes of the created director.

        Return: The director object.
        """
        with TestingSessionLocal() as db:
            director_repository = DirectorRepository(db, Director)
            attributes = {"first_name": "John",
                          "last_name": "Carpenter",
                          "country": "USA"}
            self.director = director_repository.create(attributes)

    def test_create_director(self):
        """
        Function creates a director object and tests whether the first_name, last_name,
        and country attributes are equal to 'John', 'Carpenter', and 'USA' respectively.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        assert self.director.first_name == "John"
        assert self.director.last_name == "Carpenter"
        assert self.director.country == "USA"

    def test_get_all_directors(self):
        """
        Function tries to get all directors from database after creating one.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            director_repository = DirectorRepository(db, Director)
            directors = director_repository.read_all()

        assert directors[0].first_name == "John"
        assert directors[0].last_name == "Carpenter"
        assert directors[0].country == "USA"
        assert len(directors) == 1

    def test_update_director(self):
        """
        Function tests director update.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            repository.update(self.director, {"country": "UK"})

        assert self.director.country == "UK"
        assert self.director.first_name == "John"
        assert self.director.last_name == "Carpenter"

    def test_delete_director(self):
        """
        Function tests deletion of director.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            repository.delete(self.director.id)
            directors = repository.read_all()

        assert len(directors) == 0

    def test_get_director_by_id(self):
        """
        Function tests reading director by ID.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            director = repository.read_by_id(self.director.id)

        assert director.first_name == self.director.first_name
        assert director.last_name == self.director.last_name
        assert director.country == self.director.country

    def test_search_director_by_first_name(self):
        """
        Function tests searching director by first name.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            director = repository.read_directors_by_first_name("Jo", search=True)

        assert director[0].first_name == self.director.first_name
        assert director[0].last_name == self.director.last_name
        assert director[0].country == self.director.country

    def test_search_director_by_last_name(self):
        """
        Function tests searching director by last name.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            director = repository.read_directors_by_last_name("Car", search=True)

        assert director[0].first_name == self.director.first_name
        assert director[0].last_name == self.director.last_name
        assert director[0].country == self.director.country

    def test_search_director_by_full_name(self):
        """
        Function tests searching director by full name.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            director = repository.read_director_by_full_name("John", "Carpenter")

        assert director.first_name == self.director.first_name
        assert director.last_name == self.director.last_name
        assert director.country == self.director.country

    def test_search_director_by_country(self):
        """
        Function tests searching director by country.

        Return: The director object, which is then used to assert the
        first name, last name and country of the director.
        """
        self.create_director()
        with TestingSessionLocal() as db:
            repository = DirectorRepository(db, Director)
            director = repository.read_directors_by_country("USA")

        assert director[0].first_name == self.director.first_name
        assert director[0].last_name == self.director.last_name
        assert director[0].country == self.director.country
