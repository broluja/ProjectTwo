"""Actor Schemas module"""
from pydantic import BaseModel, UUID4
from datetime import date


class ActorSchema(BaseModel):
    """Base actor schema"""
    id: UUID4
    first_name: str
    last_name: str
    date_of_birth: date
    country: str

    class Config:
        """Configuration Class"""
        orm_mode = True


class ActorSchemaIn(BaseModel):
    """Actor schema for input"""
    first_name: str
    last_name: str
    date_of_birth: str
    country: str

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1983-03-22",
                "country": "USA"
            }
        }
