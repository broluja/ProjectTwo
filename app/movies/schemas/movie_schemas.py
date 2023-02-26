"""Movie Schemas module"""
from datetime import date
from pydantic import BaseModel, UUID4

from app.actors.schemas import ActorSchema
from app.directors.schemas import DirectorSchema
from app.genres.schemas import GenreSchema


class MovieSchema(BaseModel):
    """Base Movie Schema"""
    id: UUID4
    title: str
    description: str
    date_added: date
    year_published: str
    link: str
    director_id: str
    genre_id: str

    class Config:
        """Configuration Class"""
        orm_mode = True


class MovieSchemaIn(BaseModel):
    """Movie Schema for input"""
    title: str
    description: str
    year_published: str
    director_id: str
    genre_id: str

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Blockbuster",
                "description": "short description...",
                "year_published": "2005",
                "director_id": "",
                "genre_id": ""
            }
        }


class MovieWithActorsSchema(BaseModel):
    """Movie schema with Actors"""
    id: UUID4
    title: str
    description: str
    year_published: str
    link: str

    actors: list[ActorSchema]

    class Config:
        """Configuration Class"""
        orm_mode = True


class MovieWithDirectorAndGenreSchema(BaseModel):
    """Movie schema with Genre and Director"""
    id: UUID4
    title: str
    description: str
    year_published: str
    link: str

    director: DirectorSchema
    genre: GenreSchema

    class Config:
        """Configuration Class"""
        orm_mode = True


class MovieFullSchema(BaseModel):
    """Full Movie Schema"""
    id: UUID4
    title: str
    description: str
    year_published: str
    link: str

    director: DirectorSchema
    genre: GenreSchema
    actors: list[ActorSchema]

    class Config:
        """Configuration Class"""
        orm_mode = True
