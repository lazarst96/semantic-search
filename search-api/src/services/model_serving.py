from typing import List
import json
import httpx

from src.core.config import settings


class ModelServing(object):
    text_model_url = settings.TF_SERVING_URL
    headers = {"content-type": "application/json"}

    @classmethod
    async def get_text_embedding_async(cls, text: str) -> List[float]:
        data = json.dumps({"signature_name": "serving_default", "instances": [text]})
        client = httpx.AsyncClient()
        response = await client.post(cls.text_model_url, data=data, headers=cls.headers)
        await client.aclose()
        predictions = json.loads(response.text)["predictions"][0]

        return predictions

    @classmethod
    async def get_batch_text_embedding(cls, texts: List[str]) -> List[List[float]]:
        data = json.dumps({"signature_name": "serving_default", "instances": texts})
        client = httpx.AsyncClient()
        response = await client.post(cls.text_model_url, data=data, headers=cls.headers)
        await client.aclose()
        predictions = json.loads(response.text)["predictions"]

        return predictions
