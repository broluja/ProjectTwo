from app.base import AppException


class UnknownSeriesException(AppException):
    """Exception raised when user asks for episodes of unknown series."""
    message = "Series with that title does not exist."
    code = 400
