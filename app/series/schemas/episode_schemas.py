from pydantic import BaseModel, UUID4


class EpisodeSchema(BaseModel):
    id: UUID4
    name: str
    link: str
    series_id: str

    class Config:
        orm_mode = True


class EpisodeSchemaIn(BaseModel):
    name: str
    series_id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Episode One",
                "series_id": ""
            }
        }
