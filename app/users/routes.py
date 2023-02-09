import hashlib

from fastapi import APIRouter, status, Depends
from starlette.requests import Request
from starlette.responses import Response

from app.users.controller import UserController, SubuserController, AdminController, UserWatchMovieController
from app.users.controller.user_auth_controller import JWTBearer
from app.users.schemas import *
from app.users.schemas.user_watch_movie_schema import UserWatchMovieSchema

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("/register",
                  response_model=UserSchema,
                  summary="User Registration",
                  description="Register new User",
                  status_code=status.HTTP_201_CREATED)
def register_user(user: UserSchemaIn):
    user.password = hashlib.sha256(user.password.encode()).hexdigest()
    return UserController.create_user(**user.dict())


@user_router.post("/login",
                  summary="Login",
                  description="Login User using email and password.")
def login_user(email: str, password: str, response: Response):
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    token, user_id = UserController.login_user(email, password_hashed)
    response.set_cookie(key="user_id", value=user_id)
    return token


@user_router.get("/get-all-users",
                 response_model=list[UserSchema],
                 description="Read all Users from Database. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_users():
    return UserController.get_all_users()


@user_router.get("/get-user-by-id",
                 response_model=UserSchema,
                 description="Read specific User by ID. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_user_by_id(user_id: str):
    return UserController.get_user_by_id(user_id)


@user_router.get("/search-user-by-email",
                 response_model=list[UserSchema],
                 description="Search Users by email. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def search_users_by_email(email: str):
    return UserController.search_users_by_email(email)


@user_router.get("/get-user-with-subusers",
                 response_model=UserWithSubusersSchema,
                 description="Read User`s Subusers. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_user_with_subusers(user_id: str):
    return UserController.get_user_with_all_subusers(user_id)


@user_router.get("/get-my-subusers",
                 response_model=UserWithSubusersSchema,
                 description="Read my Subusers. User's route.",
                 dependencies=[Depends(JWTBearer(["regular_user"]))])
def get_my_subusers(request: Request):
    user_id = request.cookies.get("user_id")
    return UserController.get_user_with_all_subusers(user_id)


@user_router.put("/update-user",
                 response_model=UserSchema,
                 description="Update my username. User's route.",
                 dependencies=[Depends(JWTBearer(["regular_user"]))])
def update_my_name(request: Request, username: str):
    user_id = request.cookies.get("user_id")
    return UserController.update_username(user_id, username)


@user_router.delete("/delete-user",
                    description="Delete specific User by ID. Admin Route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_user(user_id: str):
    return UserController.delete_user(user_id)


subuser_router = APIRouter(prefix="/api/subusers", tags=["Subusers"])


@subuser_router.post("/add-new-subuser",
                     response_model=SubuserSchema,
                     summary="Subuser Registration",
                     description="Register new Subuser",
                     dependencies=[Depends(JWTBearer(["regular_user"]))])
def register_subuser(user_id: str, name: str):
    return SubuserController.create_subuser(user_id, name)


@subuser_router.get("/get-all-subuser",
                    response_model=list[SubuserSchema],
                    description="Read all Subusers from Database. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_subusers():
    return SubuserController.get_all_subusers()


@subuser_router.get("/get-subuser-by-id",
                    response_model=SubuserSchema,
                    description="Read specific Subuser by ID. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_subuser_by_id(subuser_id: str):
    return SubuserController.get_subuser_by_id(subuser_id)


@subuser_router.put("/update-subuser-name",
                    response_model=SubuserSchema,
                    description="Update Subuser`s name",
                    dependencies=[Depends(JWTBearer(["regular_user"]))])
def update_subusers_name(subuser_id: str, name: str):
    return SubuserController.update_subusers_name(subuser_id, name)


@subuser_router.delete("/delete-subuser",
                       description="Delete specific Subuser by ID.",
                       dependencies=[Depends(JWTBearer(["regular_user"]))])
def delete_subuser(subuser_id: str):
    return SubuserController.delete_subuser(subuser_id)


admin_router = APIRouter(prefix="/api/admins", tags=["Admins"])


@admin_router.post("/create-admin",
                   response_model=AdminSchema,
                   description="Register new Admin. Admin route",
                   dependencies=[Depends(JWTBearer(["super_user"]))])
def create_new_admin(admin: AdminSchemaIn):
    return AdminController.create_new_admin(admin.dict())


@admin_router.get("/read-all-admins",
                  response_model=list[AdminSchema],
                  description="Read all Admins. Admin route",
                  dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_admins():
    return AdminController.get_all_admins()


@admin_router.delete("/delete-admin",
                     response_model=UserSchema,
                     description="Delete specific Admin by ID. Admin route",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def remove_admin_credentials(admin_id: str):
    return AdminController.derogate_admin(admin_id)


watch_movie = APIRouter(prefix="/api/watch_movie", tags=["Watch Movie"])


@watch_movie.post("/", response_model=UserWatchMovieSchema, description="Select movie to watch")
def user_watch_movie(request: Request, title: str):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_watch_movie(user_id, title)


@watch_movie.put("/", response_model=UserWatchMovieSchema, description="Rate Movie")
def user_rate_movie(request: Request, title: str, rating: int):
    user_id = request.cookies.get("user_id")
    return UserWatchMovieController.user_rate_movie(user_id, title, rating)
