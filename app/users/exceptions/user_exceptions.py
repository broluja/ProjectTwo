"""Custom exceptions for User logic"""
from app.base import AppException


class UserEmailAlreadyRegisteredException(AppException):
    """Exception raised when user try to register with email that is already in Database."""
    message = "User with this email is already registered."
    code = 400


class UserEmailDoesNotExistsException(AppException):
    """Exception raised when user searched by unknown Email."""
    message = "User with this email does not exist."
    code = 404


class InvalidPasswordForm(AppException):
    """Exception is raised when user's password form is not valid."""
    message = "Password must be at least 8 characters long with at least one number."
    code = 400


class InvalidVerificationCode(AppException):
    """Exception raised when user try to verify account with wrong verification code."""
    message = "Verification code unrecognized."
    code = 400


class UnverifiedAccountException(AppException):
    """Exception raised when user tries to log in before account verification."""
    message = "Please verify your account first. Check your email for verification code."
    code = 401


class InactiveUserException(AppException):
    """Exception raised when user with inactive status tries to log in."""
    message = "Your account is inactive. Please contact our support team."
    code = 401


class InvalidCredentialsException(AppException):
    """Exception raised on a wrong password during login action."""
    message = "Check your credentials."
    code = 401


class InvalidTokenException(AppException):
    """Exception raised on a wrong token authentication."""
    message = "Could not validate token."
    code = 403


class NonExistingUserIdException(AppException):
    """Exception raised when provided User's ID is non-existing."""
    code = 404


class UnknownProfileException(AppException):
    """Exception raised when provided username is non-existing."""
    code = 401
    message = "Unknown username."


class MaxLimitSubusersException(AppException):
    """Exception raised when User have reached Max number of subusers."""
    message = "You have reached Subusers Limit."
    code = 403


class AdminAlreadyCreatedException(AppException):
    """Exception is raised if you try to create admin when User is already Administrator."""
    code = 400


class AdminSubuserException(AppException):
    """Exception is raised when Admin tries to create Subuser. Not allowed for Admins."""
    message = "Admins are not allowed to create Subusers."
    code = 403


class AdminLoginException(AppException):
    """Exception is raised when user tries to log in as Admin."""
    message = "You are not an Admin."
    code = 403


class NonExistingAdminIdException(AppException):
    """Exception raised when provided Administrator's ID is non-existing."""
    message = "Unknown Admin ID."
    code = 404
