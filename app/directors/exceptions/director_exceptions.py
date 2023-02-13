from app.base import AppException


class NonExistingDirectorException(AppException):
    """Exception raised when query for director returns empty list"""
    code = 400
