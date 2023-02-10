from app.base import BaseCRUDRepository
from app.users.exceptions import InvalidCredentialsException, InvalidVerificationCode
from app.users.models import User


class UserRepository(BaseCRUDRepository):
    """Repository for User Model"""

    def read_user_by_email(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                self.db.rollback()
                raise InvalidCredentialsException
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def search_users_by_email(self, email: str):
        try:
            users = self.db.query(User).filter(User.email.ilike(f"%{email}%")).all()
            return users
        except Exception as e:
            self.db.rollback()
            raise e

    def read_user_by_code(self, verification_code: int):
        try:
            user = self.db.query(User).filter(User.verification_code == verification_code).first()
            if not user:
                self.db.rollback()
                raise InvalidVerificationCode
            return user
        except Exception as e:
            self.db.rollback()
            raise e
