import logging
from fastapi import APIRouter, Depends
from pymongo import MongoClient
from pymongo.database import Database

from src.api import deps

router = APIRouter()


@router.get("/test")
def test(db: Database = Depends(deps.get_mongo_db)):

    # inserted_id = db.answers.insert_one({"text": "This is a answer!"}).inserted_id
    # logging.info(str(inserted_id))
    logging.info(db.answers.count())
    document = db.answers.find_one({})
    return document['text']
