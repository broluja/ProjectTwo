"""User Repository module"""
from sqlalchemy.exc import IntegrityError

from app.base import BaseCRUDRepository, AppException
from app.users.exceptions import InvalidCredentialsException, InvalidVerificationCode
from app.users.models import User


class UserRepository(BaseCRUDRepository):
    """Repository for User Model"""
    def create(self, attributes: dict):
        try:
            return super().create(attributes)
        except IntegrityError as exc:
            self.db.rollback()
            raise AppException(message="User with this email is already registered.", code=400) from exc

    def read_user_by_email(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                self.db.rollback()
                raise InvalidCredentialsException
            return user
        except Exception as exc:
            self.db.rollback()
            raise exc

    def search_users_by_email(self, email: str):
        try:
            users = self.db.query(User).filter(User.email.ilike(f"%{email}%")).all()
            return users
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_user_by_code(self, verification_code: int):
        try:
            user = self.db.query(User).filter(User.verification_code == verification_code).first()
            if not user:
                self.db.rollback()
                raise InvalidVerificationCode
            return user
        except Exception as exc:
            self.db.rollback()
            raise exc

    def read_all_active_users(self, active=True):
        try:
            users = self.db.query(User).filter(User.is_active == active).all()
            return users
        except Exception as exc:
            self.db.rollback()
            raise exc
