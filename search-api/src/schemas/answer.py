from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from src.models.base import PyObjectId


class Sentence(BaseModel):
    text: str
    selected: bool = False
    score: Optional[float]


class Answer(BaseModel):
    id: PyObjectId = Field(alias="_id")
    owner: Optional[str]
    sentences: List[Sentence]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}