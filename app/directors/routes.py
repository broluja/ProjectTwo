from fastapi import APIRouter, Depends

from app.directors.schemas import DirectorSchema, DirectorSchemaIn
from app.directors.controller import DirectorController
from app.users.controller import JWTBearer

director_router = APIRouter(tags=["Directors"], prefix="/api/directors")


@director_router.post("/create-director",
                      response_model=DirectorSchema,
                      dependencies=[Depends(JWTBearer(["super_user"]))],
                      description="Register new Director in DB")
def create_new_director(director: DirectorSchemaIn):
    return DirectorController.create_director(director.first_name, director.last_name, director.country)


@director_router.get("/get-all-directors", response_model=list[DirectorSchema], description="Read all Directors")
def get_all_directors():
    return DirectorController.get_all_directors()


@director_router.get("/id", response_model=DirectorSchema, description="Read Director using ID", deprecated=True)
def get_director_by_id(director_id: str):
    return DirectorController.get_director_by_id(director_id)


@director_router.get("/search-directors-by-last-name",
                     response_model=list[DirectorSchema],
                     description="Search Directors by Last Name")
def search_directors_by_last_name(last_name: str):
    return DirectorController.search_directors_by_last_name(last_name)


@director_router.get("/search-directors-by-country",
                     response_model=list[DirectorSchema],
                     description="Search Directors by Country")
def search_directors_by_country(country: str):
    return DirectorController.search_directors_by_country(country)


@director_router.put("/id",
                     response_model=DirectorSchema,
                     description="Update Director`s data",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def update_director(director_id: str, first_name: str = None, last_name: str = None, country: str = None):
    return DirectorController.update_director(director_id, first_name, last_name, country)
