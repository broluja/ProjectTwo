from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository, AppException
from app.users.models import Subuser


class SubuserRepository(BaseCRUDRepository):
    """Repository for Subuser Model"""

    def create(self, attributes: dict):
        try:
            return super().create(attributes)
        except IntegrityError as _:
            self.db.rollback()
            raise AppException(message="Subuser Name already taken", code=400)

    def read_subusers_by_name(self, name: str, user_id: str):
        try:
            subuser = self.db.query(Subuser).filter(Subuser.name == name).filter(Subuser.user_id == user_id).first()
            return subuser
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)

    def read_subusers_by_user_id(self, user_id: str):
        try:
            subuser = self.db.query(Subuser).filter(Subuser.user_id == user_id).all()
            return subuser
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)
