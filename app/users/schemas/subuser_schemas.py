"""Subuser schemas module"""
from datetime import date
from pydantic import BaseModel, UUID4


class SubuserSchema(BaseModel):
    """Base schema for Subuser"""
    id: UUID4
    name: str
    date_subscribed: date

    class Config:
        """Configuration Class"""
        orm_mode = True


class SubuserSchemaIn(BaseModel):
    """Base Subuser schema for input"""
    name: str
    date_subscribed: date

    class Config:
        """Configuration Class"""
        orm_mode = True
