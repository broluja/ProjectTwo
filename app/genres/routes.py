from fastapi import APIRouter, Depends

from app.genres.schemas import GenreSchema, GenreSchemaIn
from app.genres.controller import GenreController
from app.users.controller import JWTBearer

genre_router = APIRouter(tags=["Genres"], prefix="/api/genres")


@genre_router.post("/create-genre",
                   response_model=GenreSchema,
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   description="Register new Genre in DB")
def create_new_genre(genre: GenreSchemaIn):
    return GenreController.create_director(genre.name)


@genre_router.get("/get-all-genres",
                  response_model=list[GenreSchema],
                  description="Read all Genres from DB",
                  dependencies=[Depends(JWTBearer(["super_user", "regular_user"]))])
def get_all_genres():
    return GenreController.get_all_genres()


@genre_router.get("/id",
                  response_model=GenreSchema,
                  description="Read Genre by ID",
                  dependencies=[Depends(JWTBearer(["super_user", "regular_user"]))])
def get_genre_by_id(genre_id: str):
    return GenreController.get_genre_by_id(genre_id)


@genre_router.get("/search-genres-by-name", response_model=list[GenreSchema], description="Search Genres by Name")
def search_genres_by_name(name: str):
    return GenreController.search_genres_by_name(name.strip())


@genre_router.put("/id",
                  response_model=GenreSchema,
                  description="Update Genre`s data",
                  dependencies=[Depends(JWTBearer(["super_user"]))])
def update_genre(genre_id: str, name: str):
    return GenreController.update_genre(genre_id, name)

