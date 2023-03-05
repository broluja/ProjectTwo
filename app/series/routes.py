"""Series and episodes routes"""
from fastapi import APIRouter, Depends, status, HTTPException, Body, Query
from starlette.requests import Request

from app.series.controller import SeriesController, EpisodeController
from app.series.controller.series_actor_controller import SeriesActorController
from app.series.schemas import *
from app.users.controller import JWTBearer
from app.users.controller.user_watch_episode_controller import UserWatchEpisodeController
from app.users.schemas.user_watch_episode_schema import UserWatchEpisodeSchema
from app.utils import get_day_before_one_month

series_router = APIRouter(tags=["Series"], prefix="/api/series")


@series_router.post("/",
                    summary="Create new Series. Admin Route.",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=SeriesWithDirectorAndGenreSchema,
                    status_code=status.HTTP_201_CREATED
                    )
def create_new_series(series: SeriesSchemaIn):
    """
    The create_new_series function creates a new series in the database.
    It takes as input a SeriesSchemaIn object, which is defined in the schemas.py file
    and contains all the fields necessary to create a new series.

    Param series:SeriesSchemaIn: Pass the schema of the series that is going to be created
    Return: A series-schema-out object.
    """
    return SeriesController.create_series(**series.dict())


@series_router.get("/", response_model=list[SeriesWithActorsSchema])
def get_all_series(page: int = 1):
    """
    Function returns a list of all series in the database.
    It takes an optional parameter, page, which defaults to 1.
    The get_all_series function returns a list of all series in the database.

    Param page:int=1: Define the page number of the series that will be returned.
    Return: A list of series objects.
    """
    return SeriesController.read_all_series(page)


@series_router.get("/get-series/episode-id",
                   summary="Get Series using ID. Admin Route",
                   dependencies=[Depends(JWTBearer(["super_user"]))]
                   )
def get_series_by_episode_id(episode_id: str):
    """
    Function returns a series object given an episode ID.

    Param episode_id:str: Get the series with the given ID.
    Return: A series object.
    """
    return SeriesController.get_series_by_episode_id(episode_id)


@series_router.put("/",
                   summary="Update Series Data. Admin Route",
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def update_series_data(series: SeriesSchemaIn, series_id: str):
    """
    The update_series_data function updates the data for a given series.

    Param series:SeriesSchemaIn: Validate the data that is passed in.
    Param series_id:str: Identify the series to be updated.
    Return: The updated series data.
    """
    attributes = {key: value for key, value in vars(series).items() if value}
    return SeriesController.update_series_data(series_id, attributes)


@series_router.delete("/",
                      summary="Delete Series. Admin Route.",
                      dependencies=[Depends(JWTBearer(["super_user"]))]
                      )
def delete_series(series_id: str = Body(embed=True)):
    """
    Function deletes a series from the database.

    Param series_id:str: Specify, which series to delete
    Return: A string.
    """
    return SeriesController.delete_series(series_id)


episode_router = APIRouter(tags=["Episodes"], prefix="/api/episodes")


@episode_router.post("/",
                     response_model=EpisodeSchema,
                     summary="Create new Episode. Admin route.",
                     dependencies=[Depends(JWTBearer(["super_user"]))],
                     status_code=status.HTTP_201_CREATED
                     )
def create_new_episode(episode: EpisodeSchemaIn):
    """
    The create_new_episode function creates a new episode in the database.
    It takes an EpisodeSchemaIn object as input, and returns an EpisodeSchemaOut object.

    Param episode:EpisodeSchemaIn: Create a new episode.
    Return: A dict.
    """
    return EpisodeController.create_episode(**episode.dict())


@episode_router.get("/get-all-episodes-for-series", response_model=list[EpisodeSchema])
def get_all_episodes_for_series(series_title: str):
    """
    The get_all_episodes_for_series function returns all episodes for a given series.
    The function takes one argument, the title of the series to be searched.
    It returns a list of dictionaries containing episode information.

    Param series_title:str: Search for a series by its title.
    Return: A list of all the episodes for a given series.
    """
    return EpisodeController.get_all_episodes_by_series(series_title)


@episode_router.get("/get-episode/id",
                    summary="Get episode by ID. Admin Route",
                    response_model=EpisodeSchema,
                    dependencies=[Depends(JWTBearer(["super_user"]))]
                    )
def get_episode_by_id(episode_id: str):
    """
    Function takes an episode ID as a parameter and returns the corresponding episode.


    Param episode_id:str: Identify the episode to be returned
    Return: A dictionary with the episode information.
    """
    return EpisodeController.get_episode_by_id(episode_id)


@episode_router.put("/",
                    summary="Update Episode. Admin Route.",
                    dependencies=[Depends(JWTBearer(["super_user"]))],
                    response_model=EpisodeSchema,
                    status_code=status.HTTP_201_CREATED
                    )
def update_episode(episode: EpisodeSchemaIn, episode_id: str = Body(embed=True)):
    """
    Function updates an existing episode in the database.

    Param episode_id:str: Identify the episode that is to be updated.
    Param episode:EpisodeSchemaIn: Specify the schema of the episode object that is being passed in.
    Return: The updated episode.
    """
    attributes = {key: value for key, value in vars(episode).items() if value}
    return EpisodeController.update_episode(episode_id, attributes)


@episode_router.delete("/",
                       summary="Delete episode by ID. Admin Route.",
                       dependencies=[Depends(JWTBearer(["super_user"]))]
                       )
def delete_episode(episode_id: str = Body(embed=True)):
    """
    Function deletes an episode from the database.

    Param episode_id:str: Specify the episode_id of the episode that is to be deleted
    Return: A boolean value.
    """
    return EpisodeController.delete_episode(episode_id)


series_actor_router = APIRouter(tags=["SeriesActors"],
                                prefix="/api/series-actors",
                                dependencies=[Depends(JWTBearer(["super_user"]))]
                                )


@series_actor_router.post("/", summary="Add actor to Series. Admin Route.", status_code=status.HTTP_201_CREATED)
def add_actor_to_series(series_id: str = Body(embed=True), actor_id: str = Body(embed=True)):
    """
    Function adds an actor to a series.

    Param series_id:str: Specify the series that the actor will be added to.
    Param actor_id:str: Specify, which actor to add to the series.
    Return: A series-actor object.
    """
    return SeriesActorController.create_series_actor(series_id, actor_id)


@series_actor_router.delete("/", summary="Remove actor from Series. Admin Route.")
def remove_actor_from_series(series_id: str = Body(embed=True), actor_id: str = Body(embed=True)):
    """
    Function removes an actor from a series.

    Param series_id:str: Specify, which series the actor is being removed from.
    Param actor_id:str: Identify the actor to be removed from the series.
    Return: A message that says the actor was removed from the series.
    """
    return SeriesActorController.delete_series_actor(series_id, actor_id)


watch_episode = APIRouter(prefix="/api/watch-episode", tags=["Watch Episode"])


@watch_episode.post("/",
                    status_code=status.HTTP_201_CREATED,
                    summary="Watch Episode. User Route.",
                    dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                    )
def user_watch_episode(request: Request, episode_name: str = Body(embed=True), series_title: str = Body(embed=True)):
    """
    The user_watch_episode function is used to add a user's watch history to the database.
    It takes in a request, episode name and series title as parameters. It then checks if the user_id cookie exists,
    and if it does it add that information into the database.

    Param request:Request: Get the user_id from the cookies.
    Param episode_name:str: Get the name of the episode that is being watched.
    Param series_title:str: Get the series title of the episode.
    Return: A response object.
    """
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_watch_episode(user_id, episode_name, series_title)


@watch_episode.patch("/rate-episode",
                     response_model=UserWatchEpisodeSchema,
                     summary="Rate Episode. User Route.",
                     dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))],
                     status_code=status.HTTP_201_CREATED
                     )
