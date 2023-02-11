from app.users.repositories import SubuserRepository
from app.users.service import UserServices
from app.db.database import SessionLocal
from app.users.models import Subuser
from app.users.exceptions import NonExistingUserIdException, MaxLimitSubusersException, AdminSubuserException, \
    UnknownProfileException

MAX_NUMBER_SUBUSERS = 2


class SubuserServices:

    @staticmethod
    def create_new_subuser(user_id, name):
        try:
            with SessionLocal() as db:
                user = UserServices.get_user_by_id(user_id)
                if not user:
                    raise NonExistingUserIdException(message=f"Non existing User ID: {user_id}", code=400)
                elif user.is_superuser:
                    raise AdminSubuserException
                subusers = SubuserServices.get_all_subusers_for_one_user(user_id)
                if len(subusers) >= MAX_NUMBER_SUBUSERS:
                    raise MaxLimitSubusersException(message=f"You have reached Subusers Limit.", code=400)
                repository = SubuserRepository(db, Subuser)
                fields = {"user_id": user_id, "name": name}
                return repository.create(fields)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_subusers():
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                return repository.read_all()
        except Exception as e:
            raise e

    @staticmethod
    def get_subuser_by_id(subuser_id: str):
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                return repository.read_by_id(subuser_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_subusers_for_one_user(user_id):
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subusers = repository.read_subusers_by_user_id(user_id)
                return subusers
        except Exception as e:
            raise e

    @staticmethod
    def update_subusers_name(subuser_id: str, name: str):
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subuser = repository.read_by_id(subuser_id)
                updates = {"name": name}
                obj = repository.update(subuser, updates)
                return obj
        except Exception as e:
            raise e

    @staticmethod
    def delete_subuser(user_id: str, subuser_name: str):
        try:
            with SessionLocal() as db:
                repository = SubuserRepository(db, Subuser)
                subuser = repository.read_subusers_by_name(subuser_name)
                if not subuser or subuser.user_id != user_id:
                    raise UnknownProfileException
                response = repository.delete(subuser.id)
                return response
        except Exception as e:
            raise e
        