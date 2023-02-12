from fastapi import APIRouter, Depends, status, HTTPException
from starlette.requests import Request

from app.series.controller import SeriesController, EpisodeController
from app.series.controller.series_actor_controller import SeriesActorController
from app.series.schemas import SeriesSchemaIn, SeriesSchema, EpisodeSchema, EpisodeSchemaIn
from app.users.controller import JWTBearer
from app.users.controller.user_watch_episode_controller import UserWatchEpisodeController
from app.users.schemas.user_watch_episode_schema import UserWatchEpisodeSchema

series_router = APIRouter(tags=["Series"], prefix="/api/series")


@series_router.post("/create-new-series",
                    description="Add new Series",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def create_new_series(series: SeriesSchemaIn):
    return SeriesController.create_series(**series.dict())


@series_router.get("/get-all-series", description="Get all Series from DB", response_model=list[SeriesSchema])
def get_all_series():
    return SeriesController.read_all_series()


@series_router.get("/get-my-series",
                   response_model=list[SeriesSchema],
                   summary="Get my series",
                   description="Get all series User watched")
def get_my_series(request: Request):
    user_id = request.cookies.get("user_id")
    return SeriesController.get_my_series(user_id)


episode_router = APIRouter(tags=["Episodes"], prefix="/api/episodes")


@episode_router.post("/add-new-episode",
                     response_model=EpisodeSchema,
                     description="Create new Episode. Admin route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def create_new_episode(episode: EpisodeSchemaIn):
    return EpisodeController.create_episode(**episode.dict())


@episode_router.get("/get-all-episodes-for-series",
                    response_model=list[EpisodeSchema],
                    description="Get all episodes from a Series")
def get_all_episodes_from_series(series_title: str):
    return EpisodeController.get_all_episodes_by_series(series_title)


series_actor_router = APIRouter(tags=["SeriesActors"], prefix="/api/series_actors")


@series_actor_router.post("/add-actor-to-series",
                          dependencies=[Depends(JWTBearer(["super_user"]))],
                          description="Add actor to Series")
def add_actor_to_movie(series_id: str, actor_id: str):
    return SeriesActorController.create_series_actor(series_id, actor_id)


@series_actor_router.delete("/remove-actor-from-series",
                            dependencies=[Depends(JWTBearer(["super_user"]))],
                            description="Remove actor from Series")
def remove_actor_from_movie(series_id: str, actor_id: str):
    return SeriesActorController.delete_series_actor(series_id, actor_id)


watch_episode = APIRouter(prefix="/api/watch_episode", tags=["Watch Episode"])


@watch_episode.post("/", description="Select episode to watch", status_code=status.HTTP_201_CREATED)
def user_watch_episode(request: Request, episode_name: str, series_title: str):
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_watch_episode(user_id, episode_name, series_title)


@watch_episode.put("/rate-episode", response_model=UserWatchEpisodeSchema, description="Rate Series Episode")
def user_rate_episode(request: Request, episode_name: str, series_title: str, rating: int):
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_rate_episode(user_id, episode_name, series_title, rating)