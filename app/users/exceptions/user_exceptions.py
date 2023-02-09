from app.base import AppException


class UserEmailAlreadyRegisteredException(AppException):
    """Exception raised when user try to register with email that is already in Database."""
    message = "User with this email is already registered."
    code = 400


class InvalidCredentialsException(AppException):
    """Exception raised on a wrong password during login action."""
    message = "Login failed. Check your credentials."
    code = 401


class InvalidTokenException(AppException):
    """Exception raised on a wrong token authentication."""
    message = "Could not validate token."
    code = 403


class NonExistingUserIdException(AppException):
    """Exception raised when provided User's ID is non-existing."""


class MaxLimitSubusersException(AppException):
    """Exception raised when User have reached Max number of subusers."""
    message = "You have reached Subusers Limit."


class AdminAlreadyCreatedException(AppException):
    """Exception is raised if you try to create admin when User is already Administrator."""
