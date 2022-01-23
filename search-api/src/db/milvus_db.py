import logging
from milvus import Milvus, IndexType, MetricType, Status

from src.core.config import settings


def create_connection() -> Milvus:
    return Milvus(host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)


def create_collections_if_not_exist(db: Milvus):
    status, ok = db.has_collection(settings.QUESTIONS_COLLECTION)
    if not ok:
        resources_params = {
            'collection_name': settings.QUESTIONS_COLLECTION,
            'dimension': settings.VECTOR_DIM,
            'index_file_size': settings.INDEX_FILE_SIZE,
            'metric_type': MetricType.IP
        }
        db.create_collection(resources_params)

        index_param = {
            'nlist': settings.INDEX_N_LIST
        }
        status = db.create_index(settings.QUESTIONS_COLLECTION, IndexType.IVF_FLAT, index_param)
        if not status.OK():
            logging.error("Creating Index failed: {}".format(status))
        else:
            logging.info(f"Created collection {settings.QUESTIONS_COLLECTION} and Index!")
    else:
        logging.info(f"Collection {settings.QUESTIONS_COLLECTION} already exists!")

    status, ok = db.has_collection(settings.ANSWERS_COLLECTION)
    if not ok:
        resources_params = {
            'collection_name': settings.ANSWERS_COLLECTION,
            'dimension': settings.VECTOR_DIM,
            'index_file_size': settings.INDEX_FILE_SIZE,
            'metric_type': MetricType.IP
        }
        db.create_collection(resources_params)

        index_param = {
            'nlist': settings.INDEX_N_LIST
        }
        status = db.create_index(settings.ANSWERS_COLLECTION_COLLECTION, IndexType.IVF_FLAT, index_param)
        if not status.OK():
            logging.error("Creating Index failed: {}".format(status))
        else:
            logging.info(f"Created collection {settings.ANSWERS_COLLECTION} and Index!")
    else:
        logging.info(f"Collection {settings.ANSWERS_COLLECTION} already exists!")


connection = create_connection()
