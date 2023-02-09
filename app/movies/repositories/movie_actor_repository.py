from app.base import BaseCRUDRepository
from app.movies.models import MovieActor


class MovieActorRepository(BaseCRUDRepository):
    """Repository for Movie-Actor Model"""

    def read_by_movie(self, movie_id: str):
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.movie_id == movie_id).all()
            return movie_actors
        except Exception as e:
            self.db.rollback()
            raise e

    def read_by_actor(self, actor_id: str):
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.actor_id == actor_id).all()
            return movie_actors
        except Exception as e:
            self.db.rollback()
            raise e
