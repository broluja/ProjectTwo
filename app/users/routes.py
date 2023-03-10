"""User routes module"""
import hashlib

from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, status, Depends, HTTPException, Body, Query, BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.users.controller import UserController, SubuserController, AdminController
from app.users.controller.user_auth_controller import JWTBearer

from app.users.schemas import *

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("/register",
                  summary="User Registration",
                  status_code=status.HTTP_201_CREATED
                  )
def register_user(user: UserSchemaIn, worker: BackgroundTasks):
    """
    Function creates a new user in the database.
    It takes as input a UserSchemaIn object, which is validated and converted to an equivalent UserSchemaOut object.
    The password is hashed using SHA256 before being stored in the database.

    Param user:UserSchemaIn: Tell the function that it will be receiving a user object.
    Return: A dictionary with the user's ID and token.
    """
    try:
        valid = validate_email(user.email)
        valid_email = valid.email
    except EmailNotValidError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UserController.create_user(worker, valid_email, user.password, user.username)


@user_router.patch("/user-verification",
                   summary="User Verification",
                   status_code=status.HTTP_200_OK
                   )
def verify_user(verification_code: int = Body(embed=True)):
    """
    Function verifies a user's account by verifying the verification code sent to their email.
    The function returns a response with the content 'Account verified. You can log in now' and status code 200 if
    the verification is successful, or it returns an error message and status code 400 if not.

    Param verification_code:int: Verify the user's account.
    Return: A response object.
    """
    UserController.verify_user(verification_code)
    return JSONResponse(content="Account verified. You can log in now", status_code=200)


@user_router.post("/user-login",
                  summary="User Login",
                  )
def login_user(login: UserLoginSchema, response: JSONResponse):
    """
    Function takes in a username, email, password and response object.
    It hashes the password using sha256 and then uses the UserController to login user.
    The function returns a token for the user.

    Param username:str: Check if the username is already taken.
    Param email:str: Check if the user exists in the database.
    Param password:str: Store the hashed password.
    Param response:Response: Set the cookie for the user.
    Return: The token and user_id of the logged-in user.
    """
    password_hashed = hashlib.sha256(login.password.encode()).hexdigest()
    token, user_id = UserController.login_user(login.email, password_hashed, login.username)
    response.set_cookie(key="user_id", value=user_id)
    response.set_cookie(key="user_email", value=login.email)
    return token


@user_router.post("/user-forget-password",
                  summary="Ask for password change.",
                  )
def forget_password(email: str = Body(embed=True)):
    """
    Function is used to send a new ver.code to the user's email.
    It takes an email as input and sends information on user's email.

    Param email:str: Specify the email address of the user whose password is to be changed.
    Return: A response object.
    """
    UserController.change_password(email)
    response = JSONResponse(content="Request granted. Instructions are sent to your email.", status_code=200)
    response.set_cookie(key="code", value="active", max_age=600)
    return response


@user_router.post("/user-reset-password",
                  summary="Reset user's password. User route.",
                  dependencies=[Depends(JWTBearer(["super_user", "regular_user"]))]
                  )
def reset_password(request: Request, email: str = Body(embed=True)):
    """
    Function is used to reset the password of a user.
    It takes in an email as a parameter and sends an email with instructions on how to reset their password.

    Param email:str: Specify the email address of the user that is requesting a password reset.
    Return: The response object.
    """
    user_email = request.cookies.get("user_email")
    if user_email != email:
        raise HTTPException(detail="Unrecognized email.", status_code=400)
    UserController.change_password(email)
    response = JSONResponse(content="Request granted. Instructions are sent to your email.", status_code=200)
    response.set_cookie(key="code", value="active", max_age=600)
    return response


@user_router.patch("/reset-password-complete",
                   summary="Save new password. User route.",
                   status_code=status.HTTP_201_CREATED
                   )
