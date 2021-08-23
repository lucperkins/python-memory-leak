import logging
import os
from random import choices, randrange
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any

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


def log_result(endpoint: str, method: str, status: int) -> None:
    logger.info('response received', extra={
        'endpoint': endpoint, 'method': method, 'status': status})


def random_text() -> str:
    value_length = randrange(25, 100)
    return ''.join(choices(ascii_lowercase + ascii_uppercase + digits, k=value_length))


class Client(object):
    def __init__(self) -> None:
        http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
        logger.info('connecting to cache API',
                    extra={'address': http_endpoint})

        cache_endpoint = f'{http_endpoint}/cache'

        self.endpoint = cache_endpoint

        s = requests.Session()
        retries = Retry(total=20, backoff_factor=0.5)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        self.session = s

    def get(self, key: str) -> None:
        key_endpoint = f'{self.endpoint}/{key}'
        res = self.session.get(key_endpoint)
        log_result(key_endpoint, 'GET', res.status_code)

    def put(self, key: str, value: Any) -> None:
        key_endpoint = f'{self.endpoint}/{key}'
        res = self.session.put(key_endpoint, json={'value': value})
        log_result(key_endpoint, 'PUT', res.status_code)


def main():
    client = Client()

    n = 1

    while True:
        res: Response

        # PUT to the cache
        key = f'key-{n}'
        value = random_text()
        client.put(key, value)

        # GET previously written keys from the cache 10 times (some will be missing)
        for _ in range(0, 10):
            r = randrange(0, n)
            key = f'key-{r}'
            client.get(key)

        n += 1


if __name__ == '__main__':
    main()
