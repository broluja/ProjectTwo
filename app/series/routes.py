from fastapi import APIRouter, Depends, status, HTTPException
from starlette.requests import Request

from app.series.controller import SeriesController, EpisodeController
from app.series.controller.series_actor_controller import SeriesActorController
from app.series.schemas import *
from app.users.controller import JWTBearer
from app.users.controller.user_watch_episode_controller import UserWatchEpisodeController
from app.users.schemas.user_watch_episode_schema import UserWatchEpisodeSchema
from app.utils import get_day_before_one_month

series_router = APIRouter(tags=["Series"], prefix="/api/series")


@series_router.post("/create-new-series",
                    description="Add new Series",
                    summary="Create new Series. Admin Route.",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=SeriesWithDirectorAndGenreSchema)
def create_new_series(series: SeriesSchemaIn):
    return SeriesController.create_series(**series.dict())


@series_router.get("/get-all-series", description="Get all Series from DB", response_model=list[SeriesWithActorsSchema])
def get_all_series(page: int = 1):
    return SeriesController.read_all_series(page)


@series_router.get("/get-series-by-episode-id",
                   summary="Get Series using ID. Admin Route",
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def get_series_by_episode_id(episode_id: str):
    return SeriesController.get_series_by_episode_id(episode_id)


@series_router.put("/update-series",
                   summary="Update Series Data. Admin Route",
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def update_series_data(series: SeriesSchemaIn, series_id: str):
    attributes = {key: value for key, value in vars(series).items() if value}
    return SeriesController.update_series_data(series_id, attributes)


@series_router.delete("/delete-series",
                      description="Delete series with all episodes.",
                      summary="Delete Series. Admin Route.",
                      dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_series(series_id: str):
    return SeriesController.delete_series(series_id)


episode_router = APIRouter(tags=["Episodes"], prefix="/api/episodes")


@episode_router.post("/add-new-episode",
                     response_model=EpisodeSchema,
                     summary="Create new Episode. Admin route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def create_new_episode(episode: EpisodeSchemaIn):
    return EpisodeController.create_episode(**episode.dict())


@episode_router.get("/get-all-episodes-for-series",
                    response_model=list[EpisodeSchema],
                    description="Get all episodes from a Series")
def get_all_episodes_for_series(series_title: str):
    episodes = EpisodeController.get_all_episodes_by_series(series_title)
    return episodes


@episode_router.get("/get-episode-by-id",
                    summary="Get episode by ID",
                    response_model=EpisodeSchema,
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_episode_by_id(episode_id: str):
    return EpisodeController.get_episode_by_id(episode_id)


@episode_router.put("/update-episode",
                    summary="Update Episode. Admin Route.",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=EpisodeSchema)
def update_episode(episode_id: str, episode: EpisodeSchemaIn):
    attributes = {key: value for key, value in vars(episode).items() if value}
    return EpisodeController.update_episode(episode_id, attributes)


@episode_router.delete("/delete-episode-by-id",
                       summary="Delete episode by ID. Admin Route.",
                       dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_episode(episode_id: str):
    return EpisodeController.delete_episode(episode_id)


series_actor_router = APIRouter(tags=["SeriesActors"], prefix="/api/series_actors")


@series_actor_router.post("/add-actor-to-series",
                          dependencies=[Depends(JWTBearer(["super_user"]))],
                          summary="Add actor to Series. Admin Route.")
def add_actor_to_series(series_id: str, actor_id: str):
    return SeriesActorController.create_series_actor(series_id, actor_id)


@series_actor_router.delete("/remove-actor-from-series",
                            dependencies=[Depends(JWTBearer(["super_user"]))],
                            summary="Remove actor from Series. Admin Route.")
def remove_actor_from_series(series_id: str, actor_id: str):
    return SeriesActorController.delete_series_actor(series_id, actor_id)


watch_episode = APIRouter(prefix="/api/watch_episode", tags=["Watch Episode"])


@watch_episode.post("/",
                    description="Select episode to watch",
                    status_code=status.HTTP_201_CREATED,
                    summary="Watch Episode. User Route.",
                    dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def user_watch_episode(request: Request, episode_name: str, series_title: str):
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_watch_episode(user_id, episode_name, series_title)


@watch_episode.put("/rate-episode",
                   response_model=UserWatchEpisodeSchema,
                   summary="Rate Episode. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def user_rate_episode(request: Request, episode_name: str, series_title: str, rating: int):
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_rate_episode(user_id, episode_name, series_title, rating)


@watch_episode.get("/get-my-series",
                   summary="Get my series. User Route.",
                   description="Get all series User watched",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_my_series(request: Request):
    user_id = request.cookies.get("user_id")
    return SeriesController.get_my_series(user_id)


@watch_episode.get("/search-series", response_model=list[SeriesWithActorsSchema], description="Search for Series")
def search_series_by_name(series: str):
    return SeriesController.get_series_by_name(series.strip())


@watch_episode.get("/get-series-data", summary="Get Series data.", response_model=SeriesFullSchema)
def get_series_data(title: str):
    return SeriesController.get_series_data(title.strip())


@watch_episode.get("/search-series-by-genre",
                   response_model=list[SeriesWithActorsSchema],
                   description="Search for Series")
def search_series_by_genre(genre: str):
    return SeriesController.get_series_by_genre(genre.strip())


@watch_episode.get("/search-series-by-director",
                   description="Search for Series by Director",
                   summary="Search Series by Director's Last Name.")
def get_series_by_director_name(director: str):
    return SeriesController.get_series_by_director_name(director.strip())


@watch_episode.get("/get-average-rating-for-series",
                   summary="Get average rating for specific Series. User Route",
                   )
def get_average_rating_for_series(title: str):
    return UserWatchEpisodeController.get_average_rating_for_series(title)


@watch_episode.get("/get-series-by-year",
                   response_model=list[SeriesSchema],
                   summary="Get Series by specific year. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_series_by_year(year: int):
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no series from provided year.")
    return SeriesController.get_series_by_year(year)


@watch_episode.get("/get-average-rating-series-by-year",
                   summary="Get average series rating for a specific year. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_average_series_rating_for_year(year: int):
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return UserWatchEpisodeController.get_average_series_rating_for_year(year)


@watch_episode.get("/get-popular-series", description="Get most popular Series.")
def get_most_popular_series():
    series = UserWatchEpisodeController.get_most_popular_series()
    sorted_series = {k: {"Views": v} for k, v in sorted(series.items(), key=lambda item: item[1], reverse=True)}
    return sorted_series


@watch_episode.get("/get-best-rated-episodes", description="Get best rated episodes.")
def get_best_rated_episodes():
    return EpisodeController.get_best_rated_episode()


@watch_episode.get("/get-worst-rated-episodes",
                   summary="Get worst rated episodes. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def get_worst_rated_episodes():
    return EpisodeController.get_best_rated_episode(best=False)


@watch_episode.get("/get-latest-features",
                   summary="Get latest features.",
                   description="Show recent released series.")
def get_latest_features():
    date_limit = get_day_before_one_month()
    return SeriesController.get_latest_features(date_limit)


@watch_episode.get("/show-series-never-downloaded",
                   summary="Show series that never have been watched. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def show_least_popular_series():
    return SeriesController.show_series_never_downloaded()


@watch_episode.get("/get-users-series-recommendations",
                   summary="Show Users recommendations. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))])
def get_users_series_recommendations(request: Request, page: int = 1):
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.get_users_recommendations(user_id, page)
