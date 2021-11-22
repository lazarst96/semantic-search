from typing import List
import json
import httpx

from src.core.config import settings


class ModelServing(object):
    headers = {"content-type": "application/json"}

    text_model_url = f"{settings.TF_SERVING_URL}/dan:predict"
    qa_model_url = f"{settings.TF_SERVING_URL}/qa:predict"

    __question_signature = "question_encoder"
    __answer_signature = "response_encoder"

    @classmethod
    async def get_text_embedding_async(cls, text: str) -> List[float]:
        data = {"signature_name": "serving_default", "instances": [text]}
        client = httpx.AsyncClient()
        response = await client.post(cls.text_model_url, json=data, headers=cls.headers)
        await client.aclose()
        predictions = json.loads(response.text)["predictions"][0]

        return predictions

    @classmethod
    async def get_batch_text_embedding_async(cls, texts: List[str]) -> List[List[float]]:
        data = {"signature_name": "serving_default", "instances": texts}
        client = httpx.AsyncClient()
        response = await client.post(cls.text_model_url, json=data, headers=cls.headers)
        await client.aclose()
        predictions = json.loads(response.text)["predictions"]

        return predictions

    @classmethod
    def get_text_embedding(cls, text: str) -> List[float]:
        data = {"signature_name": "serving_default", "instances": [text]}
        client = httpx.Client()
        response = client.post(cls.text_model_url, json=data, headers=cls.headers)
        client.close()
        predictions = json.loads(response.text)["predictions"][0]

        return predictions

    @classmethod
    def get_batch_text_embedding(cls, texts: List[str]) -> List[List[float]]:
        data = {"signature_name": "serving_default", "instances": texts}
        client = httpx.Client()
        response = client.post(cls.text_model_url, json=data, headers=cls.headers)
        client.close()
        predictions = json.loads(response.text)["predictions"]

        return predictions

    @classmethod
    def get_question_embedding(cls, question: str) -> List[float]:
        data = {
            "signature_name": cls.__question_signature,
            "instances": [question]
        }
        client = httpx.Client()
        response = client.post(cls.qa_model_url, json=data, headers=cls.headers)
        predictions = json.loads(response.text)["predictions"][0]

        return predictions

    @classmethod
    def get_batch_question_embedding(cls, questions: List[str]) -> List[List[float]]:
        data = {
            "signature_name": cls.__question_signature,
            "instances": questions
        }
        client = httpx.Client()
        response = client.post(cls.qa_model_url, json=data, headers=cls.headers)
        predictions = json.loads(response.text)["predictions"]

        return predictions

    @classmethod
    def get_resource_embedding(cls, sentences: List[str], contexts: List[str]) -> List[float]:
        payload = [{"input": sent, "context": context} for sent, context in zip(sentences, contexts)]
        data = {
            "signature_name": cls.__answer_signature,
            "instances": payload
        }
        client = httpx.Client()
        response = client.post(cls.qa_model_url, json=data, headers=cls.headers)
        predictions = json.loads(response.text)["predictions"]

        return predictions
