"""Movie-Actor Repository module"""
from app.base import BaseCRUDRepository
from app.movies.models import MovieActor


class MovieActorRepository(BaseCRUDRepository):
    """Repository for Movie-Actor Model"""

    def read_by_movie(self, movie_id: str):
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.movie_id == movie_id).all()
            return movie_actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_actor(self, actor_id: str):
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.actor_id == actor_id).all()
            return movie_actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def delete_by_movie_id_and_actor_id(self, movie_id: str, actor_id: str):
        try:
            movie_actor = self.db.query(MovieActor).filter(MovieActor.actor_id == actor_id).filter(
                MovieActor.movie_id == movie_id).first()
            self.db.delete(movie_actor)
            self.db.commit()
            self.db.refresh()
        except Exception as exc:
            self.db.rollback()
            raise exc
