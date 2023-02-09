from app.base import AppException


class NonExistingMovieTitleException(AppException):
    """Exception raised when user try search for Movie Title non-existing in Database."""
    message = "Movie with this title does not exist."
    code = 400
