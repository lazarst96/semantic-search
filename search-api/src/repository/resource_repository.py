from typing import List, Optional
import time
from functools import cmp_to_key
import logging

import numpy as np
import spacy
from pymongo.database import Database

from src import schemas, models
from src.services import ModelServing
from src.core.config import settings
from src.db import milvus_db


class ResourceRepository(object):
    __mongo_collection_name = "answers"
    __nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def __ranked_resource_cmp_score(r1: schemas.RankedResource, r2: schemas.RankedResource):
        if r1.score > r2.score:
            return 1
        elif r1.score < r2.score:
            return -1
        else:
            return 0

    @staticmethod
    def __search_params(embedding, top_k):
        return {
            'collection_name': settings.ANSWERS_COLLECTION,
            'query_records': [embedding],
            'top_k': top_k,
            'params': {
                "nprobe": settings.SEARCH_N_PROBE
            }
        }

    def get_all(self, db: Database) -> List[models.Resource]:
        answers_cursor = db.get_collection(self.__mongo_collection_name) \
            .find({}).limit(10)

        return list(map(lambda doc: models.Resource(**doc), answers_cursor))

    def create(self, db: Database, payload: schemas.ResourceIn) -> models.Resource:
        # Extracting Sentences from text/document
        sentences = [s.text for s in self.__nlp(payload.content).sents]

        # Calculating Text Embedding
        embeddings = ModelServing.get_resource_embedding(sentences=[payload.content, *sentences],
                                                         contexts=[payload.content] * (len(sentences) + 1))
        sentences_obj = [{
            "text": sent,
            "embedding": emb
        } for sent, emb in zip(sentences, embeddings[1:])]

        status, ids = milvus_db.connection.insert(
            collection_name=settings.ANSWERS_COLLECTION,
            records=[embeddings[0]])

        if status.code == 0:
            obj = models.Resource(**{
                "index_id": ids[0],
                "content": payload.content,
                "owner": payload.owner,
                "embedding": embeddings[0],
                "sentences": sentences_obj
            })
            op = db.get_collection(self.__mongo_collection_name).insert_one(obj.dict())
            obj.id = op.inserted_id
            milvus_db.connection.flush([settings.ANSWERS_COLLECTION])

            return obj
        else:
            raise Exception(f'Milvus Inserting Error - {str(status)}')

    def get_resources_for_query(self, db: Database, query: str, top_k: int = 5) -> List[schemas.RankedResource]:
        start = time.time()
        embedding = ModelServing.get_question_embedding(question=query)

        status, results = milvus_db.connection.search(**self.__search_params(embedding, top_k))
        if status.OK():
            score_mapper = {}
            ids = []
            for result in results[0]:
                score_mapper[result.id] = result.distance
                ids.append(result.id)

            resources_cursor = db.get_collection(self.__mongo_collection_name).find({'index_id': {'$in': ids}})

            response = []
            for obj in resources_cursor:
                response.append(schemas.RankedResource(**{
                    **obj,
                    'score': score_mapper[obj['index_id']]
                }))

            response.sort(key=cmp_to_key(self.__ranked_resource_cmp_score), reverse=True)
            logging.info(f"Searching time {time.time() - start}")
            return response
        else:
            return []


resource = ResourceRepository()
