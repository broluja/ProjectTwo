"""UserWatchEpisode Service module"""
from starlette.responses import Response

from app.db import SessionLocal
from app.series.exceptions.series_exceptions import UnknownSeriesException
from app.series.models import Episode, Series
from app.series.repositories import EpisodeRepository, SeriesRepository
from app.users.models.user import UserWatchEpisode
from app.users.repositories import UserWatchEpisodeRepository


class UserWatchEpisodeServices:
    """Service for UserWatchEpisode routes."""
    @staticmethod
    def user_watch_episode(user_id: str, episode_id: str):
        """
        Function allows a user to watch an episode of the show.
        It takes in two parameters, user_id and episode_id. It then checks if
        the user has already watched this particular episode,
        if they have it will return a message saying that they have already watched
        it and where to find it again. If not,
        it will create a new entry in the UserWatchEpisode table with their ID and the ID
        of the specific episode they are watching.

        Param user_id:str: Identify the user.
        Param episode_id:str: Get the episode object from the database.
        Return: A dictionary containing a message and link.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                episode_repo = EpisodeRepository(db, Episode)
                episode = episode_repo.read_by_id(episode_id)
                if watched_episode:
                    return {"message": "Watch episode again.", "link": episode.link}
                fields = {"user_id": user_id, "episode_id": episode_id}
                repository.create(fields)
                return {"message": "Watch this episode now.", "link": episode.link}
        except Exception as exc:
            raise exc

    @staticmethod
    def rate_episode(user_id: str, episode_id: str, rating: int):
        """
        Function allows a user to rate an episode.

        Param user_id:str: Identify the user.
        Param episode_id:str: Get the episode object from the database.
        Param rating:int: Set the rating of an episode.
        Return: The updated object.
        """
        try:
            with SessionLocal() as db:
                repository = UserWatchEpisodeRepository(db, UserWatchEpisode)
                watched_episode = repository.read_user_watch_episode_by_user_id_and_episode_id(user_id, episode_id)
                if watched_episode:
                    obj = repository.update(watched_episode, {"rating": rating})
                    return obj
                fields = {"user_id": user_id, "episode_id": episode_id, "rating": rating}
                return repository.create(fields)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_most_popular_series():
        """
        Function returns a dictionary of the most popular series by number of views.
        The function takes no arguments and returns a dictionary with the title as key and number of views as value.

        Return: A dictionary of series and views.
        """
        try:
            with SessionLocal() as db:
                repo = UserWatchEpisodeRepository(db, UserWatchEpisode)
                episodes = repo.read_episode_views()
                series_repo = SeriesRepository(db, Series)
                response = {}
                for series_id, views in episodes:
                    series = series_repo.read_by_id(series_id)
                    response.update({series.title: views})
                return response
        except Exception as exc:
            raise exc

    @staticmethod
    def get_users_recommendations(user_id: str, page: int):
        """
        Function returns a list of series that are recommended for the user based on their
        affinities. The function takes in a user_id and page number as the parameters, and uses
        them to query the database for the users affinities. It then uses those affinities to
        find all series with those genres, and returns them in order of popularity.

        Param user_id:str: Identify the user that we want to recommend series for.
        Param page:int: Paginate the results.
        Return: A list of series that are recommended to the user.
        """
        try:
            with SessionLocal() as db:
                user_watch_episode_repo = UserWatchEpisodeRepository(db, UserWatchEpisode)
                users_affinities = user_watch_episode_repo.read_users_affinities(user_id)
                series_repo = SeriesRepository(db, Series)
                genres = [affinity.Genre_ID for affinity in users_affinities]
                return series_repo.read_series_by_group_of_genres(page, genres)
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_series_rating_for_year(year: int):
        """
        The get_average_series_rating_for_year function returns the average rating for a given year.
        The function takes in a year as an argument and queries the database to find all series from that year.
        It then finds all episodes from those series and gets their average rating.

        Param year:int: Filter the series by a year.
        Return: The average rating for a given year.
        """
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_year(str(year))
                if not series:
                    return Response(content=f"No Series from this year: {year}", status_code=200)
                episode_ids = [episode.id for obj in series for episode in obj.episodes]
                user_watch_episode_repo = UserWatchEpisodeRepository(db, Episode)
                episodes_avg = user_watch_episode_repo.read_average_rating(episode_ids)
                average = round(sum(obj.avg for obj in episodes_avg) / len(episodes_avg), 2)
                return {"Year": year, "Average Rating": average}
        except Exception as exc:
            raise exc

    @staticmethod
    def get_average_rating_for_series(title: str):
        """
        The get_average_rating_for_series function returns the average rating for a given series.
        The function takes one argument, title, which is the name of the series to be queried.
        The function returns a dictionary containing two keys: Series and Average Rating.

        Param title:str: Search for the series.
        Return: A dictionary with the series title and average rating.
        """
        try:
            with SessionLocal() as db:
                series_repository = SeriesRepository(db, Series)
                series = series_repository.read_series_by_title(title, search=False)
                if not series:
                    raise UnknownSeriesException
                episode_ids = [episode.id for episode in series.episodes]
                user_watch_episode_repo = UserWatchEpisodeRepository(db, Episode)
                episodes_avg = user_watch_episode_repo.read_average_rating(episode_ids)
                average = round(sum(obj.avg for obj in episodes_avg) / len(episodes_avg), 2)
                return {"Series": series.title, "Average Rating": average}
        except Exception as exc:
            raise exc
