from app.users.repositories import UserRepository, SubuserRepository
from app.db.database import SessionLocal
from app.users.models import User, Subuser
from app.users.exceptions import InvalidCredentialsException, UnverifiedAccountException, InactiveUserException


class UserServices:

    @staticmethod
    def create_new_user(email, password, username, code: int):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                fields = {"email": email, "password_hashed": password, "username": username, "verification_code": code}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def verify_user(verification_code: int):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_code(verification_code)
                if user:
                    obj = repository.update(user, {"verification_code": None})
                return obj
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
    def get_all_active_users(active=True):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_all_active_users(active=active)
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_id(user_id: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_by_id(user_id)
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def get_user_by_email(email: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.read_user_by_email(email)
        except Exception as e:
            raise e

    @staticmethod
    def search_users_by_email(email: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                return repository.search_users_by_email(email)
        except Exception as e:
            raise e

    @staticmethod
    def login_user(email: str, password: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_email(email)
                if user.password_hashed != password:
                    raise InvalidCredentialsException
                if user.verification_code is not None:
                    raise UnverifiedAccountException
                if not user.is_active:
                    raise InactiveUserException
                return user
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
    def change_user_status(user_id: str, activity=False):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"is_active": activity}
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
    def generate_verification_code(user_id, code: int):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = UserServices.get_user_by_id(user_id)
                updates = {"verification_code": code}
                return repository.update(user, updates)
        except Exception as e:
            raise e

    @staticmethod
    def reset_password_complete(code: int, password_hashed: str):
        try:
            with SessionLocal() as db:
                repository = UserRepository(db, User)
                user = repository.read_user_by_code(code)
                updates = {"password_hashed": password_hashed, "verification_code": None}
                return repository.update(user, updates)
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(user_id: str):
        try:
            with SessionLocal() as db:
                subuser_repo = SubuserRepository(db, Subuser)
                subs = subuser_repo.read_subusers_by_user_id(user_id)
                user_repo = UserRepository(db, User)
                if subs:
                    for sub in subs:
                        subuser_repo.delete(sub.id)
                return user_repo.delete(user_id)
        except Exception as e:
            raise e
