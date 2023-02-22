"""Episode Controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.base import AppException
from app.series.service import EpisodeServices


class EpisodeController:
    """Controller for Episode routes"""
    @staticmethod
    def create_episode(name: str, series_id: str):
        """
        Function creates a new episode in the database.
        It takes two parameters: name and series_id. It returns an Episode object.

        Param name:str: Set the name of the episode.
        Param series_id:str: Specify the series to which the episode belongs.
        Return: A episode object.
        """
        try:
            episode = EpisodeServices.create_new_episode(name, series_id)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_episodes_by_series(series_title: str):
        """
        Function returns all episodes for a given series.
        The function takes one argument, the name of the series as a string.
        If no episodes are found for that series, it will return an empty list.

        Param series_title:str: Pass the series title to the function.
        Return: A list of all episodes for a given series title.
        """
        try:
            episodes = EpisodeServices.get_all_episodes_by_series(series_title)
            if not episodes:
                Response(content=f"No Episodes for Series: {series_title}.", status_code=200)
            return episodes
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_episode_by_id(episode_id: str):
        """
        The get_episode_by_id function is used to retrieve a single episode by its ID.
        It takes in an episode_id as a string and returns the corresponding Episode object.
        If no such episode exists, it raises an HTTPException with status code 404.

        Param episode_id:str: Identify the episode that is to be retrieved
        Return: A single episode by ID.
        """
        try:
            episode = EpisodeServices.get_episode_by_id(episode_id)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_best_rated_episode(best: bool = True):
        """
        Function returns the episode with the highest rating.
        If there are multiple episodes with the same rating, it will return all of them.


        Param best:bool=True: Get the best rated episodes or not.
        Return: A list of episodes that are the best rated episodes.
        """
        try:
            episodes = EpisodeServices.get_best_rated_episode(best=best)
            if not episodes:
                return Response(content="We have not generated episode popularity list yet.", status_code=200)
            return episodes
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_episode(episode_id: str, attributes: dict):
        """
        Function updates an episode with the given attributes.

        Param episode_id:str: Identify the episode to be updated
        Param attributes:dict: Update the episode
        Return: The updated episode.
        """
        try:
            episode = EpisodeServices.update_episode(episode_id, attributes)
            return episode
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_episode(episode_id: str):
        """
        Function deletes an episode from the database.
        It takes one parameter, which is the ID of the episode to be deleted.
        If successful, it returns a response with a message confirming that
        delete was successful and what ID was deleted.

        Param episode_id:str: Specify the episode that is to be deleted.
        Return: A response object.
        """
        try:
            EpisodeServices.delete_episode(episode_id)
            return Response(content=f"Episode with ID: {episode_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
