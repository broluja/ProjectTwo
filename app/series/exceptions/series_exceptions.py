"""Custom exceptions for Series logic"""
from app.base import AppException


class UnknownSeriesException(AppException):
    """Exception raised when user asks for episodes of unknown series."""
    message = "Series with that title does not exist."
    code = 404


class UnknownSeriesTitleException(AppException):
    """Exception raised when user's search returns an empty list."""
    message = "No Series with Title that matches your query."
    code = 404


class NoSeriesFromYearException(AppException):
    """Exception raised when User asks for Series from a specific
    year that does not have any Series in our Database."""
    message = "No Series from specific Year"
    code = 404


class NoLatestReleasesException(AppException):
    """Exception raised when user search for latest releases but in our Database there is no."""
    message = "No latest releases."
    code = 200


class UnknownEpisodeException(AppException):
    """Exception raised when user asks for episodes of unknown series."""
    message = "Episode with that title does not exist."
    code = 404


class NoPublishedEpisodesException(AppException):
    """Exception is raised when there is no episodes yet for specific Series."""
    message = "Episodes will be presented in coming future."
    code = 200
