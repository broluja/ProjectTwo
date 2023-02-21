"""Custom exceptions for Movie logic"""
from app.base import AppException


class NonExistingMovieTitleException(AppException):
    """Exception raised when user try search for Movie Title non-existing in Database."""
    message = "Movie with this title does not exist."
    code = 400


class NoRatingsException(AppException):
    """Exception raised when movie has no ratings yet."""
    message = "Movie with this title does not have rating yet."
    code = 400
