"""Admin Repository module"""
from app.base import BaseCRUDRepository, AppException
from app.users.models import Admin, User


class AdminRepository(BaseCRUDRepository):
    """Repository for Admin Model"""

    def read_admins_by_country(self, country: str):
        """
        The read_admins_by_country function accepts a country name as an argument and returns all
        the admins in that country. It first queries the database for all admins with a given country,
        then it converts them to JSON format using the AdminSchema and finally returns them.

        Param self: Access the database connection.
        Param country:str: Filter the admins by country.
        Return: A list of admin objects.
        """
        try:
            return self.db.query(Admin).filter(Admin.country == country).all()
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc

    def read_admin_by_user_id(self, user_id: str):
        try:
            return self.db.query(Admin).filter(User.id == user_id).first()
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc
