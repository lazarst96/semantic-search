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

    def get_all(self, db: Database) -> List[models.Answer]:
        answers_cursor = db.get_collection(self.__mongo_collection_name) \
            .find({}).limit(10)

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

    def get_answers_for_query(self, db: Database, query: str, top_k: int = 5) -> List[schemas.Answer]:
        start = time.time()
        question_embedding = ModelServing.get_question_embedding(question=query)

        status, results = milvus_db.connection.search(**self.__search_params(question_embedding, 2*top_k))
        if status.OK():
            score_mapper = {}
            ids = []
            for result in results[0]:
                score_mapper[result.id] = result.distance
                ids.append(result.id)

            resources_cursor = db.get_collection(self.__mongo_collection_name).find({'index_id': {'$in': ids}})

            embedded = []
            embedded_obj_id = []
            embedded_sent_ids = []
            existing_embeddings = []

            non_embedded = []
            non_embedded_obj_id = []
            non_embedded_sent_ids = []

            sentences = []
            contexts = []

            for obj in resources_cursor:
                if len(obj['sentences']) == 0 or obj['sentences'][0]['embedding'] is not None:
                    embedded.append(obj)
                    existing_embeddings.extend([sent['embedding'] for sent in obj['sentences']])
                    embedded_obj_id.extend([len(embedded) - 1] * len(obj['sentences']))
                    embedded_sent_ids.extend(range(len(obj['sentences'])))
                else:
                    non_embedded.append(obj)
                    sentences.extend([sent['text'] for sent in obj['sentences']])
                    contexts.extend([obj['content']] * len(obj['sentences']))
                    non_embedded_obj_id.extend([len(non_embedded) - 1] * len(obj['sentences']))
                    non_embedded_sent_ids.extend(range(len(obj['sentences'])))

            # Fetch Embeddings
            print(non_embedded_obj_id)
            if len(non_embedded):
                new_embeddings = ModelServing.get_resource_embedding(sentences=sentences, contexts=contexts)
            else:
                new_embeddings = []

            print(len(new_embeddings))
            all_embeddings = np.array(existing_embeddings + new_embeddings)
            all_objects = embedded + non_embedded
            all_obj_ids = embedded_obj_id + [i + len(embedded) for i in non_embedded_obj_id]
            all_sent_ids = embedded_sent_ids + non_embedded_sent_ids
            print(all_embeddings.shape)
            print(all_obj_ids)
            sentences_scores = (all_embeddings @ np.array(question_embedding)).tolist()
            print(sentences_scores)
            selected_indexes = np.argsort(sentences_scores).tolist()
            print(selected_indexes)

            response = []

            for index in selected_indexes[-top_k:]:
                obj = all_objects[all_obj_ids[index]]
                sentence_obj = obj["sentences"][all_sent_ids[index]]

                sentence_obj['score'] = sentences_scores[index]
                sentence_obj['selected'] = True

                response.append(obj)

            # Cache Embedding in Mongo DB
            cur_sent = 0
            prev_index = -1
            for index, sent_embedding in zip(non_embedded_obj_id, new_embeddings):
                if prev_index == index:
                    cur_sent += 1
                else:
                    cur_sent = 0

                cur_obj = non_embedded[index]
                # Update Embedding in Mongo record
                db.get_collection(self.__mongo_collection_name).update_one(
                    {'_id': cur_obj['_id']},
                    {'$set': {f"sentences.{cur_sent}.embedding": sent_embedding}})

                prev_index = index

            response.reverse()
            logging.info(f"Searching time {time.time() - start}")
            return response
        else:
            return []


resource = ResourceRepository()
