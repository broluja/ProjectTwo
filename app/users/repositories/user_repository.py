from app.base.base_repository import BaseCRUDRepository
from app.users.models import User
from app.base import AppException


class UserRepository(BaseCRUDRepository):
    """Repository for User Model"""

    def update_users_password(self):
        pass

    def read_user_by_username_and_password(self, email: str, password_hashed: str):
        try:
            user = self.db.query(User).filter(User.email == email).filter(User.password_hashed == password_hashed).first()
            if not user:
                self.db.rollback()
                raise AppException(message=f"Login failed. Check your credentials.", code=400)
            return user
        except Exception as e:
            self.db.rollback()
            raise e