def reset_password_complete(request: Request, reset: ChangePasswordSchema):
    """
    The reset_password_complete function is used to reset the password of a user.
    It takes as input the code generated by send_reset_password, and two strings:
    the old password and the new one. It checks if both passwords match, hashes them using SHA256,
    and then calls UserController's reset password method to change it.

    Param request:Request: Get the user's cookie.
    Param code:int: Identify the user.
    Param password:str: Set the new password for the user.
    Param new password:str: Set the new password for the user.
    Return: A response with a message that the reset password finished successfully.
    """
    if request.cookies.get("code") != "active":
        raise HTTPException(status_code=403, detail="Verification code expired. Ask for another one.")
    if reset.new_password != reset.repeat_password:
        raise HTTPException(status_code=400, detail="Passwords must match. Try again")
    password_hashed = hashlib.sha256(reset.new_password.encode()).hexdigest()
    UserController.reset_password_complete(reset.code, password_hashed)
    response = JSONResponse(content="Reset password finished successfully. You can login now.", status_code=200)
    response.delete_cookie(key="code")
    return response


@user_router.post("/admin-login",
                  summary="Admin Login",
                  )
def login_admin(login: AdminLoginSchema, response: JSONResponse):
    """
    Function takes in an email and a password, hashes the password using SHA256,
    and then checks if the email and hashed password match. If they do it returns a token for that user
    and their user_id. It also sets a cookie on the response with their user_id.

    Param email:str: Store the email of the user that is trying to log in.
    Param password:str: Hash the password before it is sent to the database.
    Param response:Response: Set the cookie.
    Return: A token and a user_id.
    """
    password_hashed = hashlib.sha256(login.password.encode()).hexdigest()
    token, user_id = UserController.login_admin(login.email, password_hashed)
    response.set_cookie(key="user_id", value=user_id)
    return token


