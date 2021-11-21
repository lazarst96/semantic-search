from typing import List
from fastapi import APIRouter, Depends, Body
from pymongo.database import Database

from src import repository, schemas
from src.api import deps


router = APIRouter()


@router.get("/reset")
def reset_collection(db: Database = Depends(deps.get_mongo_db)):
    db.get_collection("answers").delete_many({})
    return {'message': 'OK!'}


@router.get("", response_model=List[schemas.Resource])
def get_all_answers(db: Database = Depends(deps.get_mongo_db)):
    return repository.resource.get_all(db=db)


@router.post("", response_model=schemas.Resource)
def create_answer(db: Database = Depends(deps.get_mongo_db),
                  payload: schemas.ResourceIn = Body(...)):
    return repository.resource.create(db=db, payload=payload)
