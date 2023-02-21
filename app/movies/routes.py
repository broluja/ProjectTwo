"""Movie and Movie-Actor routes"""
from fastapi import APIRouter, Depends, status, HTTPException
from starlette.requests import Request

from app.movies.controller import MovieController, MovieActorController
from app.movies.schemas import *
from app.users.controller import UserWatchMovieController, JWTBearer
from app.users.schemas.user_watch_movie_schema import UserWatchMovieSchema
from app.utils import get_day_before_one_month

movie_router = APIRouter(tags=["Movies"], prefix="/api/movies")


@movie_router.post("/add-movie",
                   response_model=MovieWithDirectorAndGenreSchema,
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def add_new_movie(movie: MovieSchemaIn):
    return MovieController.create_movie(**vars(movie))


@movie_router.get("/get-all-movies",
                  response_model=list[MovieWithActorsSchema],
                  description="Read all Movies from DB",
                  summary="Search all Movies."
                  )
def get_all_movies(page: int = 1):
    return MovieController.get_all_movies(page)


@movie_router.get("/get-movie-director-and-genre",
                  response_model=MovieWithDirectorAndGenreSchema,
                  summary="Read Movie with Genre and Director. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))]
                  )
def get_movie_with_genre_and_director(movie_id: str):
    return MovieActorController.get_movie_with_director_and_genre(movie_id)


@movie_router.put("/update-movie",
                  response_model=MovieSchema,
                  summary="Update Movie Data",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  status_code=status.HTTP_201_CREATED
                  )
def update_movie_data(movie: MovieSchemaIn, movie_id):
    attributes = {key: value for key, value in vars(movie).items() if value}
    return MovieController.update_movie_data(movie_id, attributes)


@movie_router.delete("/delete-movie",
                     description='Delete specific movie by ID',
                     summary="Delete movie. Admin route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))]
                     )
def delete_movie(movie_id: str):
    return MovieController.delete_movie(movie_id)


movie_actor_router = APIRouter(tags=["MoviesActors"], prefix="/api/movies_actors")


@movie_actor_router.post("/add_actor_to_movie",
                         dependencies=[Depends(JWTBearer(["super_user"]))],
                         description="Add actor to Movie",
                         status_code=status.HTTP_201_CREATED
                         )
def add_actor_to_movie(movie_id: str, actor_id: str):
    return MovieActorController.create_movie_actor(movie_id, actor_id)


@movie_actor_router.delete("/remove_actor_to_movie",
                           dependencies=[Depends(JWTBearer(["super_user"]))],
                           description="Remove actor from Movie",
                           status_code=status.HTTP_201_CREATED
                           )
def remove_actor_from_movie(movie_id: str, actor_id: str):
    return MovieActorController.delete_movie_actor(movie_id, actor_id)


watch_movie = APIRouter(prefix="/api/watch-movie", tags=["Watch Movie"])


@watch_movie.post("/",
                  summary="Select movie to watch. User Route.",
                  status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                  )
def user_watch_movie(request: Request, title: str):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_watch_movie(user_id, title)


@watch_movie.put("/rate-movie",
                 response_model=UserWatchMovieSchema,
                 summary="Rate movie. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))],
                 status_code=status.HTTP_201_CREATED
                 )
def user_rate_movie(request: Request, title: str, rating: int):
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    obj = UserWatchMovieController.user_rate_movie(user_id, title.strip(), rating)
    return obj


@watch_movie.get("/get-movie-data",
                 response_model=MovieFullSchema,
                 summary="See actors, director and Genre for specific Movie.")
def get_movie_data(title: str):
    return MovieController.get_movie_data(title)


@watch_movie.get("/get-my-watched-movies",
                 response_model=list[MovieSchema],
                 summary="Get user's watched Movies list. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_my_watched_movies_list(request: Request):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.get_my_watched_movies_list(user_id)


@watch_movie.get("/top-ten-movies",
                 summary="Top Ten Movies. User route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_top_ten_movies():
    top_ten = UserWatchMovieController.get_popular_movies()
    sorted_movies = {k: {"Views": v} for k, v in sorted(top_ten.items(), key=lambda item: item[1], reverse=True)}
    return sorted_movies


@watch_movie.get("/search-movies-title",
                 description="Search movies by name.",
                 summary="Search Movies by title.",
                 response_model=list[MovieWithActorsSchema])
def search_movies_by_title(title: str):
    return MovieController.search_movies_by_name(title)


@watch_movie.get("/search-movies-director",
                 description="Search movies by name.",
                 summary="Search Movies by director.",
                 response_model=list[MovieWithActorsSchema])
def search_movies_by_director(director: str):
    return MovieController.search_movies_by_director(director)


@watch_movie.get("/search-movies-genre",
                 description="Search movies by genre.",
                 summary="Search Movies by genre.",
                 response_model=list[MovieWithActorsSchema])
def search_movies_by_genre(genre: str):
    return MovieController.search_movies_by_genre(genre)


@watch_movie.get("/get-movie-actors",
                 response_model=MovieWithActorsSchema,
                 summary="Read Movie by ID. Admin Route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_movie_with_all_actors(movie_id: str):
    return MovieActorController.get_movie_with_actors(movie_id)


@watch_movie.get("/get-movies-by-year",
                 summary="Get Movies from specific year. User Route.",
                 response_model=list[MovieSchema],
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_movies_by_year(year: int):
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return MovieController.get_movies_by_year(year)


@watch_movie.get("/get-movie-average-rating",
                 summary="Get average rating for specific Movie. User Route",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_average_rating_for_movie(name: str):
    return UserWatchMovieController.get_average_rating_for_movie(name)


@watch_movie.get("/get-average-ratings",
                 summary="Get average Movie ratings. User Route",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_average_ratings():
    return UserWatchMovieController.get_average_ratings()


@watch_movie.get("/get-movies-higher-rating",
                 summary="Get Movies with average rating higher than requested. User Route",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_movie_with_average_rating_above_requested(rating: float):
    return UserWatchMovieController.get_movies_with_higher_average_rating(rating)


@watch_movie.get("/get-average-movie-rating-for-year",
                 summary="Get average movie rating for a specific year. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_average_movie_rating_for_year(year: int):
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return UserWatchMovieController.get_average_movie_rating_for_year(year)


@watch_movie.get("/get-most-successful-movie-year",
                 summary="Get most successful year in terms of Movie ratings. User Route.",
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_most_successful_movie_year():
    response = UserWatchMovieController.get_most_successful_movie_year()
    sorted_movies = [(k, v) for k, v in sorted(response.items(), key=lambda item: item[1], reverse=True)]
    return {"Most successful year": {"Year": sorted_movies[0][0], "Average Rating": sorted_movies[0][1]}}


@watch_movie.get("/best-rated-movie", description="Show best rated movie.")
def show_best_rated_movie():
    return UserWatchMovieController.get_best_rated_movie(best=True)


@watch_movie.get("/worst-rated-movie", description="Show worst rated movie.")
def show_worst_rated_movie():
    return UserWatchMovieController.get_best_rated_movie(best=False)


@watch_movie.get("/show-latest-features",
                 description="Show recent released movies.",
                 summary="Show latest features",
                 response_model=list[MovieWithActorsSchema])
def show_latest_features():
    date_limit = get_day_before_one_month()
    return MovieController.get_latest_features(date_limit)


@watch_movie.get("/show-movies-never-downloaded",
                 summary="Show unpopular movies that never have been watched. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def show_least_popular_movies():
    return MovieController.show_least_popular_movies()


@watch_movie.get("/get-my-recommendations",
                 summary="Show recommended Movies. User route.",
                 description="Show User recommended Movies.",
                 response_model=list[MovieSchema],
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_my_recommendations(request: Request, page: int = 1):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.get_my_recommendations(user_id, page)
