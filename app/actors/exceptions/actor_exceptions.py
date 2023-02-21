"""Custom exceptions for Actor logic"""
from app.base import AppException


class ActorDataException(AppException):
    """Exception raised when Admin tries to create Actor without all data."""
    code = 400