@user_router.get("/get-all-users",
                 response_model=list[UserSchemaOut],
                 summary="Get all users. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_all_users():
    """
    Function returns a list of all users in the database.

    Return: A list of all the users in the database.
    """
    return UserController.get_all_users()


@user_router.get("/get-all-active-users",
                 response_model=list[UserSchemaOut],
                 summary="Get all active users. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_all_active_users():
    """
    Function returns a list of all active users.

    Return: A list of all active users.
    """
    return UserController.get_all_active_users()


@user_router.get("/get-all-inactive-users",
                 response_model=list[UserSchemaOut],
                 summary="Get all inactive users. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_all_inactive_users():
    """
    The get_all_inactive_users function returns a list of all inactive users.

    Return: A list of all inactive users.
    """
    return UserController.get_all_active_users(active=False)


@user_router.get("/get-user-by-id",
                 response_model=UserSchemaOut,
                 summary="Get user by ID. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_user_by_id(user_id: str):
    """
    Function takes a user_id as an argument and returns the User object associated with that ID.

    Param user_id:str: Identify the user
    Return: A user object from the database.
    """
    return UserController.get_user_by_id(user_id)


@user_router.get("/search-users",
                 response_model=list[UserSchemaOut],
                 summary="Search for users by email. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def search_users(choice: str = Query("Username", enum=["Username", "Email"]), query: str = ""):
    """
    Function searches for users by email or username.
    It takes an email/username as a parameter and returns
    users that possible match provided email/username.

    Param query:str: Search for a user with the given email/username.
    Return: A list of users that match the email/username provided.
    """
    if choice == "Username":
        return UserController.search_users_by_username(query)
    elif choice == "Email":
        return UserController.search_users_by_email(query)


@user_router.get("/get-user-with-subusers",
                 response_model=UserWithSubusersSchema,
                 summary="Get user by ID with all his subusers. Admin route.",
                 dependencies=[Depends(JWTBearer(["super_user"]))]
                 )
def get_user_with_subusers(user_id: str):
    """
    Function returns a user object with all of its subusers.
    The function takes in the user_id as an argument and returns the corresponding User object.

    Param user_id:str: Specify the user that is being requested.
    Return: A user object with the subusers attribute set to a list of all the user's subusers.
    """
    return UserController.get_user_with_all_subusers(user_id)


@user_router.get("/get-my-subusers",
                 response_model=UserWithSubusersSchema,
                 summary="Get my Subusers. User route.",
                 dependencies=[Depends(JWTBearer(["regular_user"]))]
                 )
def get_my_subusers(request: Request):
    """
    Function returns a list of all the subusers associated with the user who is currently logged in.
    The function takes no arguments and returns a JSON object containing two keys: 'subusers' and 'user'.
    The value for the key 'subusers' is an array of objects, each representing one of the subusers
    associated with this user. Each object has three keys: ID, name and email. The value for the key 'user'
    is an object that represents this user's information; it also has three keys: ID, name and email.

    Param request:Request: Get the user_id from the cookie.
    Return: A list of all subusers for a given user.
    """
    user_id = request.cookies.get("user_id")
    return UserController.get_user_with_all_subusers(user_id)


@user_router.patch("/update-user-username",
                   response_model=UserSchemaOut,
                   summary="Update my username. User route.",
                   dependencies=[Depends(JWTBearer(["regular_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def update_my_name(request: Request, username: str = Body(embed=True)):
    """
    The update_my_name function updates the username of a user.

    Param request:Request: Get the user_id from the cookie.
    Param username:str: Store the new username that is entered by the user.
    Return: A user object.
    """
    user_id = request.cookies.get("user_id")
    return UserController.update_username(user_id, username)


@user_router.patch("/update-user-email",
                   response_model=UserSchemaOut,
                   summary="Change my email. User Route.",
                   dependencies=[Depends(JWTBearer(["regular_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def change_my_email(request: Request, email: str = Body(embed=True)):
    """
    Function allows a user to change their email.
    It takes in the request and the new email as parameters.
    It returns a response with the status code of 200 if successful, or 400 if not.

    Param request:Request: Get the user_id from the cookies.
    Param email:str: Change the email of a user.
    Return: None.
    """
    user_id = request.cookies.get("user_id")
    return UserController.change_email(user_id, email)


@user_router.patch("/deactivate-user",
                   response_model=UserSchema,
                   summary="Deactivate User. Admin route",
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def deactivate_user(user_id: str = Body(embed=True)):
    """
    Function takes a user_id as an argument and deactivates the corresponding user.
    It returns True if the operation was successful, False otherwise.

    Param user_id:str: Specify the user that is to be deactivated
    Return: The user-controller.
    """
    return UserController.deactivate_user(user_id)


@user_router.patch("/activate-user",
                   response_model=UserSchemaOut,
                   summary="Activate User. Admin route",
                   dependencies=[Depends(JWTBearer(["super_user"]))],
                   status_code=status.HTTP_201_CREATED
                   )
def activate_user(user_id: str = Body(embed=True)):
    """
    Function is used to activate a user.
    It takes in the user_id as an argument and returns the updated User object.

    Param user_id:str: Identify the user that is to be activated.
    Return: A dictionary with the user's information.
    """
    return UserController.deactivate_user(user_id, activity=True)


@user_router.delete("/delete-user",
                    summary="Delete User. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))]
                    )
def delete_user(user_id: str = Body(embed=True)):
    """
    Function deletes a user from the database.

    Param user_id:str: Specify the user_id of the user that is to be deleted
    Return: A boolean value.
    """
    return UserController.delete_user(user_id)


subuser_router = APIRouter(prefix="/api/subusers", tags=["Subusers"])


@subuser_router.post("/add-new-subuser",
                     response_model=SubuserSchema,
                     summary="Register new Subuser. User route",
                     dependencies=[Depends(JWTBearer(["regular_user"]))],
                     status_code=status.HTTP_201_CREATED
                     )
def register_subuser(request: Request, name: str = Body(embed=True)):
    """
    Function creates a new subuser with the given name.

    Param request:Request: Get the user_id from the cookie
    Param name:str: Set the name of the subuser
    Return: A dictionary with the sub-user's information.
    """
    user_id = request.cookies.get("user_id")
    return SubuserController.create_subuser(user_id, name)


@subuser_router.get("/get-all-subusers",
                    response_model=list[SubuserSchema],
                    summary="Get all Subusers. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))]
                    )
def get_all_subusers():
    """
    The get_all_subusers function returns a list of all subusers.

    Return: A list of all the subusers in a dictionary format.
    """
    return SubuserController.get_all_subusers()


@subuser_router.get("/get-subuser-by-id",
                    response_model=SubuserSchema,
                    summary="Get specific Subuser by ID. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))]
                    )
def get_subuser_by_id(subuser_id: str):
    """
    Function returns a subuser object given an ID.

    Param subuser_id:str: Specify the subuser that is to be retrieved.
    Return: A subuser object.
    """
    return SubuserController.get_subuser_by_id(subuser_id)


@subuser_router.patch("/update-subuser-name",
                      response_model=SubuserSchema,
                      summary="Update my username. Subuser route",
                      dependencies=[Depends(JWTBearer(["sub_user"]))],
                      status_code=status.HTTP_201_CREATED
                      )
def update_subusers_name(request: Request, name: str = Body(embed=True)):
    """
    The update_subusers_name function updates the name of a subuser.

    Param request:Request: Get the user_id from the cookies.
    Param name:str: Update the name of the subuser.
    Return: A response object.
    """
    subuser_id = request.cookies.get("user_id")
    return SubuserController.update_subusers_name(subuser_id, name)


@subuser_router.delete("/delete-subuser",
                       summary="Delete my Subuser. User route",
                       dependencies=[Depends(JWTBearer(["regular_user"]))]
                       )
def delete_subuser(request: Request, subuser_name: str = Body(embed=True)):
    """
    Function deletes a subuser from the database.

    Param request:Request: Get the user_id from the cookie
    Param subuser_name:str: Specify, which subuser to delete
    Return: A response object.
    """
    user_id = request.cookies.get("user_id")
    return SubuserController.delete_subuser(user_id, subuser_name)


admin_router = APIRouter(prefix="/api/admins", tags=["Admins"])


@admin_router.post("/create-admin",
                   response_model=AdminSchema,
                   summary="Create new Admin. Admin route",
                   status_code=status.HTTP_201_CREATED,
                   dependencies=[Depends(JWTBearer(["super_user"]))]
                   )
def create_new_admin(admin: AdminSchemaIn):
    """
    The create_new_admin function creates a new admin in the database.
    It takes an AdminSchemaIn object as its only parameter and returns an AdminSchemaOut object.

    Param admin:AdminSchemaIn: Validate the input data.
    Return: The admin object created.
    """
    return AdminController.create_new_admin(admin.dict())


@admin_router.get("/read-all-admins",
                  response_model=list[AdminSchema],
                  summary="Get all Admins. Admin route",
                  dependencies=[Depends(JWTBearer(["super_user"]))]
                  )
def get_all_admins():
    """
    Function returns a list of all the admins in the database.

    Return: A list of all the admins in the database.
    """
    return AdminController.get_all_admins()


@admin_router.get("/read-admins-by-country",
                  summary="Get all Admins by country. Admin Route",
                  dependencies=[Depends(JWTBearer(["super_user"]))],
                  response_model=list[AdminSchema]
                  )
def get_all_admins_by_country(country: str):
    """
    Function returns a list of all the admins in a given country.
    The function takes one parameter, which is the name of the country to search for.

    Param country:str: Filter the admins by country.
    Return: A list of all the admins in a country.
    """
    return AdminController.get_all_admins_by_country(country)


@admin_router.patch("/derogate-admin",
                    response_model=UserSchema,
                    summary="Deactivate Admin status. Admin route",
                    dependencies=[Depends(JWTBearer(["super_user"]))]
                    )
def remove_admin_credentials(admin_id: str = Body(embed=True)):
    """
    Function removes the admin credentials from the database.
    It takes one argument, an admin_id, which is a string that represents the
    unique identifier for an admin in our database.
    The function returns True if it was successful and False otherwise.

    Param admin_id:str: Specify the admin_id of the admin that is to be removed.
    Return: The admin_id of the admin that is being removed from the system.
    """
    return AdminController.derogate_admin(admin_id)
