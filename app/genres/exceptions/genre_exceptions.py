from app.base import AppException


class NonExistingGenreException(AppException):
    """Exception raised when query for genre returns empty list"""
    code = 400