def user_rate_episode(request: Request,
                      episode_name: str = Body(embed=True),
                      series_title: str = Body(embed=True),
                      rating: int = Body(embed=True)):
    """
    Function allows a user to rate an episode of a series.
    The function takes in the name of the episode, the title of the series it belongs to,
    and what rating they want to give it.
    It returns whether their rating was successful.

    Param request:Request: Get the user_id from the cookie
    Param episode_name:str: Get the name of the episode that is being rated
    Param series_title:str: Get the series_id from the database and then pass it to user_rate_episode
    Param rating:int: Specify the rating of the episode
    Return: A dictionary.
    """
    if not 0 < rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.user_rate_episode(user_id, episode_name, series_title, rating)


@watch_episode.get("/get-my-series",
                   summary="Get my series. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                   )
def get_my_series(request: Request):
    """
    Function returns a list of all the series that belong to the user.
    The function takes in a request object as an argument and uses the cookies to get
    the user_id. The function then calls SeriesController's get_my_series method, which
    returns a list of all series belonging to that user.

    Param request:Request: Get the user_id from the cookie
    Return: A list of all the series that have been created by the user.
    """
    user_id = request.cookies.get("user_id")
    return SeriesController.get_my_series(user_id)


@watch_episode.get("/search-series",
                   response_model=list[SeriesWithActorsSchema]
                   )
def search_series_by_name(series: str):
    """
    Function searches for a series by name and returns the Series object.
    The search_series_by_name function accepts one argument, series,
    which is the name of the series to be searched.


    Param series:str: Specify the name of the series that is being searched for.
    Return: A list of series objects that match the search criteria.
    """
    return SeriesController.get_series_by_name(series.strip(), search=True)


@watch_episode.get("/get-series/data",
                   summary="Get Series data.",
                   response_model=SeriesFullSchema
                   )
def get_series_data(title: str):
    """
    Function takes a string as an argument and returns the data for that series.
    If no such series exists, it returns None.

    Param title:str: Get the title of the series
    Return: A dictionary of the data for a given series.
    """
    return SeriesController.get_series_data(title.strip())


@watch_episode.get("/search-series/genre",
                   response_model=list[SeriesWithActorsSchema]
                   )
def search_series_by_genre(genre: str):
    """
    Function takes a string as an argument and returns all series that have the genre
    specified by the string.

    Param genre:str: Search for series by a genre
    Return: A list of series that match the genre.
    """
    return SeriesController.get_series_by_genre(genre.strip())


@watch_episode.get("/search-series/director",
                   summary="Search Series by Director's Last Name.",
                   response_model=list[SeriesWithDirectorSchema])
def get_series_by_director_name(
        choice: str = Query("Last Name", enum=["First Name", "Last Name", "Country"]),
        query: str = ""
):
    """
    Function takes a director first, last name or country as an argument
    and returns all the series that have director with those queries.
    The function first strips any whitespace from the inputted string

    Param choice:str: Specify the criteria to query.
    Param query: str: Query to search for.
    Return: A list of series objects.
    """
    match choice:
        case "First Name":
            return SeriesController.get_series_by_director_first_name(query.strip())
        case "Last Name":
            return SeriesController.get_series_by_director_last_name(query.strip())
        case "Country":
            return SeriesController.get_series_by_director_country(query.strip())


@watch_episode.get("/get-average-rating-for-series",
                   summary="Get average rating for specific Series. User Route",
                   )
def get_average_rating_for_series(title: str):
    """
    Function returns the average rating for a given series.
    The function takes one argument, title, which is the name of the series to be rated.

    Param title:str: Pass the title of the series that is being rated.
    Return: The average rating for a series.
    """
    return UserWatchEpisodeController.get_average_rating_for_series(title)


@watch_episode.get("/get-series/year",
                   response_model=list[SeriesSchema],
                   summary="Get Series by specific year. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                   )
def get_series_by_year(year: int):
    """
    Function returns a list of series that were first aired in the provided year.
    If no series were first aired in the provided year, an empty list is returned.

    Param year:int: Filter the series by year
    Return: A list of dictionaries containing the data for all series that were active during the given year.
    """
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no series from provided year.")
    return SeriesController.get_series_by_year(year)


@watch_episode.get("/get-average-rating-series-by-year",
                   summary="Get average series rating for a specific year. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                   )
def get_average_series_rating_for_year(year: int):
    """
    The get_average_series_rating_for_year function returns the average rating for a series in a given year.
    The function takes one argument, year, which is an integer between 1900 and 2100.

    Param year:int: Filter the data from the database.
    Return: The average rating of the series that were watched in a given year.
    """
    if not 1900 < year < 2100:
        raise HTTPException(status_code=200, detail="Sorry, we have no movies from provided year.")
    return UserWatchEpisodeController.get_average_series_rating_for_year(year)


@watch_episode.get("/get-popular-series", description="Get most popular Series.")
def get_most_popular_series():
    """
    The get_most_popular_series function returns a dictionary of the most popular series in the database.
    The function sorts the series by number of views and returns a dictionary with each key being a
    series name and its value being how many times it has been viewed.

    Return: A sorted dictionary of series, and their number of views.
    """
    series = UserWatchEpisodeController.get_most_popular_series()
    return {k: {"Views": v} for k, v in sorted(series.items(), key=lambda item: item[1], reverse=True)}


@watch_episode.get("/get-best-rated-episodes", description="Get best rated episodes.")
def get_best_rated_episodes():
    """
    Function returns the best rated episodes.

    Return: A list of the best rated episodes.
    """
    return EpisodeController.get_best_rated_episode()


@watch_episode.get("/get-worst-rated-episodes",
                   summary="Get worst rated episodes. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))]
                   )
def get_worst_rated_episodes():
    """
    The get_worst_rated_episodes function returns a list of episodes with the lowest rating.

    Return: A list of episodes with the lowest rating.
    """
    return EpisodeController.get_best_rated_episode(best=False)


@watch_episode.get("/get-latest-features",
                   summary="Get latest features."
                   )
def get_latest_features():
    """
    Function returns a list of the latest features that have been added to the database.
    The function takes no arguments and returns a list of dictionaries,
    where each dictionary contains information about one feature.

    Return: A series object containing the latest features.
    """
    date_limit = get_day_before_one_month()
    return SeriesController.get_latest_features(date_limit)


@watch_episode.get("/show-series-never-downloaded",
                   summary="Show series that never have been watched. Admin Route.",
                   dependencies=[Depends(JWTBearer(["super_user"]))]
                   )
def show_least_popular_series():
    """
    Function returns a list of the least popular series.
    The function takes no arguments and returns a list of Series objects.

    Return: A list of series that have never been downloaded.
    """
    return SeriesController.show_series_never_downloaded()


@watch_episode.get("/get-users-series-recommendations",
                   summary="Show Users recommendations. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user", "sub_user"]))]
                   )
def get_users_series_recommendations(request: Request, page: int = 1):
    """
    Function is used to get the recommendations for a specific user.
    It takes in a request and page number and returns an array of
    dictionaries containing the series objects.

    Param request:Request: Get the user_id from the cookies.
    Param page:int=1: Specify the page number to be returned.
    Return: A list of recommendations for the user.
    """
    user_id = request.cookies.get("user_id")
    return UserWatchEpisodeController.get_users_recommendations(user_id, page)
