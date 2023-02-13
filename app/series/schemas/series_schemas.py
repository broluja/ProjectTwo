from pydantic import BaseModel, UUID4
from datetime import date

from app.actors.schemas import ActorSchema
from app.directors.schemas import DirectorSchema
from app.genres.schemas import GenreSchema


class SeriesSchema(BaseModel):
    id: UUID4
    title: str
    date_added: date
    year_published: str
    director_id: str
    genre_id: str

    class Config:
        orm_mode = True


class SeriesSchemaIn(BaseModel):
    title: str
    year_published: str
    director_id: str
    genre_id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "True Detective",
                "year_published": "1998",
                "director_id": "",
                "genre_id": "",
            }
        }


class SeriesWithActorsSchema(BaseModel):
    title: str
    date_added: date
    year_published: str
    actors: list[ActorSchema]

    class Config:
        orm_mode = True


class SeriesWithDirectorAndGenreSchema(BaseModel):
    title: str
    date_added: date
    year_published: str
    director_id: DirectorSchema
    genre_id: GenreSchema

    class Config:
        orm_mode = True
