from app.base import AppException


class UserEmailAlreadyRegisteredException(AppException):
    """Exception raised when user try to register with email that is already in Database."""


class NonExistingUserIdException(AppException):
    """Exception raised when provided User's ID is non-existing."""


class MaxLimitSubusersException(AppException):
    """Exception raised when User have reached Max number of subusers."""
