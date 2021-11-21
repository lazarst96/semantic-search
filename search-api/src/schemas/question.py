from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from src.models.base import PyObjectId


class QuestionIn(BaseModel):
    text: str
    owner: Optional[str] = None


class Question(BaseModel):
    id: PyObjectId = Field(alias="_id")
    index_id: int
    text: str
    owner: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SimilarQuestion(Question):
    score: float