"""Actor controller module"""
from fastapi import HTTPException
from starlette.responses import Response

from app.actors.service import ActorServices
from app.base import AppException


class ActorController:
    """Controller for Actor routes"""
    @staticmethod
    def create_actor(first_name: str, last_name: str, date_of_birth: str, country: str):
        """
        Function creates a new actor in the database.
        It takes four parameters: first_name, last_name, date_of_birth and country.
        The function returns an actor object.

        Param first_name:str: Specify the first name of the actor
        Param last_name:str: Set the last name of the actor
        Param date_of_birth:str: Set the date of birth of the actor
        Param country:str: Specify the country of origin for an actor
        Return: The actor object that was created.
        """
        try:
            actor = ActorServices.create_new_actor(first_name, last_name, date_of_birth, country)
            return actor
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_all_actors(page: int):
        """
        Function returns all actors in the database.
        It takes one argument, page, which is an integer representing the page number of results to return.
        The function will return a list of actors, and a count of total number of actors.

        Param page:int: Specify the page number of the results to be returned
        Return: A list of actors.
        """
        try:
            actors = ActorServices.get_all_actors(page)
            if not actors:
                return Response(content="End of query.", status_code=200)
            return actors
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_actor_by_id(actor_id: str):
        """
        Function is used to retrieve a single actor by their ID.
        It takes in an actor_id as a string and returns the corresponding Actor object.
        If no such Actor exists, it raises an HTTPException with status code 404.

        Param actor_id:str: Get the actor with the given ID.
        Return: A dictionary with the actor's information.
        """
        try:
            actor = ActorServices.get_actor_by_id(actor_id)
            return actor
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_actor_by_last_name(actor: str):
        """
        Function is used to retrieve a list of actors with the same last name.
        It takes in an actor's last name as a parameter and returns all actors that have the same last name.

        Param actor:str: Pass the last name of an actor to the function
        Return: A list of actors with the same last name.
        """
        try:
            actors = ActorServices.get_actor_by_last_name(actor)
            if not actors:
                return Response(content=f"No actor with last name: {actor}", status_code=200)
            return actors
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_actor_by_first_name(actor: str):
        """
        Function is used to retrieve all actors with a given first name.
        It takes in the actor parameter as an input and returns a list of actors that match the given first name.

        Param actor:str: Pass the first name of the actor that is being searched for
        Return: A list of actors with the first name 'james'
        """
        try:
            actors = ActorServices.get_actor_by_first_name(actor)
            if not actors:
                return Response(content=f"No actor with first name: {actor}", status_code=200)
            return actors
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def get_actor_movies(last_name: str):
        """
        Function returns a list of movies that the actor has been in.
        The function takes one parameter, last_name, which is the last name of an actor.
        If no such actor exists, it returns a message saying so.

        Param last_name:str: Specify the last name of the actor whose movies are to be retrieved
        Return: A list of movie titles for the actor with the given last name.
        """
        try:
            actor = ActorServices.get_actor_movies(last_name)
            if not actor:
                return Response(content=f"No actor with last name: {last_name}", status_code=200)
            return [movie.title for movie in actor.movies]
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def update_actor(actor_id: str, attributes: dict):
        """
        Function updates an actor's information.

        Param actor_id:str: Identify the actor to be updated
        Param attributes:dict: Update the actor with the new attributes
        Return: The updated actor.
        """
        try:
            actor = ActorServices.update_actor(actor_id, attributes)
            return actor
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @staticmethod
    def delete_actor(actor_id: str):
        """
        Function deletes an actor from the database.
        It takes in a string representing the ID of the actor to be deleted, and returns a response with either
        'Actor deleted' or 'Actor not found' as its content.

        Param actor_id:str: Identify the actor that is to be deleted.
        Return: A response object with a message and status code.
        """
        try:
            ActorServices.delete_actor(actor_id)
            return Response(content=f"Actor with ID: {actor_id} deleted.", status_code=200)
        except AppException as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
