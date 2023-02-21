"""Admin Repository module"""
from app.base import BaseCRUDRepository, AppException
from app.users.models import Admin


class AdminRepository(BaseCRUDRepository):
    """Repository for Admin Model"""

    def read_admins_by_country(self, country: str):
        try:
            admins = self.db.query(Admin).filter(Admin.country == country).all()
            return admins
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc
