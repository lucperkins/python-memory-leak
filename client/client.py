import logging
import os
import random

from pythonjsonlogger import jsonlogger
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(logHandler)


def coin_flip() -> bool:
    return bool(random.getrandbits(1))


def main():
    http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    cache_endpoint = f'{http_endpoint}/cache'

    logger.info('connecting to cache API', extra={'address': http_endpoint})

    s = requests.Session()
    retries = Retry(total=20, backoff_factor=0.5)

    s.mount('http://', HTTPAdapter(max_retries=retries))

    n = 0

    while True:
        res: Response

        key = f'key-{n}'
        value = f'some-value-{n}'
        key_endpoint = f'{cache_endpoint}/{key}'

        # Alternate between POSTs and GETS
        if coin_flip():
            res = s.post(key_endpoint, json={'value': value})
        else:
            res = s.get(key_endpoint)

        logger.info('response received', extra={
                    'endpoint': key_endpoint, 'method': 'GET', 'status': res.status_code})

        n += 1


if __name__ == '__main__':
    main()
