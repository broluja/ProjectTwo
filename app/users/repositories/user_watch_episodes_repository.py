"""UserWatchEpisode Repository module"""
from sqlalchemy import func
from sqlalchemy.orm import aliased

from app.base import BaseCRUDRepository
from app.genres.models import Genre
from app.series.models import Episode, Series
from app.users.models.user import UserWatchEpisode


class UserWatchEpisodeRepository(BaseCRUDRepository):
    """Repository for UserWatchEpisode Model"""
    def read_user_watch_episode_by_user_id_and_episode_id(self, user_id: str, episode_id: str):
        """
        Function is used to retrieve a UserWatchEpisode object from the database.
        It takes two parameters, user_id and episode_id, which are both strings.
        It then queries the database for an object with matching user_id and episode_id values.
        If it finds one, it returns that object; if not, it returns None.

        Param user_id:str: Specify the user_id of the user that we want to retrieve.
        Param episode_id:str: Identify the episode that is being watched by the user.
        Return: The user_watch_episode object.
        """
        try:
            user_watch_episode = self.db.query(UserWatchEpisode).filter(UserWatchEpisode.user_id == user_id).filter(
                UserWatchEpisode.episode_id == episode_id).first()
            return user_watch_episode
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_user_id(self, user_id: str):
        """
        Function takes a user_id as an argument and returns all the episodes that have been watched by
        the user with the given ID. It does this by querying the UserWatchEpisode table in our database,
        filtering it based on the given user_id, and returning all of those results.

        Param user_id:str: Filter the query by user_id
        Return: A list of user-watch-episode objects.
        """
        try:
            episodes = self.db.query(UserWatchEpisode).filter(UserWatchEpisode.user_id == user_id).all()
            return episodes
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_users_episodes_and_series(self, user_id: str):
        """
        Function takes a user_id as an argument and returns a list of tuples.
        Each tuple contains the episode ID, series ID, and title for each episode that the user has watched.

        Param user_id:str: Filter the results by user.
        Return: A list of tuples.
        """
        try:
            series = self.db.query(UserWatchEpisode, Episode.series_id, Series.title) \
                .join(Episode, Episode.id == UserWatchEpisode.episode_id) \
                .join(Series, Episode.series_id == Series.id) \
                .filter(UserWatchEpisode.user_id == user_id).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_episode_views(self):
        """
        Function returns a list of series, and the number of users who have watched each episode in that
        series. The function first queries the UserWatchEpisode table for all user_id's and episode_id's,
        then joins this query with
        the Episode table to get the series_id associated with each user-episode pair. It then creates a
        subquery from this join, which is used to create another subquery, which counts how many
        times each unique (user, series) pair appears in the original
        subquery. This second subquery is grouped by its series value so that we can count how many users
        watched episodes from.

        Return: A query object.
        """
        try:
            subquery = self.db.query(UserWatchEpisode.user_id.label('user'),
                                     UserWatchEpisode.episode_id.label('episode'), Episode.series_id.label('series')) \
                .join(Episode, Episode.id == UserWatchEpisode.episode_id).subquery('sq')
            sq = aliased(subquery)
            subquery2 = self.db.query(sq.c.user, sq.c.series.label('series_two')).distinct().subquery('sq2')
            sq2 = aliased(subquery2)
            result = self.db.query(sq2.c.series_two, func.count(sq2.c.series_two)).group_by(sq2.c.series_two)
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_best_rated_episode(self, best: bool = True):
        """
        Function returns the episode with the highest rating.
        The function takes one parameter, best, which is a boolean value that defaults to True.
        If best is set to False then it will return the episode with the lowest rating.

        Param best:bool=True: Determine whether the best or worst rated episode should be returned.
        Return: The episode with the highest rating.
        """
        try:
            if best:
                subquery = self.db.query(UserWatchEpisode.episode_id.label("episode"),
                                         func.avg(UserWatchEpisode.rating).label("rating")).group_by(
                    UserWatchEpisode.episode_id.label("episode")).subquery()
                max_rating = self.db.query(func.max(subquery.c.rating.label("rating")))
                episode = self.db.query(subquery.c.episode.label("episode"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == max_rating)
            else:
                subquery = self.db.query(UserWatchEpisode.episode_id.label("episode"),
                                         func.avg(UserWatchEpisode.rating).label("rating")).group_by(
                    UserWatchEpisode.episode_id.label("episode")).subquery()
                min_rating = self.db.query(func.min(subquery.c.rating.label("rating")))
                episode = self.db.query(subquery.c.episode.label("episode"), subquery.c.rating.label("rating")).filter(
                    subquery.c.rating.label("rating") == min_rating)
            return episode
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_users_affinities(self, user_id: str):
        """
        Function takes a user_id as an argument and returns the genres that the user has
        watched. The function first queries UserWatchEpisode table to get all episodes that have been
        watched by a specific user. Then it joins Episode table with Series table on Episode.series_id = Series.id,
        then joins Genre table with Series table on Genre.id = Series.genre_id, and finally filters out
        only unique genre IDs from the query results.

        Param user_id:str: Filter the query by a specific user.
        Return: A list of tuples.
        """
        try:
            sq = self.db.query(UserWatchEpisode.episode_id, Genre.id.label("Genre_ID")). \
                join(Episode, UserWatchEpisode.episode_id == Episode.id). \
                join(Series, Series.id == Episode.series_id).\
                join(Genre, Series.genre_id == Genre.id).filter(UserWatchEpisode.user_id == user_id).subquery('sq')
            result = self.db.query(sq.c.Genre_ID).distinct().all()
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_average_rating(self, episode_ids: list):
        """
        Function takes a list of episode IDS and returns the average rating for each
        episode in the list. The function first queries UserWatchEpisode to get all ratings for episodes in the
        list, then groups them by episode ID and finds their average. Finally, it returns that value.

        Param episode IDs:list: Pass in a list of episode IDs to the function.
        Return: The average rating of the episodes in episode_ids.
        """
        try:
            averages = self.db.query(UserWatchEpisode.rating.label("Rating")).\
                filter(UserWatchEpisode.episode_id.in_(episode_ids)).\
                group_by(UserWatchEpisode.episode_id).\
                subquery('averages')
            result = self.db.query(func.round(func.avg(averages.c.Rating), 2).label("Average Rating")).first()
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc
