from typing import List
from fastapi import APIRouter, Depends, Body, Path, Query
from pymongo.database import Database

from src import repository, schemas
from src.api import deps

router = APIRouter()


@router.get("/{question}", response_model=List[schemas.RankedResource])
def get_resources_by_query(db: Database = Depends(deps.get_mongo_db),
                           question: str = Path(...),
                           top_k: int = Query(default=5)):
    return repository.resource.get_resources_for_query(db=db, query=question, top_k=top_k)


@router.get("", response_model=List[schemas.Resource])
def get_all_resources(db: Database = Depends(deps.get_mongo_db)):
    return repository.resource.get_all(db=db)


@router.post("", response_model=schemas.Resource)
def create_resource(db: Database = Depends(deps.get_mongo_db),
                    payload: schemas.ResourceIn = Body(...)):
    return repository.resource.create(db=db, payload=payload)
