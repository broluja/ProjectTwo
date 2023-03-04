"""Custom exceptions for Movie logic"""
from app.base import AppException


class NonExistingMovieTitleException(AppException):
    """Exception raised when user try search for Movie Title non-existing in Database."""
    message = "Movie with this title does not exist."
    code = 404


class NoRatingsException(AppException):
    """Exception raised when movie has no ratings yet."""
    message = "Movie with this title does not have rating yet."
    code = 200


class NoMovieFromYearException(AppException):
    """Exception raised when user search for Movie from a specific year
     for which there is no data in our Database."""
    message = "There is no movies from this year in our Database."
    code = 200


class NoLatestReleasesException(AppException):
    """Exception raised when user search for latest releases but in our Database there is no."""
    message = "No latest releases."
    code = 200


class NoMoviesFromDirectorException(AppException):
    """Exception raised when user search for Movie from a specific director
     for whom there is still no data in our Database."""
    message = "There is no movies from this director in our Database yet."
    code = 200
