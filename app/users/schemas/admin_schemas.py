"""Admin Schema module"""
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class AdminSchema(BaseModel):
    """Base schema for Admin"""
    id: UUID4 = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    address: str
    country: str
    user_id: UUID4 = Field(default_factory=uuid4)

    class Config:
        """Configuration Class"""
        orm_mode = True


class AdminSchemaIn(BaseModel):
    """Base Admin schema for input"""
    first_name: str
    last_name: str
    address: str
    country: str
    user_id: UUID4

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address": "1st Street, Chicago",
                "country": "USA",
                "user_id": ""
            }
        }
