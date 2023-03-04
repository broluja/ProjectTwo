"""Movie Controller module"""
from fastapi import HTTPException
from starlette.responses import Response, JSONResponse

from app.base import AppException
from app.movies.service import MovieServices
from app.directors.service import DirectorServices
from app.genres.service import GenreServices


class MovieController:
    """Controller for movie routes"""
    @staticmethod
    def create_movie(title: str, description: str, year_published: str, director_id: str, genre_id: str):
        """
        Function creates a new movie object and returns it.
        It takes in the title, year_published, director_id, and genre_id as parameters.
        It then uses these parameters to create a new Movie object with the given information.
        The function then returns this newly created Movie object.

        Param title:str: Specify the title of the movie
        Param description:str: Store the description of the movie
        Param year published:str: Store the year when the movie was published
        Param director_id:str: Get the director object from the database
        Param genre_id:str: Get the genre object from the database
        Return: A movie object.
        """
        try:
            director = DirectorServices.get_director_by_id(director_id)
            genre = GenreServices.get_genre_by_id(genre_id)
            movie = MovieServices.create_new_movie(title, description, year_published, director_id, genre_id)
            movie.director = director
            movie.genre = genre
            return movie
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_movies(page: int):
        """
        Function returns all movies in the database.
        The function takes one argument, page, which specifies the page of results to return.
        If there are no more pages of results left, it will return an empty list.

        Param page:int: Specify the page number of the movies to be returned
        Return: A list of movies, or a message stating that there are no more movies to return.
        """
        try:
            movies = MovieServices.get_all_movies(page)
            return movies if movies else Response(content="End of query.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_data(title: str):
        """
        Function takes a movie title as an argument and returns the data for that movie.
        It first checks to see if the movie exists in the database, and if it does not, raises an exception.
        If it does exist, then it gets all of its data from the database (genre name, director name) and returns it.

        Param title:str: Get the movie by title.
        Return: A movie object.
        """
        try:
            movie = MovieServices.get_movie_by_title(title)
            genre = GenreServices.get_genre_by_id(movie.genre_id)
            director = DirectorServices.get_director_by_id(movie.director_id)
            movie.genre = genre
            movie.director = director
            return movie
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movie_by_id(movie_id: str):
        """
        Function is used to retrieve a movie by its ID.
        It takes in the movie_id as an argument and returns the corresponding Movie object.

        Param movie_id:str: Specify the movie_id of the movie that is to be retrieved
        Return: A movie object.
        """
        try:
            return MovieServices.get_movie_by_id(movie_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_movies_by_name(title: str):
        """
        Function searches for movies by name in our database.
        It returns a list of movie objects if there are any matches, otherwise it returns an empty list.

        Param title:str: Search for a movie by title.
        Return: A list of movies that match the title.
        """
        try:
            movies = MovieServices.search_movies_by_name(title)
            return movies if movies else Response(
                content=f"No Movie with title: {title} in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_movies_by_director_first_name(first_name: str):
        try:
            movies = MovieServices.search_movies_by_director_first_name(first_name)
            return movies if movies else JSONResponse(
                content=f"No Movie from Director: '{first_name}' in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_movies_by_director_last_name(director: str):
        """
        Function searches for movies by a given director.
        It takes in a string representing the name of the director and returns all movies from that director.
        If no movie is found, it returns an error message.

        Param director:str: Search for movies by a specific director.
        Return: A list of movies from the given director.
        """
        try:
            movies = MovieServices.search_movies_by_director_last_name(director)
            return movies if movies else JSONResponse(
                content=f"No Movie from Director: '{director}' in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_movies_by_director_full_name(full_name: str):
        try:
            movies = MovieServices.search_movies_by_director_full_name(full_name)
            return movies if movies else JSONResponse(
                content=f"No movies in Database from director '{full_name}'",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def search_movies_by_genre(genre: str):
        """
        Function searches for movies with a specific genre.
        It takes in a string as an argument and returns the list of movies that match the genre.

        Param genre:str: Search for movies with the given genre
        Return: A list of movies that have the genre passed in as a parameter.
        """
        try:
            movies = MovieServices.search_movies_by_genre(genre)
            return movies if movies else Response(
                content=f"No Movie with genre: {genre} in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_movies_by_year(year: int):
        """
        Function returns a list of movies from the given year.
        If no movies are found, it will return an empty list.

        Param year:int: Filter the movies by year
        Return: A list of movies from a given year.
        """
        try:
            movies = MovieServices.get_movies_by_year(year)
            return movies if movies else Response(
                content=f"No Movie from year: {year} in our Database.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_latest_features(date_limit: str):
        """
        Function returns a list of movies that are in the latest list.
        The date-limit parameter is used to filter out movies that were released before this date.
        If no movies are found, an empty array is returned.

        Param date_limit:str: Limit the amount of movies returned
        Return: A list of movies that are in the latest list.
        """
        try:
            movies = MovieServices.get_latest_features(date_limit)
            return movies if movies else Response(content="No movies in latest list.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_movie_data(movie_id: str, attributes: dict):
        """
        Function updates the movie data for a given movie ID.
        It takes in a string representing the ID of the movie to be updated, and a dictionary containing
        the attributes to be updated. It returns an object that represents the newly updated Movie.

        Param movie_id:str: Identify the movie to be updated
        Param attributes:dict: Update the movie data
        Return: The updated movie data.
        """
        try:
            return MovieServices.update_movie_data(movie_id, attributes)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_movie(movie_id: str):
        """
        Function deletes a movie from the database.
        It takes in a movie_id as an argument and returns the deleted movie with that ID.

        Param movie_id:str: Identify the movie to be deleted.
        Return: A response object.
        """
        try:
            MovieServices.delete_movie(movie_id)
            return Response(content=f"Movie with ID: {movie_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def show_least_popular_movies():
        """
        Function returns a list of movies that have been downloaded the least amount of times.
        The function takes no arguments and returns a list of dictionaries, each dictionary representing one movie.

        Return: A list of movies that have never been downloaded.
        """
        try:
            movies = MovieServices.show_least_popular_movies()
            return movies if movies else Response(
                content="There are no movies that never have been downloaded.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
