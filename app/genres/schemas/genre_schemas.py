"""Genre Schemas module"""
from pydantic import BaseModel, UUID4


class GenreSchema(BaseModel):
    """Base Genre schema"""
    id: UUID4
    name: str

    class Config:
        """Configuration Class"""
        orm_mode = True


class GenreSchemaIn(BaseModel):
    """Genre schema for input"""
    name: str

    class Config:
        """Configuration Class"""
        orm_mode = True
