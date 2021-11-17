from fastapi import APIRouter, Path


router = APIRouter()


@router.get("/{question}/similar")
async def get_similar_questions(question: str = Path(...)):
    return {"question": question}
