from typing import List
import json
import httpx

from src.core.config import settings

text_model_url = 'http://localhost:8501/v1/models/qa:predict'
headers = {"content-type": "application/json"}
data = {"signature_name": "question_encoder", "instances": ["this is test"]}
client = httpx.Client()
response = client.post(text_model_url, json=data, headers=headers)
predictions = json.loads(response.text)["predictions"]
print(predictions)

payload = {
    "input": 'this is Input!',
    "context": 'this is context!'
}
data = json.dumps({"signature_name": "response_encoder", "instances": [payload]})
client = httpx.Client()
response = client.post(text_model_url, data=data, headers=headers)
client.close()
print(response.status_code, response.text)
predictions = json.loads(response.text)["predictions"]
print(predictions)