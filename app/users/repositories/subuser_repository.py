from app.base import BaseCRUDRepository, AppException
from app.users.models import Subuser


class SubuserRepository(BaseCRUDRepository):
    """Repository for Subuser Model"""

    def read_subusers_by_user_id(self, user_id: str):
        try:
            subusers = self.db.query(Subuser).filter(Subuser.user_id == user_id).all()
            return subusers
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)
