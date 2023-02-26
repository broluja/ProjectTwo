"""Episode schemas module"""
from pydantic import BaseModel, UUID4


class EpisodeSchema(BaseModel):
    """Base Episode schema"""
    id: UUID4
    name: str
    description: str
    link: str
    series_id: str

    class Config:
        """Configuration Class"""
        orm_mode = True


class EpisodeSchemaIn(BaseModel):
    """Episode schema for input"""
    name: str
    description: str
    series_id: str

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Episode One",
                "description": "Short description...",
                "series_id": ""
            }
        }
