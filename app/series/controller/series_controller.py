"""Series Controller module"""
from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.base import AppException
from app.directors.service import DirectorServices
from app.genres.service import GenreServices
from app.series.service import SeriesServices


class SeriesController:
    """Controller for Series routes"""
    @staticmethod
    def create_series(title: str, year_published: str, director_id: str, genre_id: str):
        """
        Function creates a new series object and returns it.
        It takes in the title, year_published, director_id, and genre_id as parameters.
        It then uses these parameters to create a new Series object with the given information.
        The function then returns this newly created Series object.

        Param title:str: Specify the title of the series
        Param year published:str: Set the year published attribute of the series object
        Param director_id:str: Get the director object from the database
        Param genre_id:str: Get the genre object from the database
        Return: A series object.
        """
        try:
            director = DirectorServices.get_director_by_id(director_id)
            genre = GenreServices.get_genre_by_id(genre_id)
            series = SeriesServices.create_new_series(title, year_published, director_id, genre_id)
            series.director = director
            series.genre = genre
            return series
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def read_all_series(page):
        """
        Function returns all series in the database.
        The function takes one argument, page, which is an integer that indicates what page of results to return.
        If no value is provided for this parameter, the default value of 1 will be used.

        Param page: Specify the page of series to be returned
        Return: A list of all the series in the database.
        """
        try:
            series = SeriesServices.read_all_series(page)
            return series if series else JSONResponse(content="End of query.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_data(title: str):
        """
        The get_series_data function takes a series title as an argument and returns the data for that series.
        If no such series exists, it returns a response with status code 200, and the message
        'No Series with name: {title}'
        If any other error occurs, it raises an HTTPException with status code 500 and the message
        'Internal Server Error'.

        Param title:str: Specify the title of the series.
        Return: A series object.
        """
        try:
            series = SeriesServices.get_series_by_name(title, search=False)
            if not series:
                return JSONResponse(content=f"No Series with name: {title}.", status_code=200)
            director = DirectorServices.get_director_by_id(series.director_id)
            genre = GenreServices.get_genre_by_id(series.genre_id)
            series.director = director
            series.genre = genre
            return series
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_director_name(director: str):
        """
        Function is used to retrieve all series from a given director.
        It takes in the name of the director as an argument and returns a list of Series objects.

        Param director:str: Filter the series by director name.
        Return: A list of series that match the director name.
        """
        try:
            series = SeriesServices.get_series_by_director_name(director)
            return series if series else JSONResponse(content=f"No Series from Director: {director}.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_id(series_id: str):
        """
        Function is used to retrieve a series by its ID.
        It takes in the series_id as an argument and returns the corresponding series object.

        Param series_id:str: Get the series with that ID.
        Return: A series object.
        """
        try:
            return SeriesServices.get_series_by_id(series_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_my_series(user_id: str):
        """
        Function returns a list of all the series that the user has watched.
        It takes in a string parameter, which is the user_id and it returns a list of dictionaries,
        which contain information about each series.

        Param user_id:str: Identify the user
        Return: A list of series that the user has watched.
        """
        try:
            series = SeriesServices.get_my_series(user_id)
            return series if series else JSONResponse(content="You have not watched any series yet.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_episode_id(episode_id: str):
        """
        Function is used to retrieve a series by its episode ID.
        It takes in an episode_id as a string and returns the corresponding series object.

        Param episode_id:str: Get the series by its episode ID.
        Return: The series that the episode belongs to.
        """
        try:
            return SeriesServices.get_series_by_episode_id(episode_id)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_name(series: str):
        """
        Function takes a series name as an argument and returns the Series object associated with that name.
        If no such series exists, it returns a 404 error.

        Param series:str: Get the series by name.
        Return: A series object with the given name.
        """
        try:
            series = SeriesServices.get_series_by_name(series)
            return series if series else JSONResponse(content=f"No Series with name: {series}.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_year(year: int):
        """
        Function returns a list of series that were created in the given year.
        If no series are found, it returns an empty list.

        Param year:int: Filter the series by a year.
        Return: A list of series from a given year.
        """
        try:
            series = SeriesServices.get_series_by_year(year)
            return series if series else JSONResponse(content=f"No Series from year: {year}.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_series_by_genre(genre: str):
        """
        Function takes a genre as an argument and returns all series with that genre.
        If no series are found, it returns a message saying so.

        Param genre:str: Filter the series by a genre.
        Return: A list of series that match the genre.
        """
        try:
            series = SeriesServices.get_series_by_genre(genre)
            return series if series else JSONResponse(content=f"No Series with genre: {genre}.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_latest_features(date_limit: str):
        """
        Function returns a list of the latest series added to the database.
        The date limit parameter is used to filter out any series that were added before this date.
        If no series are found, an empty list is returned.

        Param date limit:str: Limit the number of series returned
        Return: A list of the latest features.
        """
        try:
            series = SeriesServices.get_latest_features(date_limit)
            return series if series else JSONResponse(content="No series in latest list.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def show_series_never_downloaded():
        """
        Function returns a list of all series that have never been downloaded.
        The function takes no arguments and returns a list of dictionaries,
        each dictionary representing one series.

        Return: A list of series that have never been downloaded.
        """
        try:
            series = SeriesServices.show_series_never_downloaded()
            return series if series else JSONResponse(
                content="There are no series that never have been downloaded.",
                status_code=200
            )
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_series_data(series_id: str, attributes: dict):
        """
        Function updates the series data for a given series ID.
        The function takes in two parameters, the first parameter is a string representing
        the unique identifier of an existing Series record, and the second parameter is a
        dictionary containing key-value pairs of attributes to be updated.
        The function returns an instance of Series class with all its attributes.

        Param series_id:str: Specify the series_id of the series that is to be updated.
        Param attributes:dict: Update the series data.
        Return: A series object.
        """
        try:
            return SeriesServices.update_series_data(series_id, attributes)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_series(series_id: str):
        """
        Function deletes a series from the database.
        It takes in a series_id as an argument and returns the deleted Series object.

        Param series_id:str: Specify the series to be deleted.
        Return: A response object.
        """
        try:
            SeriesServices.delete_series(series_id)
            return JSONResponse(content=f"Series with ID: {series_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
