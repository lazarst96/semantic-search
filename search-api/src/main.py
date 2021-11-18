import logging
import uvicorn
from fastapi import FastAPI

from src.api import api_router
from src.core.config import settings
from src.db import milvus_db


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router=api_router, prefix=settings.API_PREFIX)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
def init_vector_db():
    milvus_db.create_collections_if_not_exist(milvus_db.connection)


if __name__ == '__main__':
    uvicorn.run(app=app)
