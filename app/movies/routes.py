from fastapi import APIRouter, Depends

from app.movies.controller import MovieController, MovieActorController
from app.movies.schemas import *
from app.users.controller import JWTBearer

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


@movie_actor_router.post("/add_actor_to_movie")
def add_actor_to_movie(movie_id: str, actor_id: str):
    return MovieActorController.create_movie_actor(movie_id, actor_id)
