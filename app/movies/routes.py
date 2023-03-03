"""Movie and Movie-Actor routes"""
from fastapi import APIRouter, Depends, status, HTTPException, Body
from starlette.requests import Request

from app.movies.controller import MovieController, MovieActorController
from app.movies.schemas import *
from app.users.controller import UserWatchMovieController, JWTBearer
from app.users.schemas.user_watch_movie_schema import UserWatchMovieSchema
from app.utils import get_day_before_one_month

movie_router = APIRouter(tags=["Movies"], prefix="/api/movies")


@movie_router.post("/",
                   response_model=MovieWithDirectorAndGenreSchema,
                   summary="Add new Movie to Database. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def add_new_movie(movie: MovieSchemaIn):
    """
    Function creates a new movie in the database.
    It takes as input a MovieSchemaIn object, which is used to create the new movie.
    The function returns an updated MovieSchemaOut object.

    Param movie:MovieSchemaIn: Pass the movie object to the function.
    Return: The movie that was created.
    """
    return MovieController.create_movie(**vars(movie))


@movie_router.get("/",
                  response_model=list[MovieSchema],
                  summary="Search all Movies."
                  )
def get_all_movies(page: int = 1):
    """
    Function returns a list of all movies in the database.
    The get_all_movies function takes an optional parameter, page, which specifies
    which subset of movies should be returned. The default value for a page is 1.

    Param page:int=1: Indicate the page number of the movies to be retrieved
    Return: A list of movie objects.
    """
    return MovieController.get_all_movies(page)


@movie_router.get("/movie/id",
                  response_model=MovieWithDirectorAndGenreSchema,
                  summary="Read Movie with Genre and Director. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))]
                  )
def get_movie_with_genre_and_director(movie_id: str):
    """
    Function returns a movie with the genre and director of the movie.
    The function takes in a string parameter, which is the ID of the movie.
    The function then calls on MovieActorController to get
    the desired information.

    Param movie_id:str: Specify the movie_id of the movie that is to be returned
    Return: A movie object.
    """
    return MovieActorController.get_movie_with_director_and_genre(movie_id)


@movie_router.put("/",
                  response_model=MovieSchema,
                  summary="Update Movie Data. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  status_code=status.HTTP_201_CREATED
                  )
def update_movie_data(movie: MovieSchemaIn, movie_id):
    """
    The update_movie_data function updates the movie data for a given movie ID.


    Param movie:MovieSchemaIn: Pass in the movie object that is being updated
    Param movie_id: Identify the movie to be updated
    Return: The updated movie data.
    """
    attributes = {key: value for key, value in vars(movie).items() if value}
    return MovieController.update_movie_data(movie_id, attributes)


@movie_router.delete("/",
                     summary="Delete movie. Admin route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))]
                     )
def delete_movie(movie_id: str = Body(embed=True)):
    """
    Function deletes a movie from the database.

    Param movie_id:str: Specify the movie_id of the movie to be deleted
    Return: A string with the message 'movie deleted'.
    """
    return MovieController.delete_movie(movie_id)


movie_actor_router = APIRouter(tags=["MoviesActors"], prefix="/api/movies-actors")


@movie_actor_router.post("/",
                         dependencies=[Depends(JWTBearer(["super_user"]))],
                         summary="Add actor to Movie. Admin Route",
                         status_code=status.HTTP_201_CREATED
                         )
def add_actor_to_movie(movie_id: str = Body(embed=True), actor_id: str = Body(embed=True)):
    """
    The add_actor_to_movie function adds an actor to a movie.

    Param movie_id:str: Specify, which movie the actor is being added to
    Param actor_id:str: Specify the actor that will be added to the movie
    Return: A movie-actor object.
    """
    return MovieActorController.create_movie_actor(movie_id, actor_id)


@movie_actor_router.delete("/",
                           dependencies=[Depends(JWTBearer(["super_user"]))],
                           summary="Remove actor from Movie. Admin Route.",
                           status_code=status.HTTP_201_CREATED
                           )
def remove_actor_from_movie(movie_id: str = Body(embed=True), actor_id: str = Body(embed=True)):
    """
    The remove_actor_from_movie function removes an actor from a movie.

    Param movie_id:str: Find the movie in the database
    Param actor_id:str: Specify, which actor to remove from the movie
    Return: A list of actors that are in the movie.
    """
    return MovieActorController.delete_movie_actor(movie_id, actor_id)


watch_movie = APIRouter(prefix="/api/watch-movie", tags=["Watch Movie"])


@watch_movie.post("/",
                  summary="Select movie to watch. User Route.",
                  status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                  )
def user_watch_movie(request: Request, title: str = Body(embed=True)):
    """
    Function allows a user to watch a movie.
    It takes in the title of the movie and returns an error if it does not exist.

    Param request:Request: Get the user_id from the cookie
    Param title:str: Pass in the title of the movie that is being watched
    Return: A dictionary.
    """
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_watch_movie(user_id, title)


@watch_movie.patch("/rate-movie",
                   response_model=UserWatchMovieSchema,
                   summary="Rate movie. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def user_rate_movie(request: Request, title: str = Body(embed=True), rating: int = Body(embed=True)):
    """
    The user_rate_movie function allows a user to rate a movie.
    It takes in the title of the movie and rating as parameters.
    The function returns an object with the updated rating.

    Param request:Request: Get the user_id from the cookie
    Param title:str: Specify the movie title
    Param rating:int: Specify the rating of the movie
    Return: The movie object that was rated.
    """
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    obj = UserWatchMovieController.user_rate_movie(user_id, title.strip(), rating)
    return obj


@watch_movie.get("/get-movie/title",
                 response_model=MovieFullSchema,
                 summary="See actors, director and Genre for specific Movie."
                 )
def get_movie_data(title: str):
    """
    Function takes a movie title as an argument and returns the data for that movie.

    Param title:str: Get the title of the movie
    Return: A dictionary.
    """
    return MovieController.get_movie_data(title)


@watch_movie.get("/get-movie/actors",
                 response_model=MovieWithActorsSchema,
                 summary="Read Movie by ID. Admin Route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_movie_with_actors(movie_id: str):
    """
    Function returns a movie with all of its actors.
    It takes in a movie_id as an argument and returns the movie object if it exists, otherwise it returns None.

    Param movie_id:str: Specify the movie_id of the movie that is being queried
    Return: A dictionary.
    """
    return MovieActorController.get_movie_with_actors(movie_id)


@watch_movie.get("/get-movie/best-rated-movie")
def show_best_rated_movie():
    """
    Function returns the movie with the highest rating.

    Return: The best rated movie.
    """
    return UserWatchMovieController.get_best_rated_movie(best=True)


@watch_movie.get("/get-movie/worst-rated-movie")
def show_worst_rated_movie():
    """
    Function returns the movie with the lowest rating.

    Return: The worst rated movie.
    """
    return UserWatchMovieController.get_best_rated_movie(best=False)


@watch_movie.get("/my-movies",
                 response_model=list[MovieSchema],
                 summary="Get user's watched Movies list. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_my_watched_movies_list(request: Request):
    """
    Function returns a list of movies that the user has watched.
    It takes in a Request object as an argument, and uses the cookies to get the user_id.
    It then calls UserWatchMovieController's get_my_watched_movies function to retrieve this information.

    Param request:Request: Get the user_id from the cookies
    Return: A list of movie objects that the user has watched.
    """
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.get_my_watched_movies_list(user_id)


@watch_movie.get("/top-ten-movies",
                 summary="Top Ten Movies. User route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_top_ten_movies():
    """
    Function returns a dictionary of the top ten movies by number of views.
    The function takes no arguments and returns a dictionary with movie IDS as keys and number of views as values.

    Return: A dictionary of the top ten movies in descending order.
    """
    top_ten = UserWatchMovieController.get_popular_movies()
    sorted_movies = {k: {"Views": v} for k, v in sorted(top_ten.items(), key=lambda item: item[1], reverse=True)}
    return sorted_movies


@watch_movie.get("/search-movies/title",
                 summary="Search Movies by title.",
                 response_model=list[MovieWithActorsSchema]
                 )
def search_movies_by_title(title: str):
    """
    Function searches for movies by title.
    It takes a string as an argument and returns a list of dictionaries containing the movie's details.

    Param title:str: Search for a movie by its title
    Return: A list of movie objects.
    """
    return MovieController.search_movies_by_name(title)


@watch_movie.get("/search-movies/director",
                 summary="Search Movies by director.",
                 response_model=list[MovieWithActorsSchema]
                 )
def search_movies_by_director(director: str):
    """
    Function searches for all movies by a given director.
    It takes in a string representing the director's name and returns a list of dictionaries,
    each dictionary containing information about one movie.

    Param director:str: Search for a movie by the director's name
    Return: A list of movies that match the director's name.
    """
    return MovieController.search_movies_by_director(director)


@watch_movie.get("/search-movies/genre",
                 summary="Search Movies by genre.",
                 response_model=list[MovieWithActorsSchema]
                 )
def search_movies_by_genre(genre: str):
    """
    Function searches for movies by a genre.
    It takes a string as an argument and returns a list of movie objects.

    Param genre:str: Search for movies by genre
    Return: A list of movies that match the given genre.
    """
    return MovieController.search_movies_by_genre(genre)


@watch_movie.get("/get-movies/year",
                 summary="Get Movies from specific year. User Route.",
                 response_model=list[MovieSchema],
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_movies_by_year(year: int):
    """
    Function returns a list of movies from the provided year.
    If no movies are found, it returns an empty list.

    Param year:int: Filter the movies by a year
    Return: A list of movies from a given year.
    """
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return MovieController.get_movies_by_year(year)


@watch_movie.get("/get-movies/ratings",
                 summary="Get average Movie ratings. User Route",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_average_ratings():
    """
    Function returns a dictionary of the average ratings for each movie.
    The keys are the movie IDS, and the values are their corresponding average ratings.

    Return: A dictionary of all the movies and their average ratings.
    """
    return UserWatchMovieController.get_average_ratings()


@watch_movie.get("/get-movies/by-rating",
                 summary="Get Movies with average rating higher than requested. User Route",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_movie_with_average_rating_above_requested(rating: float):
    """
    Function returns a list of movies with an average rating
    greater than the requested rating. The function takes one argument, which is the requested movie rating.

    Param rating:float: Specify the minimum average rating of a movie that we want to return.
    Return: A list of movie objects with an average rating above the requested rating.
    """
    return UserWatchMovieController.get_movies_with_higher_average_rating(rating)


@watch_movie.get("/get-movies/show-latest-features",
                 summary="Show latest features",
                 response_model=list[MovieWithActorsSchema]
                 )
def show_latest_features():
    """
    Function returns a list of the latest features added to the database.
    The date limit parameter is used to filter out any features that were created before this date.

    Return: The latest features of movies in the database.
    """
    date_limit = get_day_before_one_month()
    return MovieController.get_latest_features(date_limit)


@watch_movie.get("/get-movies/never-downloaded",
                 summary="Show unpopular movies that never have been watched. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def show_least_popular_movies():
    """
    Function returns a list of movies that have the least amount of views.

    Return: A list of movies with the lowest rating.
    """
    return MovieController.show_least_popular_movies()


@watch_movie.get("/get-movies/my-recommendations",
                 summary="Show recommended Movies. User route.",
                 response_model=list[MovieSchema],
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_my_recommendations(request: Request, page: int = 1):
    """
    Function returns a list of movies that the user has not watched, but is recommended
    for them based on their previous movie ratings. The function takes in a page number as an argument and returns
    a list of movies from that page.

    Param request:Request: Get the user_id from the cookie
    Param page:int=1: Specify, which page of the recommendation list to display
    Return: A list of movies that are recommended for the user.
    """
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.get_my_recommendations(user_id, page)


@watch_movie.get("/get-rating/year",
                 summary="Get average movie rating for a specific year. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_average_movie_rating_for_year(year: int):
    """
    Function returns the average rating for all movies released in a given year.
    The function takes one argument, year, which is an integer representing the release year of a movie.

    Param year:int: Specify the year for which we want to get the average movie rating
    Return: The average movie rating for a given year.
    """
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return UserWatchMovieController.get_average_movie_rating_for_year(year)


@watch_movie.get("/get-most-successful-movie-year",
                 summary="Get most successful year in terms of Movie ratings. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                 )
def get_most_successful_movie_year():
    """
    Function returns the year with the highest average rating.
    It takes no parameters and returns a dictionary containing one key:value pair,
    where the key is 'Most successful year'
    and its value is another dictionary containing two keys: Year and Average Rating.

    Return: The year with the highest average rating.
    """
    response = UserWatchMovieController.get_most_successful_movie_year()
    sorted_movies = [(k, v) for k, v in sorted(response.items(), key=lambda item: item[1], reverse=True)]
    return {"Most successful year": {"Year": sorted_movies[0][0], "Average Rating": sorted_movies[0][1]}}
