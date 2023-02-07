from app.base import BaseCRUDRepository
from app.users.models import User
from app.base import AppException


class UserRepository(BaseCRUDRepository):
    """Repository for User Model"""

    def read_user_by_email(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                self.db.rollback()
                raise AppException(message=f"Login failed. Check your credentials.", code=401)
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def update_users_password(self):
        pass
