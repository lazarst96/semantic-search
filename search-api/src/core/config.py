from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Search API"
    API_PREFIX: str = "/api"

    MONGO_DB: str = 'search-db'
    MONGO_HOST: str = 'search'
    MONGO_USERNAME: str = 'mongo-user'
    MONGO_PASSWORD: str = 'mongo-pass'

    TF_SERVING_URL: AnyHttpUrl = 'http://tf-serving:8501/v1/models/dan:predict'

    MILVUS_HOST = 'milvus'
    MILVUS_PORT = '19530'
    ANSWERS_COLLECTION = 'answers'
    QUESTIONS_COLLECTION = 'questions'
    VECTOR_DIM = 512
    INDEX_FILE_SIZE = 64
    INDEX_N_LIST = 2048
    SEARCH_N_PROBE = 16


settings = Settings()
