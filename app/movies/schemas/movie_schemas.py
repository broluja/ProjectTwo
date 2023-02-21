"""Movie Schemas module"""
from pydantic import BaseModel, UUID4
from datetime import date

from app.actors.schemas import ActorSchema
from app.directors.schemas import DirectorSchema
from app.genres.schemas import GenreSchema


class MovieSchema(BaseModel):
    """Base Movie Schema"""
    id: UUID4
    title: str
    date_added: date
    year_published: str
    link: str
    director_id: str
    genre_id: str

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    """Movie Schema for input"""
    title: str
    year_published: str
    director_id: str
    genre_id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Blockbuster",
                "year_published": "2005",
                "director_id": "",
                "genre_id": ""
            }
        }


class MovieWithActorsSchema(BaseModel):
    """Movie schema with Actors"""
    id: UUID4
    title: str
    year_published: str
    link: str

    actors: list[ActorSchema]

    class Config:
        orm_mode = True


class MovieWithDirectorAndGenreSchema(BaseModel):
    """Movie schema with Genre and Director"""
    id: UUID4
    title: str
    year_published: str
    link: str

    director: DirectorSchema
    genre: GenreSchema

    class Config:
        orm_mode = True


class MovieFullSchema(BaseModel):
    """Full Movie Schema"""
    id: UUID4
    title: str
    year_published: str
    link: str

    director: DirectorSchema
    genre: GenreSchema
    actors: list[ActorSchema]

    class Config:
        orm_mode = True
