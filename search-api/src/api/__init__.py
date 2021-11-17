from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/hello-world")
async def hell_world():
    return {"message": 'OK'}
