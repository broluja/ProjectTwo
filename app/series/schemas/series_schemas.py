"""Series Schemas module"""
from datetime import date
from pydantic import BaseModel, UUID4

from app.actors.schemas import ActorSchema
from app.directors.schemas import DirectorSchema
from app.genres.schemas import GenreSchema


class SeriesSchema(BaseModel):
    """Base Series Schema"""
    id: UUID4
    title: str
    description: str
    date_added: date
    year_published: str
    director_id: UUID4
    genre_id: UUID4

    class Config:
        """Configuration Class"""
        orm_mode = True


class SeriesSchemaIn(BaseModel):
    """Base Series Schema for input"""
    title: str
    description: str
    year_published: str
    director_id: UUID4
    genre_id: UUID4

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "True Detective",
                "description": "Short description...",
                "year_published": "1998",
                "director_id": "",
                "genre_id": "",
            }
        }


class SeriesWithActorsSchema(BaseModel):
    """Base Series Schema with Actors"""
    id: UUID4
    title: str
    description: str
    date_added: date
    year_published: str
    actors: list[ActorSchema]

    class Config:
        """Configuration Class"""
        orm_mode = True


class SeriesWithDirectorAndGenreSchema(BaseModel):
    """Base Series Schema with Genres and Directors"""
    id: UUID4
    title: str
    description: str
    date_added: date
    year_published: str
    director: DirectorSchema
    genre: GenreSchema

    class Config:
        """Configuration Class"""
        orm_mode = True


class SeriesFullSchema(BaseModel):
    """Full Series Schema"""
    id: UUID4
    title: str
    description: str
    date_added: date
    year_published: str
    actors: list[ActorSchema]
    director: DirectorSchema
    genre: GenreSchema

    class Config:
        """Configuration Class"""
        orm_mode = True
