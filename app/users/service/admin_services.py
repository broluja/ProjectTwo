from app.db import SessionLocal
from app.users.repositories import AdminRepository
from app.users.models import Admin, User
from app.users.service import UserServices


class AdminServices:

    @staticmethod
    def create_new_admin(admin: dict):
        try:
            with SessionLocal() as db:
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
                return obj
        except Exception as e:
            raise e
