"""Base Exception Class which is inherited by all other custom exceptions."""


class AppException(Exception):
    """Base Exception Model"""
    message = "Something went wrong"
    code = 500
    headers = None

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", self.message)
        self.code = kwargs.get("code", self.code)
        if self.code == 401:
            self.headers = {"WWW-Authenticate": "bearer"}
