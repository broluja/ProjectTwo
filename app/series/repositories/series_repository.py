"""Series Repository module"""
from sqlalchemy import distinct

from app.base import BaseCRUDRepository
from app.config import settings
from app.series.models import Series, Episode
from app.users.models.user import UserWatchEpisode

PER_PAGE = settings.PER_PAGE


class SeriesRepository(BaseCRUDRepository):
    """Repository for Series Model"""

    def read_series_by_genre_id(self, genre_id: str):
        try:
            series = self.db.query(Series).filter(Series.genre_id == genre_id).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_director_id(self, director_id: str):
        try:
            series = self.db.query(Series).filter(Series.director_id == director_id).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_title(self, title: str, search: bool = False):
        try:
            if search:
                series = self.db.query(Series).filter(Series.title.ilike(f"%{title}%")).all()
            else:
                series = self.db.query(Series).filter(Series.title == title).first()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_year(self, year):
        try:
            series = self.db.query(Series).filter(Series.year_published == year).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_episode_id(self, episode_id):
        try:
            series = self.db.query(Series).join(Episode).filter(Episode.id == episode_id).first()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_latest_releases(self, date_limit: str):
        try:
            series = self.db.query(Series).filter(Series.date_added >= date_limit).all()
            return series
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_least_popular_series(self):
        try:
            sub1 = self.db.query(distinct(UserWatchEpisode.episode_id.label('episode'))).subquery('sub1')
            sub2 = self.db.query(Series.id).join(Episode).filter(
                Series.id == Episode.series_id).filter(Episode.id.in_(sub1)).distinct().subquery('sub2')
            result = self.db.query(Series.id, Series.title).filter(Series.id.not_in(sub2))
            return result
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_series_by_group_of_genres(self, page, genres):
        try:
            skip = (page - 1) * PER_PAGE
            movies = self.db.query(Series).filter(Series.genre_id.in_(genres)).offset(skip).limit(PER_PAGE).all()
            return movies
        except Exception as exc:
            self.db.rollback()
            raise exc
