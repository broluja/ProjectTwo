from fastapi import APIRouter, Depends

from app.actors.controller import ActorController
from app.actors.schemas import ActorSchema, ActorSchemaIn
from app.users.controller import JWTBearer

actor_router = APIRouter(tags=["Actors"], prefix="/api/actors")


@actor_router.post("/create-actor", response_model=ActorSchema, dependencies=[Depends(JWTBearer(["super_user"]))])
def create_new_actor(actor: ActorSchemaIn):
    return ActorController.create_actor(actor.first_name, actor.last_name, actor.date_of_birth, actor.country)


@actor_router.get("/get-all-actors", response_model=list[ActorSchema], description="Read all Actors from DB")
def get_all_actors():
    return ActorController.get_all_actors()
