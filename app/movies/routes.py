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
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def add_new_movie(movie: MovieSchemaIn):
    return MovieController.create_movie(**vars(movie))


@movie_router.get("/get-all-movies", response_model=list[MovieWithActorsSchema], description="Read all Movies from DB")
def get_all_movies():
    return MovieController.get_all_movies()


@movie_router.get("/get-movie-actors", response_model=MovieWithActorsSchema)
def get_movie_with_all_actors(movie_id: str):
    return MovieActorController.get_movie_with_actors(movie_id)


@movie_router.get("/get-movie-director-and-genre", response_model=MovieWithDirectorAndGenreSchema)
def get_movie_with_genre_and_director(movie_id: str):
    return MovieActorController.get_movie_with_director_and_genre(movie_id)


@movie_router.delete("/delete-movie", description='Delete specific movie by ID', summary="Delete movie. Admin route.")
def delete_movie(movie_id: str):
    return MovieController.delete_movie(movie_id)


movie_actor_router = APIRouter(tags=["MoviesActors"], prefix="/api/movies_actors")


@movie_actor_router.post("/add_actor_to_movie",
                         dependencies=[Depends(JWTBearer(["super_user"]))],
                         description="Add actor to Movie")
def add_actor_to_movie(movie_id: str, actor_id: str):
    return MovieActorController.create_movie_actor(movie_id, actor_id)


@movie_actor_router.delete("/remove_actor_to_movie",
                           dependencies=[Depends(JWTBearer(["super_user"]))],
                           description="Remove actor from Movie")
def remove_actor_from_movie(movie_id: str, actor_id: str):
    return MovieActorController.delete_movie_actor(movie_id, actor_id)


watch_movie = APIRouter(prefix="/api/watch-movie", tags=["Watch Movie"])


@watch_movie.post("/", description="Select movie to watch", status_code=status.HTTP_201_CREATED)
def user_watch_movie(request: Request, title: str):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_watch_movie(user_id, title)


@watch_movie.put("/rate-movie", response_model=UserWatchMovieSchema, description="Rate Movie")
def user_rate_movie(request: Request, title: str, rating: int):
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_rate_movie(user_id, title, rating)


@watch_movie.get("/get-my-watched-movies",
                 response_model=list[MovieSchema],
                 dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_my_watched_movies_list(request: Request):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.get_my_watched_movies_list(user_id)


@watch_movie.get("/top-ten-movies", description="Get top ten movies.", summary="Top Ten Movies. User route.")
def get_top_ten_movies():
    return UserWatchMovieController.get_popular_movies()


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


@watch_movie.get("/best-rated-movie", description="Show best rated movie",)
def show_best_rated_movie():
    return UserWatchMovieController.get_best_rated_movie(best=True)


@watch_movie.get("/worst-rated-movie", description="Show worst rated movie")
def show_worst_rated_movie():
    return UserWatchMovieController.get_best_rated_movie(best=False)


@watch_movie.get("/show-latest-features",
                 description="Show latest released movies.",
                 summary="Show latest features",
                 response_model=list[MovieWithActorsSchema])
def show_latest_features():
    date_limit = get_day_before_one_month()
    return MovieController.get_latest_features(date_limit)


@watch_movie.get("/show-movies-never-downloaded",
                 summary="Show unpopular movies that never have been watched. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))],
                 response_model=list[MovieSchema])
def show_least_popular_movies():
    return MovieController.show_least_popular_movies()
