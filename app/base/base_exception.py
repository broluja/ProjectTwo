"""Base Exception Class which is inherited by all other custom exceptions."""


class AppException(Exception):
    """Base Exception Model"""
    message = "Something went wrong"
    code = 500

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", self.message)
        self.code = kwargs.get("code", self.code)
