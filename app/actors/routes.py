"""Actor routes"""
from fastapi import APIRouter, Depends, status

from app.actors.controller import ActorController
from app.actors.schemas import ActorSchema, ActorSchemaIn
from app.users.controller import JWTBearer

actor_router = APIRouter(tags=["Actors"], prefix="/api/actors")


@actor_router.post("/create-actor",
                   response_model=ActorSchema,
                   summary="Create New Actor. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED)
def create_new_actor(actor: ActorSchemaIn):
    """
    Function creates a new actor in the database.
    It takes an ActorSchemaIn object as input, and returns an ActorSchemaOut object.

    Param actor:ActorSchemaIn: Pass the data from the request body to the create actor function
    Return: The newly created actor in the form of a dictionary.
    """
    return ActorController.create_actor(**vars(actor))


@actor_router.get("/get-all-actors", response_model=list[ActorSchema])
def get_all_actors(page: int = 1):
    """
    Function returns a list of all actors in the database. The get_all_actors function
    takes an optional parameter, page, which specifies which subset of the entire
    actor list should be returned. The default value for a page is 1.

    Param page:int=1: Specify the page number to be returned.
    Return: A list of actors.
    """
    return ActorController.get_all_actors(page)


@actor_router.get("/id/get-actor",
                  response_model=ActorSchema,
                  summary="Read Actor by ID. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))])
def get_actor_by_id(actor_id: str):
    """
    Function will return an actor object given the actor's ID.
    If no such actor exists, it will return None.

    Param actor_id:str: Identify the actor that is being searched for.
    Return: The actor object that has the given actor_id.
    """
    return ActorController.get_actor_by_id(actor_id)


@actor_router.get("/get-actor-by-last-name", response_model=list[ActorSchema])
def get_actor_by_last_name(actor: str):
    """
    Function takes a string representing the last name of an actor and returns
    the Actor object associated with that last name. If no such actor exists, None is returned.

    Param actor:str: Pass the last name of the actor to be searched.
    Return: A dictionary with the actor's details.
    """
    return ActorController.get_actor_by_last_name(actor.strip())


@actor_router.get("/get-actor-by-first-name", response_model=list[ActorSchema])
def get_actor_by_first_name(actor: str):
    """
    Function takes a string as an argument and returns the actor object with that first name.
    If no such actor exists, it returns None.

    Param actor:str: Specify the name of the actor that is being searched for.
    Return: A list of actors that match the first name given.
    """
    return ActorController.get_actor_by_first_name(actor.strip())


@actor_router.get("/get-actor-movies")
def get_actor_movies(actor_last_name: str):
    """
    Function returns a list of movies that the actor with the given last name was in.
    The function takes one argument, which is an actor's last name.
    The function will return a list of dictionaries,
    each dictionary representing a movie and containing keys for title and year.

    Param actor_last_name:str: Specify the last name of the actor.
    Return: A list of movie objects.
    """
    return ActorController.get_actor_movies(actor_last_name.strip())


@actor_router.put("/id/update-actor",
                  response_model=ActorSchema,
                  summary="Update Actor. Admin Route.",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  status_code=status.HTTP_201_CREATED)
def update_actor(actor_id, actor: ActorSchemaIn):
    """
    Function updates an actor's information.

    Param actor_id: Identify the actor to be updated.
    Param actor:ActorSchemaIn: Validate the input data.
    Return: A dictionary with the actor's updated information.
    """
    attributes = {key: value for key, value in vars(actor).items() if value}
    return ActorController.update_actor(actor_id, attributes)


@actor_router.delete("/id/delete-actor",
                     summary="Delete Actor by ID. Admin Route",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_actor_by_id(actor_id: str):
    """
    Function deletes an actor from the database.
    It takes in a string representing the ID of the actor to be deleted, and returns
    a dictionary with either a success message, or an error message.

    Param actor_id:str: Specify, which actor to delete.
    Return: A boolean value.
    """
    return ActorController.delete_actor(actor_id)
