"""Custom exceptions for Series logic"""
from app.base import AppException


class UnknownSeriesException(AppException):
    """Exception raised when user asks for episodes of unknown series."""
    message = "Series with that title does not exist."
    code = 404


class UnknownEpisodeException(AppException):
    """Exception raised when user asks for episodes of unknown series."""
    message = "Episode with that title does not exist."
    code = 404
