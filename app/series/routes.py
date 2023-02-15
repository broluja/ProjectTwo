from fastapi import APIRouter, Depends, status, HTTPException
from starlette.requests import Request

from app.series.controller import SeriesController, EpisodeController
from app.series.controller.series_actor_controller import SeriesActorController
from app.series.schemas import *
from app.users.controller import JWTBearer
from app.users.controller.user_watch_episode_controller import UserWatchEpisodeController
from app.users.schemas.user_watch_episode_schema import UserWatchEpisodeSchema

series_router = APIRouter(tags=["Series"], prefix="/api/series")


@series_router.post("/create-new-series",
                    description="Add new Series",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=SeriesWithDirectorAndGenreSchema)
def create_new_series(series: SeriesSchemaIn):
    return SeriesController.create_series(**series.dict())


@series_router.get("/get-all-series", description="Get all Series from DB", response_model=list[SeriesWithActorsSchema])
def get_all_series():
    return SeriesController.read_all_series()


@series_router.get("/search-series-by-director",
                   description="Search for Series by Director",
                   summary="Search Series by Director Last Name")
def get_series_by_director_name(director: str):
    return SeriesController.get_series_by_director_name(director.strip())


@series_router.get("/get-series-by-episode-id")
def get_series_by_episode_id(episode_id: str):
    return SeriesController.get_series_by_episode_id(episode_id)


@series_router.put("/update-series", summary="Update Series Data")
def update_series_data(series: SeriesSchemaIn, series_id: str):
    attributes = {key: value for key, value in vars(series).items() if value}
    return SeriesController.update_series_data(series_id, attributes)


@series_router.delete("/delete-series",
                      description="Delete series with all episodes.",
                      summary="delete Series")
def delete_series(series_id: str):
    return SeriesController.delete_series(series_id)


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
def get_all_episodes_for_series(series_title: str):
    return EpisodeController.get_all_episodes_by_series(series_title)


@episode_router.get("/get-episode-by-id",
                    summary="Get episode by ID",
                    response_model=EpisodeSchema,
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_episode_by_id(episode_id: str):
    return EpisodeController.get_episode_by_id(episode_id)


@episode_router.put("/update-episode",
                    summary="Update Episode",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=EpisodeSchema)
def update_episode(episode_id: str, episode: EpisodeSchemaIn):
    attributes = {key: value for key, value in vars(episode).items() if value}
    return EpisodeController.update_episode(episode_id, attributes)


@episode_router.delete("/delete-episode-by-id",
                       summary="Delete episode by ID",
                       dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_episode(episode_id: str):
    return EpisodeController.delete_episode(episode_id)


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


@watch_episode.get("/get-my-series",
                   summary="Get my series",
                   description="Get all series User watched",
                   dependencies=[Depends(JWTBearer(["regular_user"]))])
def get_my_series(request: Request):
    user_id = request.cookies.get("user_id")
    return SeriesController.get_my_series(user_id)


@watch_episode.get("/search-series", response_model=list[SeriesWithActorsSchema], description="Search for Series")
def search_series_by_name(series: str):
    return SeriesController.get_series_by_name(series.strip())


@watch_episode.get("/get-popular-series", description="Get most popular Series.")
def get_most_popular_series():
    series = UserWatchEpisodeController.get_most_popular_series()
    sorted_series = {k: f"Users watch: {v}" for k, v in sorted(series.items(), key=lambda item: item[1], reverse=True)}
    return sorted_series


@watch_episode.get("/get-best-rated-episodes", description="Get best rated episodes.")
def get_best_rated_episodes():
    return EpisodeController.get_best_rated_episode()


@watch_episode.get("/get-worst-rated-episodes", description="Get worst rated episodes.")
def get_worst_rated_episodes():
    return EpisodeController.get_best_rated_episode(best=False)
