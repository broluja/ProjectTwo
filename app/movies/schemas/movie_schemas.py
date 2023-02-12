from pydantic import BaseModel, UUID4
from datetime import date

from app.actors.schemas import ActorSchema
from app.directors.schemas import DirectorSchema
from app.genres.schemas import GenreSchema


class MovieSchema(BaseModel):
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
    id: UUID4
    title: str
    date_added: date
    year_published: str
    link: str

    actors: list[ActorSchema]

    class Config:
        orm_mode = True


class MovieWithDirectorAndGenreSchema(BaseModel):
    id: UUID4
    title: str
    date_added: date
    year_published: str
    link: str

    director: DirectorSchema
    genre: GenreSchema

    class Config:
        orm_mode = True
