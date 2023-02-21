"""Actor Repository module"""
from app.actors.models import Actor
from app.base import BaseCRUDRepository


class ActorRepository(BaseCRUDRepository):
    """Repository for Actor Model"""

    def read_actors_by_first_name(self, first_name: str, search: bool = True):
        try:
            if search:
                actors = self.db.query(Actor).filter(Actor.first_name.ilike(f"%{first_name}%")).all()
            else:
                actors = self.db.query(Actor).filter(Actor.first_name == first_name).first()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_actors_by_last_name(self, last_name: str, literal=False):
        try:
            if literal:
                actors = self.db.query(Actor).filter(Actor.last_name == last_name).first()
            else:
                actors = self.db.query(Actor).filter(Actor.last_name.ilike(f"%{last_name}%")).all()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_actors_by_country(self, country: str):
        try:
            actors = self.db.query(Actor).filter(Actor.country == country).all()
            return actors
        except Exception as exc:
            self.db.rollback()
            raise exc
