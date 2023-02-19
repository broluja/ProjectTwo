import hashlib

from fastapi import APIRouter, status, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.users.controller import UserController, SubuserController, AdminController
from app.users.controller.user_auth_controller import JWTBearer
from app.users.schemas import *

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("/register",
                  summary="User Registration",
                  description="Register new User",
                  status_code=status.HTTP_201_CREATED)
def register_user(user: UserSchemaIn):
    user.password = hashlib.sha256(user.password.encode()).hexdigest()
    return UserController.create_user(**user.dict())


@user_router.post("/user-verification",
                  summary="User Verification",
                  description="Verify User",
                  status_code=status.HTTP_200_OK)
def verify_user(verification_code: int):
    UserController.verify_user(verification_code)
    return Response(content="Account verified. You can log in now", status_code=200)


@user_router.post("/user-login",
                  summary="User Login",
                  description="Login User using email, password and username.")
def login_user(username: str, email: str, password: str, response: Response):
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    token, user_id = UserController.login_user(email, password_hashed, username)
    response.set_cookie(key="user_id", value=user_id)
    return token


@user_router.post("/user-forget-password",
                  summary="Ask for password change.",
                  description="Demand reset of password.")
def forget_password(email: str):
    UserController.change_password(email)
    response = Response(content="Request granted. Instructions are sent to your email.", status_code=200)
    response.set_cookie(key="code", value="active", max_age=600)
    return response


@user_router.post("/user-reset-password",
                  summary="Reset user's password. User route.",
                  description="Demand reset of password.",
                  dependencies=[Depends(JWTBearer(["super_user", "regular_user"]))])
def reset_password(email: str):
    UserController.change_password(email)
    response = Response(content="Request granted. Instructions are sent to your email.", status_code=200)
    response.set_cookie(key="code", value="active", max_age=600)
    return response


@user_router.post("/reset-password-complete",
                  summary="Save new password. User route.",
                  description="Set new password.")
def reset_password_complete(request: Request, code: int, password: str, new_password: str):
    if request.cookies.get("code") != "active":
        raise HTTPException(status_code=400, detail="Verification code expired. Ask for another one.")
    if password != new_password:
        raise HTTPException(status_code=400, detail="Passwords must match. Try again")
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    UserController.reset_password_complete(code, password_hashed)
    return Response(content="Reset password finished successfully. You can login now.", status_code=200)


@user_router.post("/admin-login",
                  summary="Admin Login",
                  description="Login Admin using email and password.")
def login_admin(email: str, password: str, response: Response):
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    token, user_id = UserController.login_admin(email, password_hashed)
    response.set_cookie(key="user_id", value=user_id)
    return token


