from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from .base import PyObjectId


class Sentence(BaseModel):
    text: str = Field(...)
    embedding: Optional[List[float]] = Field(..., min_items=512)


class Resource(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    index_id: int = Field(...)
    content: str = Field(...)
    owner: Optional[str] = None
    sentences: List[Sentence] = Field(...)
    embedding: List[float] = Field(..., min_items=512)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
