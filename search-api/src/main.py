import uvicorn
from fastapi import FastAPI

from src.api import api_router
from src.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router=api_router, prefix=settings.API_PREFIX)

if __name__ == '__main__':
    uvicorn.run(app=app)
