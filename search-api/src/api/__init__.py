from fastapi import APIRouter, Path, Body

from .endpoints import questions, answers
from src.services.model_serving import ModelServing

api_router = APIRouter()

api_router.include_router(router=questions.router, prefix='/questions', tags=['Questions'])
api_router.include_router(router=answers.router, prefix='/answers', tags=['Answers'])


@api_router.get("/embeddings/{text}")
async def hell_world(text: str = Path(...)):
    return await ModelServing.get_text_embedding_async(text=text)


@api_router.post("/embeddings")
async def batch_embedding(payload = Body(...)):
    return await ModelServing.get_batch_text_embedding(texts=payload['texts'])
