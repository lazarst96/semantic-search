from typing import List, Optional

import spacy
from pymongo.database import Database

from src import schemas, models
from src.services import ModelServing
from src.core.config import settings
from src.db import milvus_db


class ResourceRepository(object):
    __mongo_collection_name = "answers"
    __nlp = spacy.load('en_core_web_sm')

    def get_all(self, db: Database) -> List[models.Answer]:
        answers_cursor = db.get_collection(self.__mongo_collection_name) \
            .find({})

        return list(map(lambda doc: models.Answer(**doc), answers_cursor))

    def create(self, db: Database, payload: schemas.ResourceIn) -> models.Answer:
        # Extracting Sentences from text/document
        sentences = [s.text for s in self.__nlp(payload.content).sents]

        # Extracting Sentences from text/document
        embeddings = ModelServing.get_batch_text_embedding(texts=[payload.content, *sentences])
        sentences_obj = [{
            "text": sent,
            "embedding": emb
        } for sent, emb in zip(sentences, embeddings[1:])]

        obj = models.Answer(**{
            "content": payload.content,
            "owner": payload.owner,
            "embedding": embeddings[0],
            "sentences": sentences_obj
        })

        op = db.get_collection(self.__mongo_collection_name).insert_one(obj.dict())
        obj.id = op.inserted_id

        status, ids = milvus_db.connection.insert(
            collection_name=settings.ANSWERS_COLLECTION,
            records=[embeddings[0]])

        print(ids)
        print(status)

        return obj


resource = ResourceRepository()
