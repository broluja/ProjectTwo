"""Genre routes module"""
from fastapi import APIRouter, Depends, status

from app.genres.schemas import GenreSchema, GenreSchemaIn
from app.genres.controller import GenreController
from app.users.controller import JWTBearer

genre_router = APIRouter(tags=["Genres"], prefix="/api/genres")


@genre_router.post("/",
                   response_model=GenreSchema,
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   summary="Register new Genre in DB. Admin Route.",
                   status_code=status.HTTP_201_CREATED)
def create_new_genre(genre: GenreSchemaIn):
    """
    The create_new_genre function creates a new genre in the database.
    It takes one argument, which is a GenreSchemaIn object.
    The function returns the newly created genre.

    Param genre:GenreSchemaIn: Pass the name of the genre to be created.
    Return: A genre-schema-out object.
    """
    return GenreController.create_director(genre.name)


@genre_router.get("/", response_model=list[GenreSchema])
def get_all_genres():
    """
    Function returns a list of all genres in the database.

    Return: A list of all the genres in the database.
    """
    return GenreController.get_all_genres()


@genre_router.get("/get-genre/id",
                  response_model=GenreSchema,
                  summary="Read Genre by ID. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))])
def get_genre_by_id(genre_id: str):
    """
    Function takes a genre_id as an argument and returns the Genre object associated with that ID.


    Param genre_id:str: Identify the genre to be returned
    Return: A genre object.
    """
    return GenreController.get_genre_by_id(genre_id)


@genre_router.get("/search-genres/name",
                  response_model=list[GenreSchema],
                  summary="Search Genres by Name. User Route.",
                  dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def search_genres_by_name(name: str):
    """
    Function searches for genres by name.
    It takes a string as an argument and returns a list of Genre objects that match the search query.

    Param name:str: Search for a genre by name
    Return: A list of genre objects.
    """
    return GenreController.search_genres_by_name(name.strip())


@genre_router.put("/",
                  response_model=GenreSchema,
                  summary="Update Genre`s data. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  status_code=status.HTTP_201_CREATED)
def update_genre(genre_id: str, name: str):
    """
    Function updates a genre's name.

    Param genre_id:str: Identify the genre to be updated
    Param name:str: Update the name of a genre
    Return: A dictionary with a key of &quot;success&quot; and a value of true or false.
    """
    return GenreController.update_genre(genre_id, name)
