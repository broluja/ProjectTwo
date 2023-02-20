from app.base import AppException


class NonExistingGenreException(AppException):
    """Exception raised when query for genre returns empty list"""
    code = 400


class GenreAlreadyExistsException(AppException):
    """Exception raised when tried creation of Genre that already exists."""
    code = 400
