"""UserWatchEpisode Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.service import EpisodeServices, SeriesServices
from app.users.service import UserWatchEpisodeServices


class UserWatchEpisodeController:
    """Controller for User-Watch-Episode routes"""
    @staticmethod
    def user_watch_episode(user_id: str, name: str, series_title):
        """
        Function allows a user to watch an episode of a series.
        The function takes in the user_id, name and series_title as parameters.
        The function then checks if the episode exists in
        the database and returns it if it does exist.
        If not, it raises an exception with code 404.

        Param user_id:str: Identify the user.
        Param name:str: Get the name of the episode.
        Param series_title: Find the series with the given title.
        Return: The user-watch-episode object.
        """
        try:
            episode = EpisodeServices.get_episode_by_name_and_series(name, series_title)
            return UserWatchEpisodeServices.user_watch_episode(user_id, episode.id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def user_rate_episode(user_id: str, name: str, series_title: str, rating: int):
        """
        Function allows a user to rate an episode of a series.
        The function takes in the following parameters:
        - user_id: The ID of the user who is rating the episode.
        — name: The name of the episode being rated.
        — series_title: The title of the series that contains this episode.
        This parameter is used to find, which episodes exist for this show,
        and, which one matches with what was passed in as 'name'.

        Param user_id:str: Identify the user.
        Param name:str: Get the name of the episode.
        Param series_title:str: Get the series of the episode.
        Param rating:int: Specify the rating of a specific episode.
        Return: A rate episode object.
        """
        try:
            episode = EpisodeServices.get_episode_by_name_and_series(name, series_title)
            rate_episode = UserWatchEpisodeServices.rate_episode(user_id, episode.id, rating)
            return rate_episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_most_popular_series():
        """
        The get_most_popular_series function returns a list of series that have been watched the most.
        The function takes no arguments and returns a list of dictionaries, where each dictionary contains
        the name, number of views and average rating for each series.

        Return: A list of the most popular series.
        """
        try:
            series = UserWatchEpisodeServices.get_most_popular_series()
            return series if series else Response(
                content="We have not generated series popularity list yet.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_users_recommendations(user_id: str, page: int):
        """
        The get_users_recommendations function is used to get the recommendations for a specific user.
        It takes in two parameters, user_id and page. It returns a list of series objects
        that are recommended for the given user.

        Param user_id:str: Identify the user.
        Param page:int: Specify the page of the results.
        Return: A list of series recommended for a specific user.
        """
        try:
            series = UserWatchEpisodeServices.get_users_recommendations(user_id, page)
            return series if series else SeriesServices.read_all_series(page)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_average_series_rating_for_year(year: int):
        """
        The get_average_series_rating_for_year function returns the average rating for a given year.
        The function takes in a year as an argument and returns the average rating of all series from that year.

        Param year:int: Specify the year of the series you want to get average rating for.
        Return: The average rating for a series from a given year.
        """
        try:
            average = UserWatchEpisodeServices.get_average_series_rating_for_year(year)
            return average if average else Response(content=f"No Series from year: {year}.", status_code=200)

        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_average_rating_for_series(title: str):
        """
        The get_average_rating_for_series function returns the average rating for a given series.
        The function takes in a string title as an argument and returns the average rating of that series.

        Param title:str: Get the average rating for a specific series.
        Return: The average rating for a series.
        """
        try:
            return UserWatchEpisodeServices.get_average_rating_for_series(title)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
