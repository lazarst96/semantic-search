from typing import List, Optional
import time
from functools import cmp_to_key

from pymongo.database import Database

from src import schemas, models
from src.services import ModelServing
from src.core.config import settings
from src.db import milvus_db


class QuestionsRepository(object):
    __mongo_collection_name = "questions"

    @staticmethod
    def __search_params(embedding, top_k):
        return {
            'collection_name': settings.QUESTIONS_COLLECTION,
            'query_records': [embedding],
            'top_k': top_k,
            'params': {
                "nprobe": settings.SEARCH_N_PROBE
            }
        }

    @staticmethod
    def __similar_question_cmp_score(q1: schemas.SimilarQuestion, q2: schemas.SimilarQuestion):
        if q1.score > q2.score:
            return 1
        elif q1.score < q2.score:
            return -1
        else:
            return 0

    def get_all(self, db: Database) -> List[models.Question]:
        questions_cursor = db.get_collection(self.__mongo_collection_name).find({})

        return list(map(lambda doc: models.Question(**doc), questions_cursor))

    def create(self, db: Database, payload: schemas.QuestionIn) -> Optional[models.Question]:
        # Extracting Sentences from text/document
        embedding = ModelServing.get_text_embedding(text=payload.text)
        status, ids = milvus_db.connection.insert(
            collection_name=settings.QUESTIONS_COLLECTION,
            records=[embedding])
        if status.code == 0:
            obj = models.Question(**{
                "index_id": ids[0],
                "text": payload.text,
                "owner": payload.owner,
                "embedding": embedding
            })

            op = db.get_collection(self.__mongo_collection_name).insert_one(obj.dict())
            obj.id = op.inserted_id
            milvus_db.connection.flush([settings.QUESTIONS_COLLECTION])

            return obj

    def get_similar(self, db: Database, query: str, top_k: int = 5) -> List[schemas.SimilarQuestion]:
        start = time.time()
        embedding = ModelServing.get_text_embedding(text=query)

        status, results = milvus_db.connection.search(**self.__search_params(embedding, top_k))
        if status.OK():
            score_mapper = {}
            ids = []
            for result in results[0]:
                score_mapper[result.id] = result.distance
                ids.append(result.id)

            questions_cursor = db.get_collection(self.__mongo_collection_name).find({'index_id': {'$in': ids}})

            response = []
            for obj in questions_cursor:
                response.append(schemas.SimilarQuestion(**{
                    **obj,
                    'score': score_mapper[obj['index_id']]
                }))

            response.sort(key=cmp_to_key(self.__similar_question_cmp_score), reverse=True)
            print(f"Searching time {time.time() - start}")
            return response
        else:
            return []


question = QuestionsRepository()
