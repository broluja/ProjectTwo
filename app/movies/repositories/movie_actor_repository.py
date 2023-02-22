"""Movie-Actor Repository module"""
from app.base import BaseCRUDRepository
from app.movies.models import MovieActor


class MovieActorRepository(BaseCRUDRepository):
    """Repository for Movie-Actor Model"""

    def read_by_movie(self, movie_id: str):
        """
        Function takes a movie_id as an argument and returns all the actors in that movie.
        It does this by querying the MovieActor table for all rows where the given movie_id matches
        the corresponding value in its column.

        Param self: Access the database
        Param movie_id:str: Filter the movie_actors table by the movie_id column
        Return: A list of movie-actor objects.
        """
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.movie_id == movie_id).all()
            return movie_actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_by_actor(self, actor_id: str):
        """
        Function accepts an actor_id as a parameter and returns all the movies that the actor has acted in.

        Param actor_id:str: Filter the query by actor_id.
        Return: A list of movie-actor objects.
        """
        try:
            movie_actors = self.db.query(MovieActor).filter(MovieActor.actor_id == actor_id).all()
            return movie_actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def delete_by_movie_id_and_actor_id(self, movie_id: str, actor_id: str):
        """
        Function deletes a movie-actor object from the database.
        It takes in two parameters, movie_id and actor_id, which are used to find the correct record to delete.
        The function then uses SQLAlchemy's session query method to execute the deletion.

        Param movie_id:str: Specify the movie_id of the movie-actor object to be deleted
        Param actor_id:str: Specify the actor_id of the movie_actor to be deleted
        Return: The movie-actor object.
        """
        try:
            movie_actor = self.db.query(MovieActor).filter(MovieActor.actor_id == actor_id).filter(
                MovieActor.movie_id == movie_id).first()
            self.db.delete(movie_actor)
            self.db.commit()
            self.db.refresh()
        except Exception as exc:
            self.db.rollback()
            raise exc
