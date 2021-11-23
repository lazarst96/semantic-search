from typing import List
import time
import logging

import numpy as np
import spacy
from pymongo.database import Database

from src import schemas
from src.services import ModelServing
from src.core.config import settings
from src.db import milvus_db


class AnswersRepository(object):
    __mongo_collection_name = "answers"
    __nlp = spacy.load('en_core_web_sm')

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

    def __cache_embeddings_in_mongo(self, db: Database,
                                    sentence_to_obj_index: List[int],
                                    objects: List[dict],
                                    embeddings: List[List[float]]) -> None:
        """
        Function which caches calculated sentences embeddings to MongoDB

            :param db: Mongo DB Database object
            :param sentence_to_obj_index: Mapper which maps sentence to its object in objects array
            :param objects: Objects to be updated
            :param embeddings: Embeddings for each sentence
            :return:
        """
        cur_sent = 0
        prev_index = -1
        for index, sent_embedding in zip(sentence_to_obj_index, embeddings):
            if prev_index == index:
                cur_sent += 1
            else:
                cur_sent = 0

            cur_obj = objects[index]
            # Update Embedding in Mongo record
            db.get_collection(self.__mongo_collection_name).update_one(
                {'_id': cur_obj['_id']},
                {'$set': {f"sentences.{cur_sent}.embedding": sent_embedding}})

            prev_index = index

    def get_answers_for_query(self, db: Database, query: str, top_k: int = 5) -> List[schemas.Answer]:
        start = time.time()

        # Calculate given question embedding
        question_embedding = ModelServing.get_question_embedding(question=query)

        # Get best responses for given query from vector DB
        status, results = milvus_db.connection.search(**self.__search_params(question_embedding, 2 * top_k))
        if status.OK():

            # Build array from selected indexes
            ids = [res.id for res in results[0]]

            # Fetch resource objects from Mongo DB
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

            # Separating Objects with sentence embeddings from those which don't have them
            for obj in resources_cursor:
                obj_sentences = obj['sentences']
                if len(obj_sentences) == 0 or obj_sentences[0]['embedding'] is not None:
                    embedded.append(obj)
                    existing_embeddings.extend([sent['embedding'] for sent in obj_sentences])
                    embedded_obj_id.extend([len(embedded) - 1] * len(obj_sentences))
                    embedded_sent_ids.extend(range(len(obj_sentences)))
                else:
                    non_embedded.append(obj)
                    sentences.extend([sent['text'] for sent in obj_sentences])
                    contexts.extend([obj['content']] * len(obj_sentences))
                    non_embedded_obj_id.extend([len(non_embedded) - 1] * len(obj_sentences))
                    non_embedded_sent_ids.extend(range(len(obj_sentences)))

            # Calculate Embeddings
            if len(non_embedded):
                new_embeddings = ModelServing.get_resource_embedding(sentences=sentences, contexts=contexts)
            else:
                new_embeddings = []

            all_embeddings = np.array(existing_embeddings + new_embeddings)
            all_objects = embedded + non_embedded
            all_obj_ids = embedded_obj_id + [i + len(embedded) for i in non_embedded_obj_id]
            all_sent_ids = embedded_sent_ids + non_embedded_sent_ids

            # Calculating Sentences scores
            sentences_scores = (all_embeddings @ np.array(question_embedding)).tolist()
            selected_indexes = np.argsort(sentences_scores).tolist()

            # Cache Embedding in Mongo DB
            self.__cache_embeddings_in_mongo(
                db=db,
                sentence_to_obj_index=non_embedded_obj_id,
                objects=non_embedded,
                embeddings=new_embeddings)

            # Postprocess records to be suitable for response
            response = []
            unique_obj = set()
            for index in selected_indexes[-top_k:]:
                obj = all_objects[all_obj_ids[index]]
                sentence_obj = obj["sentences"][all_sent_ids[index]]

                sentence_obj['score'] = sentences_scores[index]
                sentence_obj['selected'] = True
                if obj['_id'] not in unique_obj:
                    unique_obj.add(obj['_id'])
                    response.append(obj)

            # List order is in decreasing order by score - so need to be reversed
            response.reverse()
            logging.info(f"Searching time {time.time() - start}")
            return response
        else:
            return []


answer = AnswersRepository()
