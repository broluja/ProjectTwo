"""Director routes"""
from fastapi import APIRouter, Depends, status, Query

from app.directors.schemas import DirectorSchema, DirectorSchemaIn
from app.directors.controller import DirectorController
from app.users.controller import JWTBearer

director_router = APIRouter(tags=["Directors"], prefix="/api/directors")


@director_router.post("/",
                      response_model=DirectorSchema,
                      dependencies=[Depends(JWTBearer(["super_user"]))],
                      summary="Register new Director in DB. Admin Route.",
                      status_code=status.HTTP_201_CREATED)
def create_new_director(director: DirectorSchemaIn):
    """
    Function creates a new director in the database. It takes as input a DirectorSchemaIn object,
    which is defined by marshmallow and contains the fields: first_name, last_name, country.
    The function returns an integer representing the ID of the newly created director.

    Param director:DirectorSchemaIn: Validate the input data.
    Return: A director-schema-out object.
    """
    return DirectorController.create_director(director.first_name, director.last_name, director.country)


@director_router.get("/", response_model=list[DirectorSchema])
def get_all_directors():
    """
    Function returns a list of all directors in the database.

    Return: A list of all directors in the database.
    """
    return DirectorController.get_all_directors()


@director_router.get("/get-director/id",
                     response_model=DirectorSchema,
                     summary="Read Director using ID. Admin Route",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def get_director_by_id(director_id: str):
    """
    Function takes a director_id as an argument and returns the Director object with that ID.

    Param director_id:str: Specify the ID of the director that is being retrieved.
    Return: A dictionary with the director's information.
    """
    return DirectorController.get_director_by_id(director_id)


@director_router.get("/get-director/first-name", response_model=list[DirectorSchema])
def get_director_by_first_name(first_name: str):
    """
    Function searches for directors by their first name.
    It takes a string as an argument and returns a list of dictionaries,
    each dictionary representing one director.

    Param first_name:str: Specify the first name of the director to be searched.
    Return: A list of director objects that match the first name.
    """
    return DirectorController.search_directors_by_first_name(first_name.strip(), search=False)


@director_router.get("/get-director/last-name", response_model=list[DirectorSchema])
def get_director_by_last_name(last_name: str):
    """
    Function searches for directors by last name.
    It takes a string as an argument and returns a list of dictionaries containing the director's
    first and last names, as well as their ID number.

    Param last_name:str: Specify the last name of the director.
    Return: A list of director objects.
    """
    return DirectorController.search_directors_by_last_name(last_name.strip(), search=False)


@director_router.get("/get-director/country", response_model=list[DirectorSchema])
def get_director_by_country(country: str):
    """
    Function searches for directors by country. It takes a string as an argument
    and returns a list of dictionaries, where each dictionary contains information about one director.

    Param country:str: Search for directors from a specific country.
    Return: A list of directors.
    """
    return DirectorController.search_directors_by_country(country.strip(), search=False)


@director_router.get("/search-directors", summary="Search Directors", response_model=list[DirectorSchema])
def search_directors(choice: str = Query("First Name", enum=["First Name", "Last Name", "Country"]), query: str = ""):
    if choice == "First Name":
        return DirectorController.search_directors_by_first_name(query, search=True)
    elif choice == "Last Name":
        return DirectorController.search_directors_by_last_name(query, search=True)
    elif choice == "Country":
        return DirectorController.search_directors_by_country(query, search=True)


@director_router.put("/",
                     response_model=DirectorSchema,
                     summary="Update Director`s data. Admin Route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))],
                     status_code=status.HTTP_201_CREATED)
def update_director(director_id: str, director: DirectorSchemaIn):
    """
    Function updates a director's information.

    Param director_id:str: Identify the director to be updated
    Param director:DirectorSchemaIn: Specify the schema of the incoming director
    Return: A director-schema-out object.
    """
    attributes = {key: value for key, value in vars(director).items() if value}
    return DirectorController.update_director(director_id, attributes)


@director_router.delete("/",
                        summary="Delete Director. Admin Route.",
                        dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_director(director_id: str):
    """
    Function deletes a director from the database.

    Param director_id:str: Specify the director to be deleted
    Return: A dictionary response.
    """
    return DirectorController.delete_director(director_id)
