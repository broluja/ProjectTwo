from app.base import BaseCRUDRepository, AppException
from app.users.models import Admin


class AdminRepository(BaseCRUDRepository):
    """Repository for Admin Model"""

    def read_admins_by_country(self, country: str):
        try:
            admins = self.db.query(Admin).filter(Admin.country == country).all()
            return admins
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)
