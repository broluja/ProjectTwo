import hashlib

from fastapi import APIRouter, status, Depends
from app.users.controller import UserController, SubuserController, AdminController
from app.users.controller.user_auth_controller import JWTBearer
from app.users.schemas import *

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("/register",
                  response_model=UserSchema,
                  summary="User Registration",
                  description="Register new User",
                  status_code=status.HTTP_201_CREATED)
def register_user(user: UserSchemaIn):
    password_hashed = hashlib.sha256(user.password.encode()).hexdigest()
    return UserController.create_user(user.email, password_hashed, user.username)


@user_router.get("/login",
                 summary="Login",
                 description="Login User using email and password.")
def login_user(email: str, password: str):
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    return UserController.login_user(email, password_hashed)


@user_router.get("/get-all-users",
                 response_model=list[UserSchema, ],
                 description="Read all Users from Database. Admin route",
                 dependencies=[Depends(JWTBearer("super_user"))])
def get_all_users():
    return UserController.get_all_users()


@user_router.get("/get-user-by-id", response_model=UserSchema, description="Read specific User by ID. Admin route")
def get_user_by_id(user_id: str):
    return UserController.get_user_by_id(user_id)


@user_router.get("/get-user-with-subusers", response_model=UserWithSubusersSchema)
def get_user_with_subusers(user_id: str):
    return UserController.get_user_with_all_subusers(user_id)


@user_router.put("/update-user", response_model=UserSchema, description="Update User`s username")
def update_users_name(user_id: str, username: str):
    return UserController.update_username(user_id, username)


@user_router.delete("/delete-user", description="Delete specific User by ID. Admin Route")
def delete_user(user_id: str):
    return UserController.delete_user(user_id)


subuser_router = APIRouter(prefix="/api/subusers", tags=["Subusers"])


@subuser_router.post("/add-new-subuser",
                     response_model=SubuserSchema,
                     summary="Subuser Registration",
                     description="Register new Subuser")
def register_subuser(user_id: str, name: str):
    return SubuserController.create_subuser(user_id, name)


@subuser_router.get("/get-all-subuser",
                    response_model=list[SubuserSchema],
                    description="Read all Subusers from Database. Admin route")
def get_all_subusers():
    return SubuserController.get_all_subusers()


@subuser_router.get("/get-subuser-by-id",
                    response_model=SubuserSchema,
                    description="Read specific Subuser by ID. Admin route")
def get_subuser_by_id(subuser_id: str):
    return SubuserController.get_subuser_by_id(subuser_id)


@subuser_router.put("/update-subuser-name", response_model=SubuserSchema, description="Update Subuser`s name")
def update_subusers_name(subuser_id: str, name: str):
    return SubuserController.update_subusers_name(subuser_id, name)


@subuser_router.delete("/delete-subuser", description="Delete specific Subuser by ID.")
def delete_subuser(subuser_id: str):
    return SubuserController.delete_subuser(subuser_id)


admin_router = APIRouter(prefix="/api/admins", tags=["Admins"])


@admin_router.post("/create-admin", response_model=AdminSchema, description="Register new Admin. Admin route")
def create_new_admin(admin: AdminSchemaIn):
    return AdminController.create_new_admin(vars(admin))


@admin_router.get("/read-all-admins", response_model=list[AdminSchema], description="Read all Admins. Admin route")
def get_all_admins():
    return AdminController.get_all_admins()


@admin_router.delete("/delete-admin", response_model=UserSchema, description="Delete specific Admin by ID. Admin route")
def remove_admin_credentials(admin_id: str):
    return AdminController.derogate_admin(admin_id)
