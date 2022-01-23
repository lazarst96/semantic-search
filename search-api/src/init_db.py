from typing import List
import json
import logging
import httpx
import spacy
from pymongo import MongoClient
from milvus import Milvus, MetricType

from src.core.config import settings
from src.db import milvus_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = '/app/data'

RESET_RESPONSE_COLLECTION = False
RESET_QUESTIONS_COLLECTION = False

RESPONSE_SIGNATURE = "response_encoder"
QUESTIONS_SIGNATURE = "question_encoder"

QA_MODEL_URL = f"{settings.TF_SERVING_URL}/qa:predict"

RESOURCE_COLLECTION = "answers"
QUESTIONS_COLLECTION = "questions"


def get_resources_embedding(client: httpx.Client, contexts: List[str]) -> List[List[float]]:
    """Get Embedding from model serving service
            Parameters:
                client (httpx.Client): HttpX Sync Client Object
                contexts (List[str]): Contexts to be embedded
            Returns:
                embeddings (List[List[float]]): list of embeddings for each context
    """
    payload = [{"input": context, "context": context} for context in contexts]
    data = {
        "signature_name": RESPONSE_SIGNATURE,
        "instances": payload
    }
    response = client.post(QA_MODEL_URL, json=data, headers={"content-type": "application/json"})
    predictions = json.loads(response.text)["predictions"]

    return predictions


def get_questions_embedding(client: httpx.Client, questions: List[str]) -> List[List[float]]:
    """Get Embedding from model serving service
            Parameters:
                client (httpx.Client): HttpX Sync Client Object
                questions (List[str]): Questions to be embedded
            Returns:
                embeddings (List[List[float]]): list of embeddings for each question
    """
    data = {
        "signature_name": QUESTIONS_SIGNATURE,
        "instances": questions
    }
    response = client.post(QA_MODEL_URL, json=data, headers={"content-type": "application/json"})
    predictions = json.loads(response.text)["predictions"]

    return predictions


def clear_mongo_collection(client: MongoClient, collection_name: str) -> None:
    """Delete all records from specified MongoDB collection
        Parameters:
            client (MongoClient): PyMongo client object
            collection_name (str): Name of the collection which will be cleared
        Returns:
            None
    """

    client.get_database(settings.MONGO_DB). \
        get_collection(collection_name). \
        delete_many({})


def create_or_clear_milvus_collection(db: Milvus, collection_name: str, should_clear: bool = False) -> None:
    """Create (if not exists) or Clear (existing) Milvus Collection
            Parameters:
                db (Milvus): Milvus DB object
                collection_name (str): Name of the collection which will be created or cleared
                should_clear (str): Should clear collection (Default is False)
            Returns:
                None
        """
    status, ok = db.has_collection(collection_name)

    if ok and should_clear:
        db.drop_collection(collection_name)

    if not ok or should_clear:
        params = {
            'collection_name': collection_name,
            'dimension': settings.VECTOR_DIM,
            'index_file_size': settings.INDEX_FILE_SIZE,
            'metric_type': MetricType.IP
        }
        db.create_collection(params)


def insert_responses_batch(client: MongoClient, collection_name: str, batch_data: List[str]) -> None:
    records = []
    embeddings = get_resources_embedding(http_client, batch_data)
    status, ids = milvus_db.connection.insert(
        collection_name=settings.ANSWERS_COLLECTION,
        records=embeddings)
    if status.code:
        logging.error(f"Error during inserting data - {str(status)}")
        return

    for res, emb, ind_id in zip(batch_data, embeddings, ids):
        sentences = [{
            'text': s.text,
            'embedding': None
        } for s in nlp(res).sents]

        records.append({
            "index_id": ind_id,
            "content": res,
            "owner": None,
            "embedding": emb,
            "sentences": sentences,

        })
    client.get_database(settings.MONGO_DB). \
        get_collection(collection_name). \
        insert_many(records)


def insert_questions_batch(client: MongoClient, collection_name: str, batch_data: List[str]) -> None:
    records = []
    embeddings = get_questions_embedding(http_client, batch_data)
    status, ids = milvus_db.connection.insert(
        collection_name=settings.QUESTIONS_COLLECTION,
        records=embeddings)
    if status.code:
        logging.error(f"Error during inserting data - {str(status)}")
        return

    for res, emb, ind_id in zip(batch_data, embeddings, ids):
        records.append({
            "index_id": ind_id,
            "text": res,
            "owner": None,
            "embedding": emb
        })
    client.get_database(settings.MONGO_DB). \
        get_collection(collection_name). \
        insert_many(records)


if __name__ == '__main__':
    mongo_client = MongoClient(host=settings.MONGO_HOST,
                               port=settings.MONGO_PORT,
                               username=settings.MONGO_USERNAME,
                               password=settings.MONGO_PASSWORD)
    http_client = httpx.Client()

    if RESET_RESPONSE_COLLECTION:
        clear_mongo_collection(client=mongo_client,
                               collection_name=RESOURCE_COLLECTION)
        create_or_clear_milvus_collection(db=milvus_db.connection,
                                          collection_name=settings.ANSWERS_COLLECTION,
                                          should_clear=True)

        nlp = spacy.load('en_core_web_sm')
        with open(f'{DATA_DIR}/resources.txt') as file:
            batch = []
            for i, line in enumerate(file):
                if (i + 1) % 10000 == 0:
                    logging.info(f"Line {i+1} processed!")

                batch.append(line.replace('\n', ''))

                if len(batch) == 256:
                    insert_responses_batch(client=mongo_client,
                                           collection_name=RESOURCE_COLLECTION,
                                           batch_data=batch)

                    batch = []

            if len(batch) > 0:
                insert_responses_batch(client=mongo_client,
                                       collection_name=RESOURCE_COLLECTION,
                                       batch_data=batch)

    if RESET_QUESTIONS_COLLECTION:
        clear_mongo_collection(client=mongo_client, collection_name=QUESTIONS_COLLECTION)
        create_or_clear_milvus_collection(db=milvus_db.connection,
                                          collection_name=settings.QUESTIONS_COLLECTION,
                                          should_clear=True)

        nlp = spacy.load('en_core_web_sm')
        with open(f'{DATA_DIR}/questions.txt') as file:
            batch = []
            for i, line in enumerate(file):
                if (i + 1) % 10000 == 0:
                    logging.info(f"Line {i + 1} processed!")

                batch.append(line.replace('\n', ''))

                if len(batch) == 256:
                    insert_questions_batch(client=mongo_client,
                                           collection_name=QUESTIONS_COLLECTION,
                                           batch_data=batch)

                    batch = []

            if len(batch) > 0:
                insert_questions_batch(client=mongo_client,
                                       collection_name=QUESTIONS_COLLECTION,
                                       batch_data=batch)

    http_client.close()
