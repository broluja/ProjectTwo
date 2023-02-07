from app.db import SessionLocal
from app.users.exceptions import NonExistingUserIdException, AdminAlreadyCreatedException
from app.users.repositories import AdminRepository
from app.users.models import Admin
from app.users.service import UserServices


class AdminServices:

    @staticmethod
    def create_new_admin(admin: dict):
        try:
            with SessionLocal() as db:
                user = UserServices.get_user_by_id(admin.get("user_id"))
                if not user:
                    raise NonExistingUserIdException(message=f"Non existing User ID: {admin.get('user_id')}", code=400)
                elif user.is_superuser:
                    raise AdminAlreadyCreatedException(message=f"User {user.username} is already Admin.", code=400)
                repository = AdminRepository(db, Admin)
                obj = repository.create(admin)
                UserServices.update_admin_status(admin.get("user_id"))
                return obj
        except Exception as e:
            raise e

    @staticmethod
    def derogate_admin(admin_id: str):
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                admin = admin_repository.read_by_id(admin_id)
                obj = UserServices.update_admin_status(admin.user_id, superuser=False)
                admin_repository.delete(admin_id)
                return obj
        except Exception as e:
            raise e

    @staticmethod
    def get_all_admins():
        try:
            with SessionLocal() as db:
                admin_repository = AdminRepository(db, Admin)
                return admin_repository.read_all()
        except Exception as e:
            raise e
