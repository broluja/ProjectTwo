from app.users.repositories import UserRepository
from app.db.database import SessionLocal
from app.users.models import User


class UserServices:

    @staticmethod
    def create_new_user(email, password, username):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                fields = {"email": email, "password_hashed": password, "username": username}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_users():
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_all()
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_id(user_id: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_by_id(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_email_and_password(email: str, password: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_user_by_username_and_password(email, password)
        except Exception as e:
            raise e

    @staticmethod
    def update_username(user_id: str, username: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"username": username}
                return repository.update(user, updates)
        except Exception as e:
            raise e

    @staticmethod
    def update_admin_status(user_id, superuser=True):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"is_superuser": superuser}
                return repository.update(user, updates)
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(user_id: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.delete(user_id)
        except Exception as e:
            raise e
