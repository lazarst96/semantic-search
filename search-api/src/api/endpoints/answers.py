from typing import List
from fastapi import APIRouter, Depends, Body, Path
from pymongo.database import Database

from src import repository, schemas
from src.api import deps


router = APIRouter()


@router.get("/{question}", response_model=List[schemas.Answer])
def get_answers(db: Database = Depends(deps.get_mongo_db),
                question: str = Path(...)):

    return repository.answer.get_answers_for_query(db=db, query=question)
