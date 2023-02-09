from pydantic import BaseModel, UUID4
from datetime import date

from app.actors.schemas import ActorSchema


class MovieSchema(BaseModel):
    id: UUID4
    title: str
    date_added: date
    year_published: str

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    title: str
    year_published: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Blockbuster",
                "year_published": "2005"
            }
        }


class MovieWithActorsSchema(BaseModel):
    title: str
    date_added: date
    year_published: str

    actors: list[ActorSchema]

    class Config:
        orm_mode = True