@user_router.get("/get-all-users",
                 response_model=list[UserSchema],
                 summary="Get all users. Admin route.",
                 description="Read all Users from Database. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_users():
    return UserController.get_all_users()


@user_router.get("/get-all-active-users",
                 response_model=list[UserSchema],
                 summary="Get all active users. Admin route.",
                 description="Read all active Users from Database. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_active_users():
    return UserController.get_all_active_users()


@user_router.get("/get-all-inactive-users",
                 response_model=list[UserSchema],
                 summary="Get all inactive users. Admin route.",
                 description="Read all inactive Users from Database. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_inactive_users():
    return UserController.get_all_active_users(active=False)


@user_router.get("/get-user-by-id",
                 response_model=UserSchema,
                 summary="Get user by ID. Admin route.",
                 description="Read specific User by ID. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_user_by_id(user_id: str):
    return UserController.get_user_by_id(user_id)


@user_router.get("/search-user-by-email",
                 response_model=list[UserSchema],
                 summary="Search for users by email. Admin route.",
                 description="Search Users by email. Admin route",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def search_users_by_email(email: str):
    return UserController.search_users_by_email(email)


@user_router.get("/get-user-with-subusers",
                 response_model=UserWithSubusersSchema,
                 summary="Get user by ID with all his subusers. Admin route.",
                 description="Read User`s Subusers. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def get_user_with_subusers(user_id: str):
    return UserController.get_user_with_all_subusers(user_id)


@user_router.get("/get-my-subusers",
                 response_model=UserWithSubusersSchema,
                 summary="Get my Subusers. User route.",
                 description="Read my Subusers. User's route.",
                 dependencies=[Depends(JWTBearer(["regular_user"]))])
def get_my_subusers(request: Request):
    user_id = request.cookies.get("user_id")
    return UserController.get_user_with_all_subusers(user_id)


@user_router.put("/update-user",
                 response_model=UserSchema,
                 summary="Update my username. User route.",
                 description="Update my username. User's route.",
                 dependencies=[Depends(JWTBearer(["regular_user"]))])
def update_my_name(request: Request, username: str):
    user_id = request.cookies.get("user_id")
    return UserController.update_username(user_id, username)


@user_router.put("/deactivate-user",
                 response_model=UserSchema,
                 summary="Deactivate User. Admin route",
                 description="Deactivate specific User.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def deactivate_user(user_id: str):
    return UserController.deactivate_user(user_id)


@user_router.put("/activate-user",
                 response_model=UserSchema,
                 summary="Activate User. Admin route",
                 description="Activate specific User.",
                 dependencies=[Depends(JWTBearer(["super_user"]))])
def deactivate_user(user_id: str):
    return UserController.deactivate_user(user_id, activity=True)


@user_router.delete("/delete-user",
                    summary="Delete User. Admin route",
                    description="Delete specific User by ID. Admin Route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def delete_user(user_id: str):
    return UserController.delete_user(user_id)


subuser_router = APIRouter(prefix="/api/subusers", tags=["Subusers"])


@subuser_router.post("/add-new-subuser",
                     response_model=SubuserSchema,
                     summary="Register new Subuser. User route",
                     description="Register new Subuser",
                     dependencies=[Depends(JWTBearer(["regular_user"]))],
                     status_code=status.HTTP_201_CREATED)
def register_subuser(request: Request, name: str):
    user_id = request.cookies.get("user_id")
    return SubuserController.create_subuser(user_id, name)


@subuser_router.get("/get-all-subusers",
                    response_model=list[SubuserSchema],
                    summary="Get all Subusers. Admin route",
                    description="Read all Subusers from Database. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_subusers():
    return SubuserController.get_all_subusers()


@subuser_router.get("/get-subuser-by-id",
                    response_model=SubuserSchema,
                    summary="Get specific Subuser by ID. Admin route",
                    description="Read specific Subuser by ID. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))])
def get_subuser_by_id(subuser_id: str):
    return SubuserController.get_subuser_by_id(subuser_id)


@subuser_router.put("/update-subuser-name",
                    response_model=SubuserSchema,
                    summary="Update my username. Subuser route",
                    description="Update Subuser`s name",
                    dependencies=[Depends(JWTBearer(["sub_user"]))])
def update_subusers_name(request: Request, name: str):
    subuser_id = request.cookies.get("user_id")
    return SubuserController.update_subusers_name(subuser_id, name)


@subuser_router.delete("/delete-subuser",
                       summary="Delete my Subuser. User route",
                       description="Delete specific Subuser by subuser name.",
                       dependencies=[Depends(JWTBearer(["regular_user"]))])
def delete_subuser(request: Request, subuser_name: str):
    user_id = request.cookies.get("user_id")
    return SubuserController.delete_subuser(user_id, subuser_name)


admin_router = APIRouter(prefix="/api/admins", tags=["Admins"])


@admin_router.post("/create-admin",
                   response_model=AdminSchema,
                   summary="Create new Admin. Admin route",
                   description="Register new Admin. Admin route",
                   status_code=status.HTTP_201_CREATED)
def create_new_admin(admin: AdminSchemaIn):
    return AdminController.create_new_admin(admin.dict())


@admin_router.get("/read-all-admins",
                  response_model=list[AdminSchema],
                  summary="Get all Admins. Admin route",
                  description="Read all Admins. Admin route",
                  dependencies=[Depends(JWTBearer(["super_user"]))])
def get_all_admins():
    return AdminController.get_all_admins()


@admin_router.get("/read-admins-by-country",
                  summary="Get all Admins by country. Admin Route",
                  description="Get all Admins from specific country.",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  response_model=list[AdminSchema])
def get_all_admins_by_country(country: str):
    return AdminController.get_all_admins_by_country(country)


@admin_router.delete("/delete-admin",
                     response_model=UserSchema,
                     summary="Deactivate Admin status. Admin route",
                     description="Delete specific Admin by ID. Admin route",
                     dependencies=[Depends(JWTBearer(["super_user"]))])
def remove_admin_credentials(admin_id: str):
    return AdminController.derogate_admin(admin_id)
