from typing import Generator
from pymongo import MongoClient

from src.core.config import settings


def get_mongo_db() -> Generator:
    client = None
    try:
        client = MongoClient(host=settings.MONGO_HOST,
                             port=27017,
                             username=settings.MONGO_USERNAME,
                             password=settings.MONGO_PASSWORD)
        yield client[settings.MONGO_DB]
    finally:
        if client is not None:
            client.close()

