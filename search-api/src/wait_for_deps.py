import logging

import httpx
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 3


QA_MODEL_URL = f"{settings.TF_SERVING_URL}/qa:predict"
RESPONSE_SIGNATURE = "response_encoder"


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_tf_serving() -> None:
    payload = [{"input": "This is input!", "context": 'This is context!'}]
    data = {
        "signature_name": RESPONSE_SIGNATURE,
        "instances": payload
    }
    client = httpx.Client()
    try:
        response = client.post(QA_MODEL_URL, json=data, headers={"content-type": "application/json"})
        if response.status_code != 200:
            raise Exception()
    except Exception as e:
        logger.error("Initialization Failed!")
        raise e
    finally:
        client.close()


if __name__ == "__main__":
    logger.info("Initializing TF Serving service")
    init_tf_serving()
    logger.info("TF Serving finished initializing")