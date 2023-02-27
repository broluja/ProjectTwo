"""UserWatchMovie Service module"""
from starlette.responses import Response

from app.db import SessionLocal
from app.movies.models import Movie
from app.movies.repositories import MovieRepository
from app.users.models.user import UserWatchMovie
from app.users.repositories import UserWatchMovieRepository


class UserWatchMovieServices:
    """Service for UserWatchMovie routes."""
    @staticmethod
    def user_watch_movie(user_id: str, movie_id: str):
        """
        Function allows a user to watch a movie.
        It takes in two parameters, the user_id and the movie_id.
        The function then checks if there is an existing record of
        this particular combination of user ID and movie ID.
        If it does not exist, it creates one with the given information.

        Param user_id:str: Identify the user.
        Param movie_id:str: Get the movie object from the database.
        Return: A dictionary with two keys.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                movie_repo = MovieRepository(db, Movie)
                movie = movie_repo.read_by_id(movie_id)
                watched_movie = repository.read_user_watch_movie_by_user_id_and_movie_id(user_id, movie_id)
                if watched_movie:
                    return {"message": "Watch movie again.", "link": movie.link}
                fields = {"user_id": user_id, "movie_id": movie_id}
                repository.create(fields)
                return {"message": "Watch this movie now.", "link": movie.link}
        except Exception as exc:
            raise exc

    @staticmethod
    def rate_movie(user_id: str, movie_id: str, rating: int):
        """
        Function allows a user to rate a movie.
        It takes in the user_id, movie_id and rating as parameters.
        The function then checks if the user has already rated that particular movie.
        If they have not, it creates a new entry in the UserWatchMovie table with their rating for that specific film.

        Param user_id:str: Identify the user.
        Param movie_id:str: Specify the movie that is being rated.
        Param rating:int: Set the rating of a movie.
        Return: The user-watch-movie object that was created or updated.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                watched_movie = repository.read_user_watch_movie_by_user_id_and_movie_id(user_id, movie_id)
                if watched_movie:
                    obj = repository.update(watched_movie, {"rating": rating})
                    return obj
                fields = {"user_id": user_id, "movie_id": movie_id, "rating": rating}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_my_watched_movies_list(user_id: str):
        """
        Function returns a list of movies that the user has watched.
        It takes in a string representing the user_id and returns a list of movie objects.

        Param user_id:str: Pass the user_id of the logged-in user to the function.
        Return: A list of movie objects.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                objects = repository.read_movies_from_user(user_id)
                if not objects:
                    return Response(content="You have not watched any Movie yet.", status_code=200)
                movie_ids = [obj.movie_id for obj in objects]
                movie_repo = MovieRepository(db, Movie)
                return [movie_repo.read_by_id(movie_id) for movie_id in movie_ids]
        except Exception as exc:
            raise exc

    @staticmethod
    def get_popular_movies():
        """
        The get_popular_movies function returns the top 10 most popular movies in the database.
        The function takes no arguments and returns a dictionary of movie titles mapped to their number of views.

        Return: The top 10 most popular movies.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchMovieRepository(db, UserWatchMovie)
                movies = repository.read_movie_downloads()
                movie_repo = MovieRepository(db, Movie)
                response = {}
                for movie_id, views in movies[:10]:
                    movie = movie_repo.read_by_id(movie_id)
                    response[movie.title] = views
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_best_rated_movie(best: bool = True):
        """
        Function returns the best rated movie by users.
        The function takes one parameter, best, which is a boolean value that defaults to True.
        If the user passes in False for this parameter then it will return the worst rated movie.

        Param best:bool=True: Determine whether the function should return the best or worst rated movie.
        Return: A list of dictionaries with the movie title and rating.
        """
        try:
            with SessionLocal() as db:
                movie_repo = MovieRepository(db, Movie)
                user_watch_repo = UserWatchMovieRepository(db, UserWatchMovie)
                movie = user_watch_repo.read_movies_by_rating(best)
                response = []
                for movie_id, rating in movie:
                    movie = movie_repo.read_by_id(movie_id)
                    response.append({movie.title: rating})
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_my_recommendations(user_id, page):
        """
        Function returns a list of movies that are recommended to the user based on their
        affinities. The function takes in two parameters, user_id and page. The page
        parameter is used to paginate the results
        and return only 10 movies at a time. It also takes into account if
        there are no more pages left by checking if there
        are any more records in the database for that particular genre.

        Param user_id: Get the user's affinity for each genre.
        Param page: Paginate the results.
        Return: A list of movies that are recommended to the user.
        """
        try:
            with SessionLocal() as db:
                user_watch_movie_repo = UserWatchMovieRepository(db, UserWatchMovie)
                users_affinities = user_watch_movie_repo.read_users_affinities(user_id)
                movies_repo = MovieRepository(db, Movie)
                genres = [affinity.Genre_ID for affinity in users_affinities]
                return movies_repo.read_movies_by_group_of_genres(page, genres)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_rating_for_movie(name: str):
        """
        Function returns the average rating for a movie.
        It takes in a string name of the movie and returns an object with the title,
        average rating, and number of ratings.

        Param name:str: Pass the name of the movie to be searched.
        Return: The average rating for a movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                movie = movie_repository.read_movie_by_title(name, search=False)
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                average = user_watch_movie_repository.read_average_rating(movie.id)
                response = {"Movie": movie.title}
                response.update(average)
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_ratings():
        """
        Function returns the average rating for all movies in the database.

        Return: A list of dictionaries containing the movie_id and average rating for all movies.
        """
        try:
            with SessionLocal() as db:
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                return user_watch_movie_repository.read_average_rating_for_all_movies()
        except Exception as exc:
            raise exc

    @staticmethod
    def get_movies_with_higher_average_rating(rating: float):
        """
        Function returns a list of movies with an average rating higher than the specified rating.
        The function takes one argument, which is the minimum average rating that you want returned.

        Param rating:float: Filter the movies based on the average rating.
        Return: A list of movies that have an average rating higher than the rating passed in as a parameter.
        """
        try:
            with SessionLocal() as db:
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                ratings = user_watch_movie_repository.read_average_rating_for_all_movies()
                return [movie for movie in ratings if movie["Average Rating"] and movie["Average Rating"] > rating]
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_movie_rating_for_year(year: int):
        """
        Function returns the average rating for all movies in a given year.
        The function takes one argument, year, which is an integer representing the desired year to search for.
        If no movies are found from that particular year then it will return 'No Movies from this Year'.

        Param year:int: Specify the year of the movies that will be used to calculate the average rating.
        Return: The average rating for all movies from a given year.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                movies = movie_repository.read_movies_by_year(str(year))
                if not movies:
                    return Response(content=f"No Movies from this year: {year}", status_code=200)
                movie_ids = [movie.id for movie in movies]
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                ratings = user_watch_movie_repository.read_average_rating_for_movies(movie_ids)
                all_ratings = [rating["Average Rating"] for rating in ratings]
                return {f"Average rating for year: {year}": round(sum(all_ratings) / len(all_ratings), 2)}
        except Exception as exc:
            raise exc

    @staticmethod
    def get_most_successful_movie_year():
        """
        Function returns the year with the highest average rating.
        It takes no arguments and returns a dictionary of years mapped to their average ratings.

        Return: A dictionary with the year as key and average rating as value.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db, Movie)
                query = movie_repository.read_movie_years()
                years = [obj.year_published for obj in query]
                user_watch_movie_repository = UserWatchMovieRepository(db, Movie)
                response = {}
                for year in years:
                    movies = movie_repository.read_movies_by_year(year)
                    ids = [movie.id for movie in movies]
                    ratings = user_watch_movie_repository.read_average_rating_for_movies(movie_ids=ids)
                    all_ratings = [rating["Average Rating"] for rating in ratings if rating["Average Rating"]]
                    avg_rating = round(sum(all_ratings) / len(all_ratings), 2) if all_ratings else None
                    if avg_rating:
                        response[year] = avg_rating
                return response
        except Exception as exc:
            raise exc
