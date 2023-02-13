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
        try:
            db_obj = self.model(**attributes)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as e:
            self.db.rollback()
            raise e
        return db_obj

    def read_all(self):
        try:
            models = self.db.query(self.model).all()
            return models
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)

    def read_many(self, *, skip: int = 0, limit: int = 100):
        try:
            result = self.db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            self.db.rollback()
            raise AppException(message=str(e), code=500)
        return result

    def read_by_id(self, model_id: Union[str, int]):
        try:
            obj = self.db.query(self.model).filter(self.model.id == model_id).first()
            if not obj:
                self.db.rollback()
                raise AppException(message=f"{self.model.__name__} ID: {model_id} does not exist in DB.", code=400)
            return obj
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, db_obj, updates: dict):
        try:
            obj_data = jsonable_encoder(db_obj)
            for data in obj_data:
                if data in updates:
                    setattr(db_obj, data, updates[data])
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as e:
            self.db.rollback()
            raise e
        return db_obj

    def delete(self, model_id: Union[str, int]):
        try:
            obj = self.db.query(self.model).filter(self.model.id == model_id).first()
            if obj is None:
                self.db.rollback()
                raise AppException(message=f"ID: {model_id} does not exist in Database.", code=400)
            self.db.delete(obj)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        return True
