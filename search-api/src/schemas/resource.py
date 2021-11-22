from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from src.models.base import PyObjectId


class ResourceIn(BaseModel):
    content: str
    owner: Optional[str] = None


class Sentence(BaseModel):
    text: str


class Resource(BaseModel):
    id: PyObjectId = Field(alias="_id")
    content: str
    owner: Optional[str]
    sentences: List[Sentence]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RankedResource(BaseModel):
    id: PyObjectId = Field(alias="_id")
    content: str
    owner: Optional[str]
    score: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
