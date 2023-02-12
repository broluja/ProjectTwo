from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.series.controller import SeriesController, EpisodeController
from app.series.schemas import SeriesSchemaIn, SeriesSchema, EpisodeSchema, EpisodeSchemaIn
from app.users.controller import JWTBearer

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
def get_all_episodes_from_series(series_id: str):
    return EpisodeController.get_all_episodes_by_series(series_id)
