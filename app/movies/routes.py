from fastapi import APIRouter, Depends, status, HTTPException
from starlette.requests import Request

from app.movies.controller import MovieController, MovieActorController
from app.movies.schemas import *
from app.users.controller import JWTBearer, UserWatchMovieController
from app.users.schemas.user_watch_movie_schema import UserWatchMovieSchema

movie_router = APIRouter(tags=["Movies"], prefix="/api/movies")


@movie_router.post("/add-movie", response_model=MovieSchema, dependencies=[Depends(JWTBearer(["super_user"]))])
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


watch_movie = APIRouter(prefix="/api/watch_movie", tags=["Watch Movie"])


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


@watch_movie.get("/movie-downloads", description="Get top ten movies.", summary="Top Ten Movies. User route.")
def get_movie_downloads():
    return UserWatchMovieController.get_popular_movies()
    