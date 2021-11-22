from typing import List
from fastapi import APIRouter, Depends, Path, Body, Query
from pymongo.database import Database
from src import repository, schemas

from src.api import deps

router = APIRouter()


@router.get("/{question}/similar", response_model=List[schemas.SimilarQuestion])
def get_similar_questions(db: Database = Depends(deps.get_mongo_db),
                          question: str = Path(...),
                          top_k: int = Query(default=5)):
    return repository.question.get_similar(db=db, query=question, top_k=top_k)


@router.get("", response_model=List[schemas.Question])
def get_question_list(db: Database = Depends(deps.get_mongo_db)):
    return repository.question.get_all(db=db)


@router.post("", response_model=schemas.Question)
def create_question(db: Database = Depends(deps.get_mongo_db),
                    payload: schemas.QuestionIn = Body(...)):
    return repository.question.create(db=db, payload=payload)
