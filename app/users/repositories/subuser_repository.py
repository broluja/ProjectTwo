from app.base import BaseCRUDRepository, AppException
from app.users.models import Subuser


class SubuserRepository(BaseCRUDRepository):
    """Repository for Subuser Model"""

    def read_subusers_by_name(self, name: str):
        try:
            subuser = self.db.query(Subuser).filter(Subuser.name == name).first()
            return subuser
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)
