"""Base Repository class with CRUD operations, which is inherited by every other repository Model."""
from typing import Union, Type, TypeVar, Generic
from fastapi.encoders import jsonable_encoder

from app.base.base_exception import AppException
from app.db import SessionLocal

Model = TypeVar("Model")


class BaseCRUDRepository(Generic[Model]):
    """Base Class for CRUD operations. Class will be inherited by all Model Repositories."""

    def __init__(self, db: SessionLocal, model: Type[Model]):
        self.db = db
        self.model = model

    def create(self, attributes: dict):
        """
        Function creates a new instance of the model class and adds it to the database.
        It then returns that newly created object.

        Param attributes:dict: Pass in the attributes that will be used to create a new instance of the model
        Return: The newly created object.
        """
        try:
            db_obj = self.model(**attributes)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as exc:
            self.db.rollback()
            raise exc
        return db_obj

    def read_all(self):
        """
        Function is used to retrieve all the objects from a table.
        It takes no arguments and returns a list of model objects.

        Return: All the models of a specific model.
        """
        try:
            models = self.db.query(self.model).all()
            return models
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(e), code=500) from exc

    def read_many(self, *, skip: int = 0, limit: int = 100):
        """
        Function is used to retrieve a list of records from the database.
        It takes two keyword arguments: skip and limit. The skip argument specifies how many
        records to skip before starting to return results, and the limit argument specifies how many
        results should be returned.

        Param *: Indicate that the function can accept any number of keyword arguments
        Param skip:int=0: Skip the first n rows
        Param limit:int=100: Limit the number of returned results
        Return: A list of all the instances of the model class that are in the database.
        """
        try:
            result = self.db.query(self.model).offset(skip).limit(limit).all()
        except Exception as exc:
            self.db.rollback()
            raise AppException(message=str(exc), code=500) from exc
        return result

    def read_by_id(self, model_id: Union[str, int]):
        """
        Function accepts a model_id as an argument and returns the object with that ID.
        If no such object exists, it raises an AppException with code 400.

        Param model_id:Union[str: Specify the type of model_id
        Param int]: Cast the model_id to an integer
        Return: An object of the model class that matches the given ID.
        """
        try:
            obj = self.db.query(self.model).filter(self.model.id == model_id).first()
            if not obj:
                self.db.rollback()
                raise AppException(message=f"{self.model.__name__} ID: {model_id} does not exist in DB.", code=400)
            return obj
        except Exception as exc:
            self.db.rollback()
            raise exc

    def update(self, db_obj, updates: dict):
        """
        Function updates an existing object in the database.
        It takes two arguments, db_obj and updates. The db_obj is the object to be updated,
        and the updates are a dictionary of attributes to update on that object.

        Param db_obj: Pass the database object to be updated
        Param updates:dict: Update the object in the database
        Return: The updated object.
        """
        try:
            obj_data = jsonable_encoder(db_obj)
            for data in obj_data:
                if data in updates:
                    setattr(db_obj, data, updates[data])
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as exc:
            self.db.rollback()
            raise exc
        return db_obj

    def delete(self, model_id: Union[str, int]):
        """
        Function deletes a model from the database.
        It takes one argument, which is the ID of the model to be deleted.
        If no such object exists in the database, it raises an exception.

        Param model_id: Pass the ID of the model that is to be deleted.
        Return: True.
        """
        try:
            obj = self.db.query(self.model).filter(self.model.id == model_id).first()
            if obj is None:
                self.db.rollback()
                raise AppException(message=f"ID: {model_id} does not exist in Database.", code=400)
            self.db.delete(obj)
            self.db.commit()
        except Exception as exc:
            self.db.rollback()
            raise exc
        return True
