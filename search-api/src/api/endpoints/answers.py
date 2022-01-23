from typing import List
from fastapi import APIRouter, Depends, Query, Path
from pymongo.database import Database

from src import repository, schemas
from src.api import deps


router = APIRouter()


@router.get("/{question}", response_model=List[schemas.Answer])
def get_answers(db: Database = Depends(deps.get_mongo_db),
                question: str = Path(...),
                top_k: int = Query(default=5)):

    return repository.answer.get_answers_for_query(db=db, query=question, top_k=top_k)
