from fastapi import APIRouter

from .endpoints import questions, resources, answers

api_router = APIRouter()

api_router.include_router(router=questions.router, prefix='/questions', tags=['Questions'])
api_router.include_router(router=resources.router, prefix='/resources', tags=['Resources'])
api_router.include_router(router=answers.router, prefix='/answers', tags=['Answers'])
